from langchain_core.prompts import ChatPromptTemplate
from langchain_core.prompts.prompt import PromptTemplate
from langchain_openai import ChatOpenAI
from database.createGraph import llm
from utils.utils_query import retriever

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



chain.invoke({"question": "which is the best phone for daily usage?"})


chain.invoke({"question": "which is better for taking photos and processing them for photography"})
