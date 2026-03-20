from app.utils import get_logger, cfg

from langchain.chat_models import init_chat_model
from langchain.agents import create_agent
from pydantic import BaseModel, Field
from typing import Literal

log = get_logger(__file__)

model = init_chat_model(cfg.model.classification_agent_model)

classification_agent_system_prompt = """

"""

class ClassificationAgentOutput(BaseModel):
    sentiment: str = Literal["positive", "negative", "natural"]
    topic: str = Literal["topic 1", "topic 2"]


try:
    classification_agent = create_agent(
        model = model,
        system_prompt = classification_agent_system_prompt,
        response_format = ClassificationAgentOutput
    )
    log.info("Initializing classification agent")
except Exception as e:
    log.error(f"Error in classification agent {str(e)}")
    raise RuntimeError("Error in classification agent")
