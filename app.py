import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import os
load_dotenv()
API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=API_KEY)


def generate_response(message):
    # Call the fine-tuned GPT-3.5 model
    response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=message,
                temperature=0.2,
                max_tokens=128,
                top_p=1,
            )

    return response.choices[0].message.content

def main():
    st.image("Citigroup-Logo.png", width=170) 
    st.title("CitiSQL Assistant")

    # Set your OpenAI API key
    
    schema='''Employees table CREATE TABLE Employees ( employee_id INT PRIMARY KEY, first_name VARCHAR(50), last_name VARCHAR(50),email VARCHAR(100), phone_number VARCHAR(20), hire_date DATE, job_id INT, salary DECIMAL(10, 2), commission_pct DECIMAL(4, 2), manager_id INT, department_id INT ); -- Departments table CREATE TABLE Departments ( department_id INT PRIMARY KEY, department_name VARCHAR(100), manager_id INT, location_id INT ); -- Locations table CREATE TABLE Locations ( location_id INT PRIMARY KEY, street_address VARCHAR(255), postal_code VARCHAR(20), city VARCHAR(100), state_province VARCHAR(100), country_id INT ); -- Countries table CREATE TABLE Countries ( country_id INT PRIMARY KEY, country_name VARCHAR(100), region_id INT ); -- Regions table CREATE TABLE Regions ( region_id INT PRIMARY KEY, region_name VARCHAR(100) ); -- Job_history table CREATE TABLE Job_history ( employee_id INT, start_date DATE, end_date DATE, job_id INT, department_id INT ); -- Jobs table CREATE TABLE Jobs ( job_id INT PRIMARY KEY, job_title VARCHAR(100), min_salary DECIMAL(10, 2), max_salary DECIMAL(10, 2) );" '''
    base_prompt='''You are an helpful assistant that is an expert in generating SQL queries. Having the access to database content, Generate information about the database content, generate a correct SQL query for the given question and also generate synthetic data based on the below database content. Also, while generating sythetic data return the data in a tabular format only.
                    Database content:{0}
                '''


    system_prompt = base_prompt.format(schema)
    # print(system_prompt)

    message=[
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": "Show me your schema in tabular format. Dont show the data types and constraints."}
    ]
    response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=message,
                    temperature=0.2,
                    max_tokens=256,
                    top_p=1,
                ) 
    response=response.choices[0].message.content
    st.write(response)
    message.append({"role": "assistant", "content": response})
    
    # # User input
    # user_message = st.chat_input("Enter your message:")
    user_message = st.chat_input("Say what you need—no SQL knowledge required!")
    
    if user_message:
        with st.chat_message("user"):        
            st.write(user_message)
            message.append({"role": "user", "content": user_message})

        if user_message:
            # Generate model response
            response = generate_response(message)
            # st.success("Model Response:")

            with st.chat_message("assistant"):
                st.write(response)

            # response=completion.choices[0].message.content
            message.append({"role": "assistant", "content": response})
        else:
            st.warning("Please enter a message to get a response.")


if __name__ == "__main__":
    main()
