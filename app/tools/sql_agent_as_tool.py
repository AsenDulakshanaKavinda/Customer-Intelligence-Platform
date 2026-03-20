from app.utils import cfg, get_logger
from app.agents import sql_agent

from langchain.tools import tool

from typing import Dict

log = get_logger(__file__)

@tool
def sql_tool(agent_state: Dict):
    """
    Executes natural language queries against the SQL database to retrieve structured data.
    
    Use this tool when you need to answer questions involving:
    - Quantitative data (counts, sums, averages)
    - Relationships between entities (users, orders, products, etc.)
    - Real-time status updates from the database
    
    The input should be the current 'agent_state' containing the user's question.
    Returns a structured query results or if tool failed the error message.
    """

    try:
        response = sql_agent.invoke({
            "messages": [{"role": "user", "content": agent_state["question"]}]
        })

        if not response:
            log.error("SQL agent returned an empty structured response")
            raise ValueError("SQL agent returned an empty structured response")

        log.info("SQL agent invoked in the node")
        return response

    except Exception as e:
        log.error(f"SQL agent failed: {str(e)}")
        return "SQL agent failed"
