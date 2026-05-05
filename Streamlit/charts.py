import streamlit as st
import snowflake.connector
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import numpy as np
import requests, pathlib, os
from dotenv import load_dotenv


# env_path = pathlib.Path('.') / '.env'
# load_dotenv(dotenv_path=env_path)


def get_charts():
    conn_params = {
        'user': os.getenv('user_login_name'),
        'password': os.getenv('password_snowflake'),
        'account': os.getenv('account_identifier'),
        'warehouse': os.getenv('warehouse_name'),
        'database': os.getenv('database_name'),
        'schema': os.getenv('schema_name')
    }
    conn = snowflake.connector.connect(**conn_params)
    st.set_option('deprecation.showPyplotGlobalUse', False)
    
    def execute_query(query):
        with snowflake.connector.connect(**conn_params) as connection:
            with connection.cursor() as cursor:
                cursor.execute(query)
                result = cursor.fetchall()
        return result
    
    # Chart 1
    query = """
    SELECT
        PLATFORM_NAME,
        SUM(SUM_IMPRESSIONS) AS total_impressions,
        SUM(ENGAGEMENTS) AS total_engagements
    FROM
        TEAM2_DB.ANALYTICS.SPONSOR_EXPOSURE
    GROUP BY
        PLATFORM_NAME;
    """
    result = execute_query(query)
    df = pd.DataFrame(result, columns=['Platform', 'Impressions', 'Engagements'])
    df_long = pd.melt(df, id_vars=['Platform'], var_name='Metric', value_name='Value')
    st.title("Total Engagements and Impressions by Platform")
    fig1 = px.bar(df_long, x='Platform', y='Value', color='Metric', barmode='group')
    st.plotly_chart(fig1)
    
    
    # Chart 2
    query2 = """
    SELECT
        c.state,
        SUM(s.ENGAGEMENTS) AS TOTAL_ENGAGEMENTS
    FROM
        TEAM2_DB.ANALYTICS.CONSUMER_DATA c
    JOIN
        TEAM2_DB.ANALYTICS.SPONSOR_EXPOSURE s ON c.STATE = s.STATE_CODE
    GROUP BY
        c.state;
    """
    result2 = execute_query(query2)
    df2 = pd.DataFrame(result2, columns=['STATE', 'TOTAL_ENGAGEMENTS'])
    st.title("ENGAGEMENTS Count by State")
    st.line_chart(df2.set_index('STATE'))
    
    
    # Chart 3
    query_app_usage = """
    SELECT
        STATE,
        AVG(AGE) AS avg_age,
        SUM(DURATION_SEC)/(60*60) AS TOTAL_TIME_IN_HOURS
    FROM
        TEAM2_DB.ANALYTICS.PANELIST_APP_USAGE
    GROUP BY
        STATE;
    """
    result_app_usage = execute_query(query_app_usage)
    df_app_usage = pd.DataFrame(result_app_usage, columns=['STATE', 'AGE', 'TOTAL_TIME_IN_HOURS'])
    st.title("Average Age vs. Total Duration by State")
    fig2 = px.scatter(df_app_usage, x='AGE', y='TOTAL_TIME_IN_HOURS', color='STATE')
    st.plotly_chart(fig2)
    
    #Chart 4
    query_sponsorship_nfl = """
    SELECT
        TEAM_NAME,
        SUM(SUM_IMPRESSIONS) AS total_impressions,
        SUM(ENGAGEMENTS) AS total_engagements
    FROM
        TEAM2_DB.ANALYTICS.SPONSOR_EXPOSURE
    GROUP BY
        TEAM_NAME;
    """
    result_sponsorship_nfl = execute_query(query_sponsorship_nfl)
    df_sponsorship_nfl = pd.DataFrame(result_sponsorship_nfl, columns=['Team_name', 'Total_impressions', 'total_engagements'])
    conn.close()
    st.title("Total Impressions by NFL Team")
    fig3 = px.pie(df_sponsorship_nfl, names='Team_name', values='Total_impressions')
    st.plotly_chart(fig3)
    