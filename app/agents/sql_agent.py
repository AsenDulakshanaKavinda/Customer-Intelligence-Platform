from app.utils import cfg, get_logger
from app.agents.agent_class import AI_Agent

import os
from pydantic import BaseModel, Field
from langchain.chat_models import init_chat_model
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain_community.utilities import SQLDatabase

db_connection = os.getenv("DATABASE_CONNECTION")

log = get_logger(__file__)

db = SQLDatabase.from_uri(database_uri = db_connection)
model = init_chat_model(model = cfg.model.database_agent_model)
toolkit = SQLDatabaseToolkit(db = db, llm = model)
tools = toolkit.get_tools()


database_agent_system_prompt = """
You are an agent designed to interact with a SQL database.

1. You are acting on behalf of User ID: {user_id}.
2. Every SQL query you generate MUST include a WHERE clause filtering by 'owner_id' (e.g., WHERE owner_id = {user_id}).
3. Never show data where the owner_id does not match {user_id}.
4. If the user asks for "all items," only return "their" items.

Given an input question, create a syntactically correct {dialect} query to run,
then look at the results of the query and return the answer. Unless the user
specifies a specific number of examples they wish to obtain, always limit your
query to at most {top_k} results.

You can order the results by a relevant column to return the most interesting
examples in the database. Never query for all the columns from a specific table,
only ask for the relevant columns given the question.

You MUST double check your query before executing it. If you get an error while
executing a query, rewrite the query and try again.

DO NOT make any DML statements (INSERT, UPDATE, DELETE, DROP etc.) to the
database.

To start you should ALWAYS look at the tables in the database to see what you
can query. Do NOT skip this step.

Then you should query the schema of the most relevant tables.
"""

# .format(
#   dialect=db.dialect,
#     top_k=5,
# )

class DatabaseAgentOutputSchema(BaseModel):
    answer: str = Field(..., description="the answer to the user's question based on the query results")
    query: str = Field(..., description="the SQL query executed to obtain the answer")
    confident: float = Field(..., description="from 0 to 1, how confident the agent is that the answer is correct based on the query results and the question asked")

try:
    log.info("Initializing classification agent")
    database_agent = AI_Agent(
        name = "database_agent",
        model_name = cfg.models.database_agent_model,
        system_prompt = database_agent_system_prompt,
        tools = tools,
        output_schema = DatabaseAgentOutputSchema
    )
except Exception as e:
    log.error(f"Error in database agent {str(e)}")
    raise RuntimeError(f"Error in database agent: {str(e)}")

# todo - 
"""
# The variables passed here fill the {} in your system prompt
    return database_agent.invoke(
        user_query=question,
        user_id=user.id,        # Fills {user_id}
        dialect="sqlite",      # Fills {dialect}
        top_k=5                # Fills {top_k}
    )
"""