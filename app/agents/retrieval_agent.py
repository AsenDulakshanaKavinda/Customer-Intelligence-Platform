from app.utils import get_logger, cfg
from tools import retriever_tool

from langchain.agents import create_agent
from pydantic import BaseModel, Field


log = get_logger(__file__)

class RetrievalAgentOutput:
    content: str = Field(..., description="")


try:
    retrieval_agent = create_agent(
        model=cfg.model.retrieval_agent_model,
        system_prompt="system_prompt",
        tools=[retriever_tool],
        response_format=RetrievalAgentOutput
    )
    log.info("Initializing retrieval agent")
except Exception as e:
    log.error(f"Error in retrieval agent {str(e)}")
    raise RuntimeError("Error in retrieval agent")
