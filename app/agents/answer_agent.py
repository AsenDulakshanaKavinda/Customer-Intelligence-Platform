from app.utils import get_logger, cfg

from langchain.agents import create_agent


log = get_logger(__file__)


try:
    answer_agent = create_agent(
        model=cfg.model.answer_agent_model,
        system_prompt="system_prompt",
        tools=[],
    )
    log.info("Initializing answer agent")
except Exception as e:
    log.error(f"Error in answer agent {str(e)}")
    raise RuntimeError("Error in answer agent")
