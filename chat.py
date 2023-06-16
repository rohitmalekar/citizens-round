import os
import streamlit as st
os.environ['OPENAI_API_KEY'] = st.secrets['OPENAI_API_KEY']

import streamlit as st
from langchain.llms import OpenAI
from llama_index import StorageContext, load_index_from_storage, GPTVectorStoreIndex, SimpleDirectoryReader, LLMPredictor, ServiceContext, Prompt

# set the model and parameters
llm_predictor = LLMPredictor(llm=OpenAI(model_name='text-davinci-003', temperature=0))
service_context = ServiceContext.from_defaults(
  llm_predictor=llm_predictor
)

# custom prompt
template = (
    "We have provided context information below. \n"
    "---------------------\n"
    "{context_str}"
    "\n---------------------\n"
    "If the question includes the name of the grantee, then append their grantee website URL and their Twitter handle at the end of the response.\n"
    "Do not respond to questions that ask to sort or rank grantees. Do not respond to questions that ask to compare \
    grantees. Similarly, do not respond to questions that ask for advise on which grantee to donate contributions to. \
    Few examples of such questions are (a) Which grantee had most impact on Gitcoin? (b) Who should I donate to \
    (c) Rank the grantees by impact (d) Compare work of one grantee versus another \
    For such questions, do not share any grantee information and just say: Dear human, I am told not to influence you with my biases for such queries. \
    The burden of choosing the public greats and saving the future of your kind lies on you. Choose well! \n"
    "Given this information, please answer the question: {query_str}\n" 
)
qa_template = Prompt(template)

# load from disk
#index = GPTVectorStoreIndex.load_from_disk('index.json')
index = load_index_from_storage(StorageContext.from_defaults(persist_dir="./storage"))
query_engine = index.as_query_engine(service_context=service_context, text_qa_template=qa_template)

st.title("Gitcoin Citizens Round")
st.markdown("Hi there! 👋 [The Gitcoin Citizens Round](https://gov.gitcoin.co/t/rewarding-the-community-gitcoin-citizen-round-1/14905) aims to reward people and grassroots projects \
            that have contributed to Gitcoin’s success, specifically by engaging with the wider ecosystem and community")
st.markdown("Gitcoin Citizens Round #1 is **[live](https://explorer.gitcoin.co/#/round/10/0x984e29dcb4286c2d9cbaa2c238afdd8a191eefbc)**! \
            Donations open until June 27th 23:59 UTC")
st.markdown("Below, you'll find some links that can give you more information about the grantees on Explorer. \
            And if you have any questions about the Round or the impact that grantees have made, feel free to ask away! 🙌")

col1, col2, col3 = st.columns(3)

with col1:
  st.markdown("[40acres DAO](https://explorer.gitcoin.co/#/round/10/0x984e29dcb4286c2d9cbaa2c238afdd8a191eefbc/0x984e29dcb4286c2d9cbaa2c238afdd8a191eefbc-57)")
  st.markdown("[All for Climate DAO](https://explorer.gitcoin.co/#/round/10/0x984e29dcb4286c2d9cbaa2c238afdd8a191eefbc/0x984e29dcb4286c2d9cbaa2c238afdd8a191eefbc-53)")

with col2:
  st.markdown("[40acres DAO](https://explorer.gitcoin.co/#/round/10/0x984e29dcb4286c2d9cbaa2c238afdd8a191eefbc/0x984e29dcb4286c2d9cbaa2c238afdd8a191eefbc-57)")
  st.markdown("[All for Climate DAO](https://explorer.gitcoin.co/#/round/10/0x984e29dcb4286c2d9cbaa2c238afdd8a191eefbc/0x984e29dcb4286c2d9cbaa2c238afdd8a191eefbc-53)")

with col3:
  st.markdown("[40acres DAO](https://explorer.gitcoin.co/#/round/10/0x984e29dcb4286c2d9cbaa2c238afdd8a191eefbc/0x984e29dcb4286c2d9cbaa2c238afdd8a191eefbc-57)")
  st.markdown("[All for Climate DAO](https://explorer.gitcoin.co/#/round/10/0x984e29dcb4286c2d9cbaa2c238afdd8a191eefbc/0x984e29dcb4286c2d9cbaa2c238afdd8a191eefbc-53)")

question = st.text_input("", placeholder="Enter your question here")

if question != "":
    response = query_engine.query(question)
    display = "\n" + str(response) + "\n"
    st.markdown(display)
    st.markdown(llm_predictor.last_token_usage)
