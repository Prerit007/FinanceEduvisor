import os
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.core.query_engine import BaseQueryEngine


def create_query_engine(path: str) -> VectorStoreIndex | None:
    print(f"Loading document from {path}")
    if not os.path.exists(path):
        print(f"Document {path} does not exist.")
        return None
    documents = SimpleDirectoryReader(path).load_data()
    if not documents:
        print(f"No documents found in {path}.")
        return None
    print(f"Creating index for {len(documents)} documents/nodes.")
    index = VectorStoreIndex.from_documents(documents)
    return index
