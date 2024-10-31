import json
from pathlib import Path
from langchain.text_splitter import TokenTextSplitter


file_path='../data/crawl_new.json'
data = json.loads(Path(file_path).read_text())

text_splitter = TokenTextSplitter(chunk_size=512, chunk_overlap=24)


# Flatten the page_content and create the split documents
split_documents = []
for item_key, item_value in data.items():
    # Combine title, description, and reviews for page content
    content = item_value.get('title', '') + " " + item_value.get('description', '') + " " + " ".join(item_value.get('reviews', []))
    
    # Split content using the text splitter and retain metadata
    split_docs = text_splitter.create_documents([content], metadatas=[{"product": item_key}])
    split_documents.extend(split_docs)


documents = text_splitter.split_documents(split_documents)
