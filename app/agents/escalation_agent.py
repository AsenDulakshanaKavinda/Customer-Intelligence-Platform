from app.utils import get_logger, cfg

from langchain.chat_models import init_chat_model
from langchain.agents import create_agent

log = get_logger(__file__)

model = init_chat_model(cfg.model.escalation_agent_model)

escalation_agent_system_prompt = """

"""

try:
    escalation_agent = create_agent(
        model = model,
        system_prompt = escalation_agent_system_prompt,
        tools = [],
    )
    log.info("Initializing escalation agent")
except Exception as e:
    log.error(f"Error in escalation agent {str(e)}")
    raise RuntimeError("Error in escalation agent")
