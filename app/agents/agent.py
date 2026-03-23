
import os
from uuid import uuid1
from dotenv import load_dotenv; load_dotenv()

from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver
from langchain.chat_models import init_chat_model
from app.utils import get_logger, cfg

os.environ["MISTRAL_API_KEY"] = os.getenv(cfg.models.api_key)
log = get_logger(__file__)


def load_agent_model(model_name: str):
    """Function to load the agent model based on the configuration."""
    try:
        model = init_chat_model(
            model = model_name
        )
        log.info("Agent model loaded successfully.")
        return model
    except Exception as e:
        log.error(f"Error while loading the agent model: {str(e)}")
        raise RuntimeError("Error while loading the agent model")


def initialize_agent(model, system_prompt, tools, checkpointer):
    """Function to create the Medical Agent with the specified model, system prompt, tools, and checkpointer."""
    try:
        agent = create_agent(
            model=model,
            system_prompt=system_prompt,
            tools=tools,
            checkpointer=checkpointer
        )
        log.info("Agent created successfully.")
        return agent
    except Exception as e:
        log.error(f"Error while creating the agent: {str(e)}")
        raise RuntimeError("Error while creating the agent")


def invoke_agent(user_query: str):
    """Function to invoke the Medical Agent with a user query and return the response."""
    checkpointer = InMemorySaver()
    model = load_agent_model()
    try:
        agent = initialize_agent(
            model=model,
            system_prompt=SYSTEM_PROMPT,
            tools=[retriever],
            checkpointer=checkpointer
        )
        config = {"configurable": {"thread_id": str(uuid1())}}
        log.info("Generating response.")
        response = agent.invoke(
            {
                "messages": [{
                    "role": "user",
                    "content": user_query
                }]
            },
            config=config
        )
        return response["messages"][-1].content
    
    except Exception as e:
        log.error(f"Error while generating the response: {str(e)}")
        raise RuntimeError("Error while generating the response")