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

class Transaction:
    def __init__(self):
        self.conn = engine.connect()
    
    def runQuery(self, query:str, args:dict = {}):
        sql = text(query)
        results = self.conn.execute(sql, args)
        return results
    
    def commit(self):
        self.conn.commit()

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
        final_query = sql.bindparams(**args).compile(bind=engine, compile_kwargs={"literal_binds": True}) 
        print(final_query)
        results = conn.execute(sql, args)
        if query.strip().split()[0].lower() in ("delete", "insert", "update"):
            conn.commit()
        return results

def convert_to_dict(sql_result):
    """
    Converts the results of a query to a JSON format.

    Parameters:
    results (ResultProxy): The result of a query.

    Returns:
    list: A list of dictionaries, where each dictionary represents a row in the query result.
    """
    raw_results = sql_result.all()

    # Convert each row to a dictionary
    return [dict(row._mapping) for row in raw_results]

def test():
    query = "select * from users limit 5"
    result = runQuery(query)
    for row in result:
        print((row[users["name"]], row[users["password"]]))
# ('Ella Mitchell', 'SunnyMeadow72')
# ('James Cox', 'OceanBreeze73')
# ('Olivia Diaz', 'MorningMist74')
# ('Benjamin Cooper', 'TwilightEchoes75')