import os
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.core.query_engine import BaseQueryEngine, RetrieverQueryEngine
from llama_index.core.retrievers import VectorIndexRetriever
from llama_index.core.response_synthesizers import get_response_synthesizer
from llama_index.core.postprocessor import SimilarityPostprocessor
from llama_index.core import Settings

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
    
    # Create vector retriever
    vector_retriever = VectorIndexRetriever(
        index=index,
        similarity_top_k=5
    )
    
    # Create response synthesizer with custom prompt
    response_synthesizer = get_response_synthesizer(
        response_mode="tree_summarize",
        structured_answer_filtering=True,
        llm=Settings.llm,
        verbose=True,
        text_qa_template="""You are a financial expert assistant. Use the following pieces of context to answer the question at the end. 
        If you don't know the answer based on the context, you can use your own knowledge to provide a comprehensive answer.
        If the context doesn't contain enough information, feel free to supplement it with your own knowledge.
        
        Context: {context_str}
        
        Question: {query_str}
        
        Answer: """
    )
    
    # Create postprocessor with lower similarity cutoff
    similarity_postprocessor = SimilarityPostprocessor(similarity_cutoff=0.6)  # Lowered from 0.7
    
    # Create the enhanced query engine
    query_engine = RetrieverQueryEngine(
        retriever=vector_retriever,
        response_synthesizer=response_synthesizer,
        node_postprocessors=[similarity_postprocessor]
    )
    
    return index
