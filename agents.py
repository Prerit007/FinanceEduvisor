from llama_index.core.memory import ChatMemoryBuffer
from llama_index.core.chat_engine.types import BaseChatEngine
from llama_index.core.query_engine import RouterQueryEngine, BaseQueryEngine
from llama_index.core.selectors import LLMSingleSelector
from llama_index.core.tools import QueryEngineTool
from llama_index.core import VectorStoreIndex
from prompts import TEACHER_SYSTEM_PROMPT, GUIDE_SYSTEM_PROMPT

def create_teacher_chat_engine(teacher_index: VectorStoreIndex) -> tuple[BaseChatEngine, BaseQueryEngine]:
    memory = ChatMemoryBuffer.from_defaults(token_limit=1500)
    chat_engine = teacher_index.as_chat_engine(
        system_prompt=TEACHER_SYSTEM_PROMPT,
        memory=memory,
        chat_mode="context",
    )
    query_engine = teacher_index.as_query_engine()
    print("Teacher Chat Engine and Query Engine created.")
    return chat_engine, query_engine

def create_guide_chat_engine(advisor_index: VectorStoreIndex) -> tuple[BaseChatEngine, BaseQueryEngine]:
    """Creates a LlamaIndex ChatEngine for the Guide agent."""
    memory = ChatMemoryBuffer.from_defaults(token_limit=4000)
    chat_engine = advisor_index.as_chat_engine(
        system_prompt=GUIDE_SYSTEM_PROMPT,
        memory=memory,
        chat_mode="context",
    )
    query_engine = advisor_index.as_query_engine()
    print("Guide Chat Engine and Query Engine created.")
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