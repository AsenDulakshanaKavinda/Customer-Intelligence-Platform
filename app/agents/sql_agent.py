from app.utils import cfg, get_logger

import os
from langchain.chat_models import init_chat_model
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain_community.utilities import SQLDatabase
from langchain.agents import create_agent

from dotenv import load_dotenv; load_dotenv()
os.environ["MISTRAL_API_KEY"] = os.getenv("MISTRAL_API_KEY")
db_connection = os.getenv("DATABASE_CONNECTION")

log = get_logger(__file__)
db = SQLDatabase.from_uri(database_uri = db_connection)
model = init_chat_model(model = 'mistral-large-latest')
toolkit = SQLDatabaseToolkit(db = db, llm=model)
tools = toolkit.get_tools()

sql_agent_system_prompt = """
You are an agent designed to interact with a SQL database.
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
""".format(
    dialect=db.dialect,
    top_k=5,
)

try:
    sql_agent = create_agent(
        model = model,
        tools = tools,
        system_prompt = sql_agent_system_prompt
    )
    log.info("SQL agent initialized")

except Exception as e:
    log.error(f"Error while initializing the SQL agent: {str(e)}")  
    raise RuntimeError("Error while initializing the SQL agent")  