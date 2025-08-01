import os
from langchain_community.graphs import Neo4jGraph
from dotenv import load_dotenv
import logging
# from logging_config import setup_logging

# setup_logging()
load_dotenv()

os.environ['NEO4J_USERNAME'] = "neo4j"
os.environ['NEO4J_PASSWORD'] = "bcZ7MfY1rSKjRjbJVXcnpTCQVGhpi5QUP2ai-22PGDk"
os.environ['NEO4J_URI'] = "neo4j+s://935f0b57.databases.neo4j.io"


# neo4j_url = os.getenv("NEO4J_URI")
# neo4j_username = os.getenv("NEO4J_USERNAME")
# neo4j_password = os.getenv("NEO4J_PASSWORD")

# try:
#     driver = GraphDatabase.driver(neo4j_url, auth=(neo4j_username, neo4j_password))
#     graph_instance = Neo4jGraph(driver)

#     # Verify the connection by running a simple query
#     with driver.session() as session:
#         result = session.run("RETURN 1")
#         if result.single()[0] == 1:
#             print("Successfully connected to Neo4j!")
#         else:
#             print("Failed to connect to Neo4j.")
    
# except Exception as e:
#     print(f"An error occurred: {e}")

try:
    graph_instance = Neo4jGraph()
    print("Successfully created graph instance.")
except Exception as e:
    logging.error(f"An error occurred with creating graph: {e}")