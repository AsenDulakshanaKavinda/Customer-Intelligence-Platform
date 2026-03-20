
from app.schemas import AgentState
from langgraph.graph import StateGraph, START, END





agent_builder = StateGraph(AgentState)

# add nodes
agent_builder.add_node("router_node", )