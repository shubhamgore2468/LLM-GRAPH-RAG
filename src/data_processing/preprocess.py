import json
from pathlib import Path
from langchain.text_splitter import TokenTextSplitter
import logging
# from logging_config import setup_logging
# setup_logging()


def preprocess_document(path):
    # file_path='../data/crawl_new.json'
    file_path = path
    print(f"Starting to preprocess document at path: {file_path}")

    try:
        data = json.loads(Path(file_path).read_text())

        text_splitter = TokenTextSplitter(chunk_size=512, chunk_overlap=24)
        print("Initialized TokenTextSplitter")


        # Flatten the page_content and create the split documents
        split_documents = []
        for item_key, item_value in data.items():
            # Combine title, description, and reviews for page content
            content = item_value.get('title', '') + " " + item_value.get('description', '') + item_value.get('about') + " " + " ".join(item_value.get('reviews', []))
            
            # Split content using the text splitter and retain metadata
            split_docs = text_splitter.create_documents([content], metadatas=[{"product": item_key}])
            split_documents.extend(split_docs)


        documents = text_splitter.split_documents(split_documents)
        print("preprocesing document Successful")
        return documents
    except Exception as e:
        logging.error(f"An error occurred during preprocessing: {e}")
        raise