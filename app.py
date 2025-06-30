from langchain.chat_models import AzureChatOpenAI
import os
from dotenv import load_dotenv
import streamlit as st

# Load environment variables
load_dotenv()


st.title("My first Streamlit app with Azure OpenAI")
st.write("This is a simple app to interact with Azure OpenAI using Streamlit.")

llm = AzureChatOpenAI(
    openai_api_base=os.getenv("AZURE_OPENAI_API_BASE"),
    openai_api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
    openai_api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    deployment_name=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),
    model_name="gpt-4o",
    temperature=0.7,
)

queries = []
for i in range(1):
    query = st.text_input(f"Enter query {i+1}:", key=f"query_{i}")
    queries.append(query)

for i, query in enumerate(queries):
    if query:
        result = llm.invoke(query)
        st.write(f"**AI Response to Query {i+1}:** {result.content}")
        print("AI:", result.content)
        print("--------------------------------------------------")
