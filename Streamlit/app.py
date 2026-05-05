import streamlit as st, pandas as pd, numpy as np, ast
from langchain.utilities import SQLDatabase
from langchain.llms import OpenAI
from langchain_experimental.sql import SQLDatabaseChain
from langchain.chat_models import ChatOpenAI
from langchain.chains import create_sql_query_chain
from charts import get_charts


from langchain.utilities import SQLDatabase
from langchain.llms import OpenAI
from langchain_experimental.sql import SQLDatabaseChain
from langchain.chat_models import ChatOpenAI
from langchain.chains import create_sql_query_chain

import requests, pathlib, os
from dotenv import load_dotenv


# env_path = pathlib.Path('.') / '.env'
# load_dotenv(dotenv_path=env_path)

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
user_login_name = os.getenv('user_login_name')
password = os.getenv('password')
account_identifier = os.getenv('account_identifier')
database_name = os.getenv('database_name')
schema_name = os.getenv('schema_name')
warehouse_name = os.getenv('warehouse_name')
role_name = os.getenv('role_name')



def build_query_chain(dialect, table_info, few_shot_examples, user_question):

    few_shot_examples_str = "\n".join(
        [f"Question: \"{example['question']}\"\nSQLQuery: \"{example['query']}\"\n" for example in few_shot_examples]
    )

    prompt = create_prompt(user_question, few_shot_examples_str, table_info, dialect)

    # Create a SQL query chain
    chain = create_sql_query_chain(ChatOpenAI(temperature=0, openai_api_key=OPENAI_API_KEY), st.session_state['db'])
    response = chain.invoke({"question": prompt})
    return response

def create_prompt(input_text, examples_text, table_info, dialect):
    template = """
    Given an input question, first create a syntactically correct {dialect} query to run, then look at the results of the query and return the answer.
    Use the following format:

    Question: "{input_text}"
    SQLQuery: "SQL Query to run"
    SQLResult: "Result of the SQL Query"
    Answer: "Final answer here"

    Only use the following tables:

    {table_info}.

    Some examples of SQL queries that correspond to questions are:

    {few_shot_examples}
        """
    return template.format(input_text=input_text, few_shot_examples=examples_text, table_info=table_info, dialect=dialect)


def load_adhoc_query_configs():
    db = SQLDatabase.from_uri(f"snowflake://{user_login_name}:{password}@{account_identifier}/{database_name}/{schema_name}?warehouse={warehouse_name}&role={role_name}")
    dialect = "SQL"
    table_info = ''
    for table_name in ['CONSUMER_DATA', 'PANELIST_APP_USAGE', 'SPONSORSHIP_APPUSAGES_CORR', 'SPONSOR_EXPOSURE']:
        table_info = table_info + table_name + " schema :" + db.run(f"SELECT COLUMN_NAME, DATA_TYPE FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '{table_name}'") + ". \n"
    print(table_info)
    few_shot_examples = [
        {"question": "Display all rows in Consumer table", "query": "SELECT * FROM CONSUMER_DATA;"},
        {"question": "Display all rows in app usage table", "query": "SELECT * FROM PANELIST_APP_USAGE;"},
        {"question": "Display all rows in Sponser - app usages correlation table", "query": "SELECT * FROM SPONSORSHIP_APPUSAGES_CORR;"},
        ]
    
    return db, dialect, table_info, few_shot_examples

def adhoc_query_page():
    st.title('Welcome to NFL Sponsor Performance Analysis')
    st.write('What would you like to know about the data')
    if 'table_info' not in st.session_state:
        st.session_state['db'], st.session_state['dialect'], st.session_state['table_info'], st.session_state['few_shot_examples'] = load_adhoc_query_configs()

    st.session_state['user_query'] = st.text_input("Enter the question you want to ask", key="query_input")

    if st.button("Get Query"):
        if 'user_modified_question' in st.session_state:
            del st.session_state['user_modified_question'] 
        st.session_state['user_response'] = build_query_chain(st.session_state['dialect'], st.session_state['table_info'], st.session_state['few_shot_examples'], st.session_state['user_query'])
        print(st.session_state['user_response'])

    st.session_state['user_modified_question']  = st.text_area("Modify the question", value=st.session_state.get('user_response', ''))

    if hasattr(st.session_state, 'user_query') and st.session_state['user_query'] != '':
        try:   
            if st.button("Execute Query") :
                query_response= st.session_state['db'].run(st.session_state['user_modified_question'])
                df = pd.DataFrame(ast.literal_eval(query_response))
                st.dataframe(df)
        except Exception as e:
            error_message = "⚠️ Oops! Something went wrong with the query."
            st.write(error_message)
        
    if st.button("Return Home"):
        st.session_state['page'] = 'landing' 
        st.rerun()  
        
def charts_page():
    get_charts()
    if st.button("Return Home"):
        st.session_state['page'] = 'landing' 
        st.rerun()  

def landing_page():
    if 'user_query' in st.session_state:
        del st.session_state['user_query']
    st.title('Welcome to NFL Sponsor Performance Analysis')
    
    st.write("What would you like to do today")
    if st.button('See general analysis and dashboards'):
        st.session_state['page'] = 'charts' 
        st.rerun()    
    if st.button('Run adhoc queries'):
        st.session_state['page'] = 'adhoc_query' 
        st.rerun()  

def main():
    if 'page' not in st.session_state:
        st.session_state['page'] = 'landing'    
    if st.session_state['page'] == 'landing':
        landing_page()
    elif st.session_state['page'] == 'charts':
        charts_page()
    elif st.session_state['page'] == 'adhoc_query':
        adhoc_query_page()

if __name__ == '__main__':
    main()
