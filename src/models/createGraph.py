import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_experimental.graph_transformers import LLMGraphTransformer
from dotenv import load_dotenv
from src.database.GraphModel import graph
import logging

from src.logging_config import setup_logging
setup_logging()
load_dotenv()

if not os.getenv('GOOGLE_APPLICATION_CREDENTIALS'):
    raise EnvironmentError("GOOGLE_APPLICATION_CREDENTIALS is not set in the environment.")

llm = ChatGoogleGenerativeAI(model='gemini-2.5-flash-lite')
llm_transformer = LLMGraphTransformer(llm=llm)


def add_data_to_graph(documents):

    try:
        graph_documents = llm_transformer.convert_to_graph_documents(documents)
        # several API calls, depending on number of chunks, 

        graph.add_graph_documents(
            graph_documents,
            baseEntityLabel=True,
            include_source=True
        )
        logging.info("Successfully added data to the graph.")

    except Exception as e:
        logging.error(f"An error occurred while adding data to the graph: {e}")
        raise