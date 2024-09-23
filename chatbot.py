import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import os
load_dotenv()
API_KEY = os.getenv("OPENAI_API_KEY")

schema='''Employees table CREATE TABLE Employees ( employee_id INT PRIMARY KEY, first_name VARCHAR(50), last_name VARCHAR(50),email VARCHAR(100), phone_number VARCHAR(20), hire_date DATE, job_id INT, salary DECIMAL(10, 2), commission_pct DECIMAL(4, 2), manager_id INT, department_id INT ); -- Departments table CREATE TABLE Departments ( department_id INT PRIMARY KEY, department_name VARCHAR(100), manager_id INT, location_id INT ); -- Locations table CREATE TABLE Locations ( location_id INT PRIMARY KEY, street_address VARCHAR(255), postal_code VARCHAR(20), city VARCHAR(100), state_province VARCHAR(100), country_id INT ); -- Countries table CREATE TABLE Countries ( country_id INT PRIMARY KEY, country_name VARCHAR(100), region_id INT ); -- Regions table CREATE TABLE Regions ( region_id INT PRIMARY KEY, region_name VARCHAR(100) ); -- Job_history table CREATE TABLE Job_history ( employee_id INT, start_date DATE, end_date DATE, job_id INT, department_id INT ); -- Jobs table CREATE TABLE Jobs ( job_id INT PRIMARY KEY, job_title VARCHAR(100), min_salary DECIMAL(10, 2), max_salary DECIMAL(10, 2) );" '''
base_prompt='''You are an helpful assistant that is an expert in generating SQL queries. Having the access to database content, Generate information about the database content, generate a correct SQL query for the given question and also generate synthetic data based on the below database content. Also, while generating sythetic data return the data in a tabular format only.
                Database content:{0}
                If you are not sure about the accuracy of the SQL Query, just respond that “Please provide detailed information for precise sql query.”'''


system_prompt = base_prompt.format(schema)

message=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": "Tell me about your tables and their column name you have."}
        ]

with st.sidebar:
    openai_api_key = st.text_input("OpenAI API Key", key=API_KEY, type="password")
    "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"
    "[View the source code](https://github.com/streamlit/llm-examples/blob/main/Chatbot.py)"
    "[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/streamlit/llm-examples?quickstart=1)"

st.title("💬 Chatbot")

if "messages" not in st.session_state:
    st.session_state["messages"] = message

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    if not openai_api_key:
        st.info("Please add your OpenAI API key to continue.")
        st.stop()

    client = OpenAI(api_key=openai_api_key)
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    response = client.chat.completions.create(model="gpt-3.5-turbo", messages=st.session_state.messages)
    msg = response.choices[0].message.content
    st.session_state.messages.append({"role": "assistant", "content": msg})
    st.chat_message("assistant").write(msg)