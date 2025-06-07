from llama_index.core.tools import QueryEngineTool
from llama_index.core.chat_engine.types import BaseChatEngine

def get_teacher_tool(teacher_chat_engine: BaseChatEngine) -> QueryEngineTool:
    """Creates a QueryEngineTool for the Teacher Chat Engine."""
    return QueryEngineTool.from_defaults(
        query_engine=teacher_chat_engine,
        name="FinanceTeacher",
        description="Use this for educational questions about finance. It can define financial terms, explain concepts like stocks, bonds, P/E ratios, diversification, risk, asset allocation, and market basics. It uses a curated knowledge base for factual answers."
    )

def get_guide_tool(guide_chat_engine: BaseChatEngine) -> QueryEngineTool:
    """Creates a QueryEngineTool for the Guide Chat Engine."""
    return QueryEngineTool.from_defaults(
        query_engine=guide_chat_engine,
        name="FinancialGuide",
        description="Use this when the user seeks financial guidance, suggestions on how to invest, what types of investments to consider, portfolio structuring ideas, or help related to their financial goals, risk tolerance, and investment timeline. This tool can engage in a conversation to understand the user's profile and uses an advisory knowledge base."
    )