from app.utils import get_logger, cfg

from langchain.agents import create_agent


log = get_logger(__file__)


try:
    router_agent = create_agent(
        model=cfg.model.router_agent_model,
        system_prompt="system_prompt",
        tools=[],
    )
    log.info("Initializing router agent")
except Exception as e:
    log.error(f"Error in router agent {str(e)}")
    raise RuntimeError("Error in router agent")
