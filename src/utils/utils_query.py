# from langchain_community.vectorstores.neo4j_vector import remove_lucene_chars
# from inference.langchain_integration import entity_chain, vector_index

# from database.GraphModel import graph_instance as graph

# def generate_full_text_query(input: str) -> str:
#     full_text_query = ""
#     words = [el for el in remove_lucene_chars(input).split() if el]
#     for word in words[:-1]:
#         full_text_query += f" {word}~2 AND"
#     full_text_query += f" {words[-1]}~2"
#     return full_text_query.strip()

# def structured_retriever(question: str) -> str:
#     result = ""
#     entities = entity_chain.invoke({"question": question})
#     for entity in entities.names:
#         response = graph.query(
#             """CALL db.index.fulltext.queryNodes('entity', $query, {limit:2})
#             YIELD node, score
#             CALL {
#               WITH node
#               MATCH (node)-[r:MENTIONS]->(neighbor)
#               RETURN node.id + ' - ' + type(r) + ' -> ' + neighbor.id AS output
#               UNION ALL
#               MATCH (node)<-[r:MENTIONS]-(neighbor)
#               RETURN neighbor.id + ' - ' + type(r) + ' -> ' + node.id AS output
#             } IN TRANSACTIONS 
#             RETURN output LIMIT 50
#             """,
#             {"query": generate_full_text_query(entity)},
#         )
#         result += "\n".join([el['output'] for el in response])
#     return result

# def retriever(question: str):
#     print(f"Search query: {question}")
#     structured_data = structured_retriever(question)
#     unstructured_data = [el.page_content for el in vector_index.similarity_search(question)]
#     final_data = f"""Structured data:
# {structured_data}
# Unstructured data:
# {"#Document ". join(unstructured_data)}
#     """
#     return final_data