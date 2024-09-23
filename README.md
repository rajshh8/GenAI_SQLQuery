- Refer GPTQuery.ipynb file for code base. 
- Refer docs link: https://platform.openai.com/docs/overview
- Below are the steps to build/finetune GEN AI application.

Data Preparation:
 1. Data was collected from various sources where SQL Query and questions are given.
 2. Prepared the data in json format where system message, user message(Natural Language) and assitant message(SQL Query) is present
 3. In system message database schema is been given.
 4. Conver the data into JSONL format further, as finetuning can be done in this data format only.

Fine Tuning:
  - Select a right LLM model based on your usecase. I chose GPT3.5 Turbo.
  - Fine tuning can be done through GUI or Python code, the code way is present in the GPTQuery.ipynb file.
  - Use OpenAI dashboard to play with you finetuned model, try several prompts in which your model can give best answers
  - Adjust parameters such as Temprature, Maximum tokens, Top P etc to get the most relevant answer.

Call your LLM Model:
  - Call your trained model using python code and pass the parameter that you decide in the above step.
  - Pass the message in System, User and assitant format and keep adding all the prmopts in a variable as mentioned in the GPTQuery.ipybn file
  -  Capture the output and display however and wherever you want to use.
    
