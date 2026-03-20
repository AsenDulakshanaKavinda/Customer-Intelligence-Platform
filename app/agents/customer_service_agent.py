from app.utils import get_logger, cfg
from app.tools import retriever_tool, sql_tool

from langchain.chat_models import init_chat_model
from langchain.agents import create_agent



log = get_logger(__file__)

model = init_chat_model(cfg.model.customer_service_agent_model)

customer_service_system_prompt = """

"""

try:
    customer_service_system_agent = create_agent(
        model = model,
        system_prompt = customer_service_system_prompt,
        tools = [retriever_tool, sql_tool],
    )
    log.info("Initializing customer service agent")
except Exception as e:
    log.error(f"Error in customer service agent {str(e)}")
    raise RuntimeError("Error in customer service agent")
