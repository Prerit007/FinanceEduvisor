import os
import sys
from datetime import datetime
from dotenv import load_dotenv
from llama_index.core import Settings
from kb_handler import create_query_engine
from prompts import ROUTER_SYSTEM_PROMPT_TEMPLATE
from tools import get_teacher_tool, get_guide_tool
import google.generativeai as genai
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.gemini import Gemini as LlamaIndexGeminiLLM
from agents import create_teacher_chat_engine, create_guide_chat_engine, create_router_query_engine


def run_finguide_modular():
    print("Initializing Modular LlamaIndex-centric FinGuide Assistant...")
    try:
        initialize_llama_index_settings()
    except Exception as e:
        print(f"Critical error during LlamaIndex settings initialization: {e}")
        return

    print("\nLoading/Creating Knowledge Base Indexes...")
    teacher_index = create_query_engine("kb_path1")
    advisor_index = create_query_engine("kb_path")

    if teacher_index is None or advisor_index is None:
        print("FATAL ERROR: Failed to initialize one or more knowledge base indexes. Exiting.")
        return
    print("Knowledge Base Indexes ready.")

    print("\nCreating Chat Engines...")
    try:
        teacher_chat_engine, teacher_query_engine = create_teacher_chat_engine(teacher_index)
        guide_chat_engine, guide_query_engine = create_guide_chat_engine(advisor_index)
        print("Chat Engines ready.")
    except Exception as e:
        print(f"FATAL ERROR: Could not create chat engines: {e}")
        import traceback
        traceback.print_exc()
        return

    print("\nCreating Tools for Router...")
    teacher_tool = get_teacher_tool(teacher_query_engine)
    guide_tool = get_guide_tool(guide_query_engine)
    query_engine_tools = [teacher_tool, guide_tool]
    print("Tools ready.")

    print("\nSetting up Query Router...")
    try:
        router_query_engine = create_router_query_engine(query_engine_tools)
        print("Query Router ready.")
    except Exception as e:
        print(f"FATAL ERROR: Could not set up router: {e}")
        import traceback
        traceback.print_exc()
        return

    print(f"\n--- Welcome to Modular LlamaIndex FinGuide Assistant! (Current as of {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}) ---")
    print("You can ask educational questions or seek general financial guidance. Type 'exit' or 'quit' to end.")

    while True:
        user_input = input("You: ").strip()
        if user_input.lower() in ['exit', 'quit']:
            print("Exiting FinGuide Assistant. Goodbye!")
            break
        if not user_input:
            continue

        print("\nFinGuide (Router): Determining best assistant for your query...")
        try:
            router_response = router_query_engine.query(user_input)
            final_response = str(router_response.response if hasattr(router_response, 'response') else router_response)

        except Exception as e:
            final_response = f"Sorry, I encountered an error processing your request: {e}"
            print(f"DEBUG: Router/Agent Error: {e}")
            import traceback
            traceback.print_exc()

        print(f"\nFinGuide: {final_response}\n")

def initialize_llama_index_settings(): 
    load_dotenv()
    google_api_key = os.getenv("GOOGLE_API_KEY")
    if not google_api_key:
        raise ValueError("GOOGLE_API_KEY not found. Please set it.")
    
    try:
        genai.configure(api_key=google_api_key)
        print("Base google.generativeai SDK configured successfully with API key.")

        print("Configuring LlamaIndex HuggingFace Embedding model...")
        Settings.embed_model = HuggingFaceEmbedding(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )
        print("LlamaIndex HuggingFace Embedding model object created.")

        Settings.llm = LlamaIndexGeminiLLM(
            model_name="models/gemini-1.5-flash-latest",
            api_key=google_api_key
        )
        print("LlamaIndex global LLM (Gemini) configured successfully.")
        
        print("All LlamaIndex global settings configured.")

    except Exception as e:
        print(f"FATAL ERROR: Error configuring LlamaIndex Settings (LLM/Embeddings): {e}")
        raise

if __name__ == "__main__":
    run_finguide_modular()