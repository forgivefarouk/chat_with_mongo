import streamlit as st
from dotenv import load_dotenv
from pymongo import MongoClient
import urllib,io,json
from langchain_openai import ChatOpenAI
from langchain_cohere.llms import Cohere
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

from utilities import vector_search

load_dotenv()
#llm =Cohere(temperature=0.0)
llm=ChatOpenAI(model="gpt-3.5-turbo",temperature=0.0)
#mongo client
user_pwd="sameh:ZbsjcRsux5ri2zGM"
#user_pwd=""
database_address = "cluster0.t54bdbq.mongodb.net"
#database_address = "192.168.1.119"

client = MongoClient(f"mongodb+srv://{user_pwd}@{database_address}/?retryWrites=true&w=majority&appName=Cluster0")
db = client['stations']
collection = db["5"]

st.title("talk to MongoDB")
st.write("ask anything and get answer")
input=st.text_area("enter your question here")


prompt ='''

please extract the answer from this document {document} and please note that 
"
generators == المولدات
transformers == المحولات
ele panel or ele or electrical panel == وحدات التحكم
Not working == لا تعمل == مش شغاله == عطلان
"

question : {question}
answer:

'''

query_with_prompt=PromptTemplate(
    template=prompt,
    input_variables=["document","question"]
)
llmchain=LLMChain(llm=llm,prompt=query_with_prompt,verbose=True)

if input is not None:
    button=st.button("Submit")
    if button:
        result = vector_search(input,collection)
        response= llmchain.invoke({
            "question":input,
            "document":result
        })
        
        st.write(response)