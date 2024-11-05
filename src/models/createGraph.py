import os
from langchain_openai  import ChatOpenAI
from langchain_experimental.graph_transformers import LLMGraphTransformer
from langchain_community.vectorstores import Neo4jVector
from langchain_openai import OpenAIEmbeddings
from yfiles_jupyter_graphs import GraphWidget
from neo4j import GraphDatabase
from langchain_community.graphs import Neo4jGraph
from dotenv import load_dotenv
from database.GraphModel import graph_instance as graph

load_dotenv()

os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')

llm = ChatOpenAI(model='gpt-3.5-turbo')
llm_transformer = LLMGraphTransformer(llm=llm)


def add_data_to_graph(documents):

    try:
        graph_documents = llm_transformer.convert_to_graph_documents(documents)

        graph.add_graph_documents(
            graph_documents,
            baseEntityLabel=True,
            include_source=True
        )


    except Exception as e:
        print(f"An error occurred while adding data to the graph: {e}")