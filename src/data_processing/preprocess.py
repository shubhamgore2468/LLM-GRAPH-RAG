from langchain_text_splitters import TokenTextSplitter
import logging


def preprocess_document(json_data):
    logging.info("Starting to preprocess in-memory JSON data...")

    try:
        text_splitter = TokenTextSplitter(chunk_size=512, chunk_overlap=24)
        logging.info("Initialized TokenTextSplitter")

        split_documents = []
        for item_key, item_value in json_data.items():
            title = item_value.get('title', '')
            description = item_value.get('description', '')
            about = item_value.get('about', '')
            reviews = item_value.get('reviews', [])
            content = title + " " + description + " " + about + " " + " ".join(reviews)

            split_docs = text_splitter.create_documents(
                [content],
                metadatas=[{"product": item_key}]
            )
            split_documents.extend(split_docs)

        logging.info("Preprocessing successful.")
        return split_documents

    except Exception as e:
        logging.error(f"An error occurred during preprocessing: {e}")
        raise
