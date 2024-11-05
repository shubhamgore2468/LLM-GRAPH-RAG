import os
from langchain_community.graphs import Neo4jGraph
from dotenv import load_dotenv

load_dotenv()

os.environ['NEO4J_USERNAME'] = "neo4j"
os.environ['NEO4J_PASSWORD'] = "0QpuNom0_Qr9-zLvCqyaaWTDE6FPI8T6zO87iIoRqXw"
os.environ['NEO4J_URI'] = "neo4j+s://dfea93cd.databases.neo4j.io"



graph_instance = Neo4jGraph()