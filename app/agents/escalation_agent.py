from app.utils import get_logger, cfg

from langchain.agents import create_agent


log = get_logger(__file__)


try:
    escalation_agent = create_agent(
        model=cfg.model.escalation_agent_model,
        system_prompt="system_prompt",
        tools=[],
    )
    log.info("Initializing escalation agent")
except Exception as e:
    log.error(f"Error in escalation agent {str(e)}")
    raise RuntimeError("Error in escalation agent")
