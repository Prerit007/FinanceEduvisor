from llama_index.core.memory import ChatMemoryBuffer
from llama_index.core.chat_engine.types import BaseChatEngine
from llama_index.core.query_engine import RouterQueryEngine, BaseQueryEngine
from llama_index.core.selectors import LLMSingleSelector
from llama_index.core.tools import QueryEngineTool
from llama_index.core import VectorStoreIndex, Settings
from prompts import TEACHER_SYSTEM_PROMPT, GUIDE_SYSTEM_PROMPT

def create_teacher_chat_engine(teacher_index: VectorStoreIndex) -> tuple[BaseChatEngine, BaseQueryEngine]:
    memory = ChatMemoryBuffer.from_defaults(token_limit=1500)
    
    # Create enhanced chat engine with custom prompt
    chat_engine = teacher_index.as_chat_engine(
        system_prompt=TEACHER_SYSTEM_PROMPT + """
        You are a financial expert assistant. If the knowledge base doesn't contain enough information to answer a question,
        you can use your own knowledge to provide a comprehensive answer. Always try to be helpful and informative.
        """,
        memory=memory,
        chat_mode="context",
        response_mode="tree_summarize",
        streaming=True,
        llm=Settings.llm,
        verbose=True
    )
    
    # Create enhanced query engine with custom prompt
    query_engine = teacher_index.as_query_engine(
        response_mode="tree_summarize",
        streaming=True,
        llm=Settings.llm,
        verbose=True,
        text_qa_template="""You are a financial expert assistant. Use the following pieces of context to answer the question at the end. 
        If you don't know the answer based on the context, you can use your own knowledge to provide a comprehensive answer.
        If the context doesn't contain enough information, feel free to supplement it with your own knowledge.
        
        Context: {context_str}
        
        Question: {query_str}
        
        Answer: """
    )
    
    print("Enhanced Teacher Chat Engine and Query Engine created.")
    return chat_engine, query_engine

def create_guide_chat_engine(advisor_index: VectorStoreIndex) -> tuple[BaseChatEngine, BaseQueryEngine]:
    memory = ChatMemoryBuffer.from_defaults(token_limit=4000)
    
    # Create enhanced chat engine without query transforms
    chat_engine = advisor_index.as_chat_engine(
        system_prompt=GUIDE_SYSTEM_PROMPT,
        memory=memory,
        chat_mode="context",
        response_mode="tree_summarize",
        streaming=True
    )
    
    # Create enhanced query engine without query transforms
    query_engine = advisor_index.as_query_engine(
        response_mode="tree_summarize",
        streaming=True
    )
    
    print("Enhanced Guide Chat Engine and Query Engine created.")
    return chat_engine, query_engine

def create_router_query_engine(query_engine_tools_list: list[QueryEngineTool]) -> RouterQueryEngine:
    selector = LLMSingleSelector.from_defaults()
    
    router_engine = RouterQueryEngine(
        selector=selector,
        query_engine_tools=query_engine_tools_list,
        verbose=True
    )
    print("Router Query Engine created.")
    return router_engine