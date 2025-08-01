# pip install --upgrade --quiet langchain langchain-community langchain-openai langchain-experimental neo4j wikipedia tiktoken yfiles_jupyter_graphs'
import os



os.environ['NEO4J_USERNAME'] = NEO4J_USERNAME
os.environ['NEO4J_PASSWORD'] = NEO4J_PASSWORD
os.environ['NEO4J_URI'] = NEO4J_URI
os.environ['OPENAI_API_KEY'] = OPENAI_API_KEY


from langchain_community.graphs import Neo4jGraph
graph = Neo4jGraph()

from langchain_community.document_loaders import JSONLoader
import json
from pathlib import Path

file_path='../data/crawl_new.json'
data = json.loads(Path(file_path).read_text())
data

from langchain.text_splitter import TokenTextSplitter
text_splitter = TokenTextSplitter(chunk_size=512, chunk_overlap=24)

# Flatten the page_content and create the split documents
split_documents = []
for item_key, item_value in data.items():
    # Combine title, description, and reviews for page content
    content = item_value.get('title', '') + " " + item_value.get('description', '') + " " + " ".join(item_value.get('reviews', []))
    
    # Split content using the text splitter and retain metadata
    split_docs = text_splitter.create_documents([content], metadatas=[{"product": item_key}])
    split_documents.extend(split_docs)

for doc in split_documents:
    print(doc)
documents = text_splitter.split_documents(split_documents)
documents
from langchain_openai import ChatOpenAI
llm = ChatOpenAI(model='gpt-3.5-turbo')

from langchain_experimental.graph_transformers import LLMGraphTransformer
llm_transformer = LLMGraphTransformer(llm=llm)
graph_documents = llm_transformer.convert_to_graph_documents(documents)
graph_documents
graph.add_graph_documents(
    graph_documents,
    baseEntityLabel=True,
    include_source=True
)

# ---------------------------------------------------------------------------------------------------


default_cypher = "MATCH (s)-[r:!MENTIONS]->(t) RETURN s,r,t LIMIT 50"



from yfiles_jupyter_graphs import GraphWidget
from neo4j import GraphDatabase


def showGraph(cypher: str = default_cypher):
    # create a neo4j session to run queries
    driver = GraphDatabase.driver(
        uri = os.environ["NEO4J_URI"],
        auth = (os.environ["NEO4J_USERNAME"],
                os.environ["NEO4J_PASSWORD"]))
    session = driver.session()
    widget = GraphWidget(graph = session.run(cypher).graph())
    widget.node_label_mapping = 'id'
    display(widget)
    return widget



showGraph()




from langchain_community.vectorstores import Neo4jVector



from typing import Tuple, List, Optional




from langchain_openai import OpenAIEmbeddings
vector_index = Neo4jVector.from_existing_graph(
    OpenAIEmbeddings(),
    search_type="hybrid",
    node_label="Document",
    text_node_properties=["text"],
    embedding_node_property="embedding",
    index_name="new_vector_index"
)



graph.query("CREATE FULLTEXT INDEX entity IF NOT EXISTS FOR (e:__Entity__) ON EACH [e.id]")



from langchain_core.pydantic_v1 import BaseModel, Field
# Extract entities from text
class Entities(BaseModel):
    """Identifying information about entities."""

    names: List[str] = Field(
        ...,
        description="All the person, organization, or business entities that "
        "appear in the text",
    )


from langchain_core.prompts import ChatPromptTemplate
from langchain_core.prompts.prompt import PromptTemplate



prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are extracting product reviews of people from ecommerce platform and person entities from the text.",
        ),
        (
            "human",
            "Use the given format to extract information from the following "
            "input: {question}",
        ),
    ]
)



entity_chain = prompt | llm.with_structured_output(Entities)




entity_chain.invoke({"question": "which product is better?"}).names



from langchain_community.vectorstores.neo4j_vector import remove_lucene_chars



def generate_full_text_query(input: str) -> str:
    full_text_query = ""
    words = [el for el in remove_lucene_chars(input).split() if el]
    for word in words[:-1]:
        full_text_query += f" {word}~2 AND"
    full_text_query += f" {words[-1]}~2"
    return full_text_query.strip()




def structured_retriever(question: str) -> str:
    result = ""
    entities = entity_chain.invoke({"question": question})
    for entity in entities.names:
        response = graph.query(
            """CALL db.index.fulltext.queryNodes('entity', $query, {limit:2})
            YIELD node, score
            CALL {
              WITH node
              MATCH (node)-[r:MENTIONS]->(neighbor)
              RETURN node.id + ' - ' + type(r) + ' -> ' + neighbor.id AS output
              UNION ALL
              MATCH (node)<-[r:MENTIONS]-(neighbor)
              RETURN neighbor.id + ' - ' + type(r) + ' -> ' + node.id AS output
            }
            RETURN output LIMIT 50
            """,
            {"query": generate_full_text_query(entity)},
        )
        result += "\n".join([el['output'] for el in response])
    return result



def retriever(question: str):
    print(f"Search query: {question}")
    structured_data = structured_retriever(question)
    unstructured_data = [el.page_content for el in vector_index.similarity_search(question)]
    final_data = f"""Structured data:
{structured_data}
Unstructured data:
{"#Document ". join(unstructured_data)}
    """
    return final_data



_template = """Given the following conversation and a follow up question, rephrase the follow up question to be a standalone question,
in its original language.
Chat History:
{chat_history}
Follow Up Input: {question}
Standalone question:"""



CONDENSE_QUESTION_PROMPT = PromptTemplate.from_template(_template)



from langchain_core.runnables import (
    RunnableBranch,
    RunnableLambda,
    RunnableParallel,
    RunnablePassthrough,
)




from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.output_parsers import StrOutputParser



_search_query = RunnableBranch(
    # If input includes chat_history, we condense it with the follow-up question
    (
        RunnableLambda(lambda x: bool(x.get("chat_history"))).with_config(
            run_name="HasChatHistoryCheck"
        ),  # Condense follow-up question and chat into a standalone_question
        RunnablePassthrough.assign(
            chat_history=lambda x: _format_chat_history(x["chat_history"])
        )
        | CONDENSE_QUESTION_PROMPT
        | ChatOpenAI(temperature=0)
        | StrOutputParser(),
    ),
    # Else, we have no chat history, so just pass through the question
    RunnableLambda(lambda x : x["question"]),
)



template = """Answer the question based only on the following context:
{context}

Question: {question}
Use natural language and be concise.
Answer:"""




prompt = ChatPromptTemplate.from_template(template)



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


# chain.invoke({"question": "which is better for taking photos and processing them for photography"})
