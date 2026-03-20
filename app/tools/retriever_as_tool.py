from app.utils import cfg, get_logger
from app.rag import Retrievers, retrievers
from langchain.tools import tool
from langchain_community.agent_toolkits import SQLDatabaseToolkit


log = get_logger(__file__)

@tool
def retriever_tool(query: str):
    """
    Retrieve relevant information from the database or knowledge base



    """
    try:
        result = retrievers.search_as_retriever(query=query)
        log.info("used retriever tool to retrieved data")
        return result
    except Exception as e:
        log.error(f"Error while using retriever tool: {str(e)}")
        return f"Error while using retriever tool, could not retrieve any data"









