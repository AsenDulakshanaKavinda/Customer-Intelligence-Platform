from app.utils import get_logger, cfg

from langchain.agents import create_agent


log = get_logger(__file__)


try:
    retrieval_agent = create_agent(
        model=cfg.model.retrieval_agent_model,
        system_prompt="system_prompt",
        tools=[],
    )
    log.info("Initializing retrieval agent")
except Exception as e:
    log.error(f"Error in retrieval agent {str(e)}")
    raise RuntimeError("Error in retrieval agent")
