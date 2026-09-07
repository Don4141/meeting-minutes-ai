import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

TRANSCRIPTION_MODEL = "gpt-4o-transcribe-diarize"
ANALYSIS_MODEL  = "openai/gpt-5.6-terra"

def openai_client():
    """
    Create and return authenticated Openai client
    """
    openai_api_key = os.getenv("OPENAI_API_KEY")
    
    if not openai_api_key:
        raise ValueError(
                "OPENAI_API_KEY do not exist"
                "Add to the local environ")
    
    return OpenAI(api_key=openai_api_key)


def anthropic_client():
    """
    Create and return authenticated OpenAI-compatible client for the anthropic endpoint
    """
    anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")
    anthropic_base_url = os.getenv("ANTHROPIC_BASE_URL")
    
    if not anthropic_api_key:
        raise ValueError(
            "ANTHROPIC_API_KEY do not exist"
            "Add to local environ")
    
    if not anthropic_base_url:
        raise ValueError(
            "ANTHROPIC_BASE_URL do not exit"
            "Add to local environ")
    
    return OpenAI(base_url=anthropic_base_url,
                  api_key=anthropic_api_key)