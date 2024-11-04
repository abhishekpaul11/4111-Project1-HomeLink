from sqlalchemy import create_engine, text
from utils.tableDefs import users

from dotenv import load_dotenv
import os

# Load environment variables from the .env file
load_dotenv()

# Access the variables
db_user = os.getenv("DB_USER")
db_pass = os.getenv("DB_PASS")

# Connect to SQLite database (or another database by changing the connection string)
engine = create_engine(f'postgresql://{db_user}:{db_pass}@w4111.cisxo09blonu.us-east-1.rds.amazonaws.com/w4111', echo=True)


def runQuery(query:str, args:dict = {}):
    """
    Executes a given SQL query with the provided arguments.

    Parameters:
    query (str): The SQL query to be executed. (will be passed to text so make sure its parameterized)
    args (dict): A dictionary of arguments to be passed to the SQL query.

    Returns:
    ResultProxy: The result of the executed query.
    """
    with engine.connect() as conn:
        sql = text(query)
        results = conn.execute(sql, args)
        return results

def test():
    query = "select * from users limit 5"
    result = runQuery(query)
    for row in result:
        print((row[users["name"]], row[users["password"]]))
# ('Ella Mitchell', 'SunnyMeadow72')
# ('James Cox', 'OceanBreeze73')
# ('Olivia Diaz', 'MorningMist74')
# ('Benjamin Cooper', 'TwilightEchoes75')