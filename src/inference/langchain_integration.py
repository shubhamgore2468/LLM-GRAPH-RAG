from typing import Tuple, List
import os
import logging

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.prompts.prompt import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableBranch, RunnableLambda, RunnableParallel, RunnablePassthrough
from langchain_core.messages import AIMessage, HumanMessage

from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from google.oauth2 import service_account

from langchain_neo4j import Neo4jVector
from langchain_neo4j.vectorstores.neo4j_vector import remove_lucene_chars
from src.database.GraphModel import graph
from pydantic import BaseModel, Field

from dotenv import load_dotenv
load_dotenv()

_creds_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
if not _creds_path:
    raise EnvironmentError("GOOGLE_APPLICATION_CREDENTIALS is not set in the environment.")

_credentials = service_account.Credentials.from_service_account_file(
    _creds_path,
    scopes=["https://www.googleapis.com/auth/cloud-platform"],
)

llm = ChatGoogleGenerativeAI(model='gemini-2.5-flash-lite', credentials=_credentials)

def generate_full_text_query(input: str) -> str:
    logging.info(f"[generate_full_text_query] Raw input: {input}")
    full_text_query = ""
    words = [el for el in remove_lucene_chars(input).split() if el]
    if not words:
        return ""
    for word in words[:-1]:
        full_text_query += f" {word}~2 AND"
    full_text_query += f" {words[-1]}~2"
    query = full_text_query.strip()
    logging.info(f"[generate_full_text_query] Generated query: {query}")
    return query

def structured_retriever(question: str) -> str:
    # This function's core logic remains the same
    logging.info(f"[structured_retriever] Question received: {question}")
    result = ""
    entities = entity_chain.invoke({"question": question})
    logging.info(f"[structured_retriever] Extracted entities: {entities.names}")
    # Return early if no entities are found
    if not entities.names:
        return "" # Return an empty string
    
    for entity in entities.names:
        # ... rest of the function is the same
        ft_query = generate_full_text_query(entity)
        response = graph.query(
            """
            CALL db.index.fulltext.queryNodes('entity', $query, {limit: 2})
            YIELD node, score
            CALL (node) {
                WITH node
                MATCH (node)-[r]->(neighbor)
                RETURN node.id + ' - ' + type(r) + ' -> ' + neighbor.id AS output
                UNION ALL
                WITH node
                MATCH (node)<-[r]-(neighbor)
                RETURN neighbor.id + ' - ' + type(r) + ' -> ' + node.id AS output
            }
            RETURN output
            LIMIT 50
            """,
            {"query": ft_query},
        )
        result += "\n".join([el['output'] for el in response])
    return result

def retriever(question: str):
    logging.info(f"[retriever] Retrieving context for question: {question}")
    
    # Run both retrievers in parallel
    structured_data = structured_retriever(question)
    unstructured_results = vector_index.similarity_search(question)
    unstructured_data = [el.page_content for el in unstructured_results]
    
    # Conditionally build the final context
    final_context = []
    if structured_data:
        logging.info("Adding structured data to context.")
        final_context.append(f"Structured data:\n{structured_data}")
        
    if unstructured_data:
        logging.info("Adding unstructured data to context.")
        # Use a more descriptive joiner
        unstructured_context = "\n\n---\n\n".join(unstructured_data)
        final_context.append(f"Unstructured data:\n{unstructured_context}")

    final_data = "\n\n".join(final_context)
    logging.debug(f"[retriever] Final combined data:\n{final_data}")
    return final_data

vector_index = Neo4jVector.from_existing_graph(
    GoogleGenerativeAIEmbeddings(model="models/text-embedding-004", credentials=_credentials),
    search_type="hybrid",
    node_label="Document",
    text_node_properties=["text"],
    embedding_node_property="embedding",
    index_name="new_vector_index"
)


class Entities(BaseModel):
    """Identifying information about entities."""

    names: List[str] = Field(
        ...,
        description="All the person, organization, or business entities that "
        "appear in the text. If the text mentions a general category like 'phone' or 'product', "
        "include that as well.",
    )

entity_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are an expert at extracting product names, brands, and general product categories from a user's question. "
            "Your goal is to identify any specific entities mentioned."
        ),
        (
            "human",
            "Extract all entities from the following input, using the format provided: {question}",
        ),
    ]
)

entity_chain = entity_prompt | llm.with_structured_output(Entities)

_template = """
                Given the following conversation and a follow up question, rephrase the follow up question to be a standalone question,in its original language.
                Chat History:
                {chat_history}
                Follow Up Input: {question}
                Standalone question:
            """

CONDENSE_QUESTION_PROMPT = PromptTemplate.from_template(_template)

def _format_chat_history(chat_history: List[Tuple[str, str]]) -> List:
    logging.info(f"[_format_chat_history] Formatting chat history: {chat_history}")
    buffer = []
    for human, ai in chat_history:
        buffer.append(HumanMessage(content=human))
        buffer.append(AIMessage(content=ai))
    return buffer

_search_query = RunnableBranch(
    (
        RunnableLambda(lambda x: bool(x.get("chat_history"))).with_config(
            run_name="HasChatHistoryCheck"
        ),  
        RunnablePassthrough.assign(
            chat_history=lambda x: _format_chat_history(x["chat_history"])
        )
        | CONDENSE_QUESTION_PROMPT
        | llm
        | StrOutputParser(),
    ),
    RunnableLambda(lambda x : x["question"]),
)

question_template = """Answer the question based only on the following context:
                        {context}
                        Question: {question}
                        Use natural language and be concise.
                        Answer:
                    """

prompt = ChatPromptTemplate.from_template(question_template)

chain = (
    RunnableParallel(
        {
            "context": _search_query | retriever,
            "question": RunnablePassthrough(),
        }
    )
    | prompt
    | llm
    | StrOutputParser()
)

# chain.invoke({"question": "which is the best phone for daily usage?"})

def process_prompt(prompt: str, chat_history: List[dict] = None) -> str:
    # print(f"[process_prompt] Prompt: {prompt}")
    # print(f"[process_prompt] Chat history: {chat_history}")
    input_data = {
        "question": prompt,
        "chat_history": chat_history or []
    }
    logging.info(f"[process_prompt] Input data: {input_data}")
    result = chain.invoke(input_data)
    # print(f"[process_prompt] Final response: {result}")
    return result
