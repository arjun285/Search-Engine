import streamlit as st
from langchain_groq import ChatGroq
from langchain_community.utilities import ArxivAPIWrapper,WikipediaAPIWrapper
from langchain_community.tools import ArxivQueryRun,WikipediaQueryRun,DuckDuckGoSearchRun
from langchain.agents import initialize_agent,AgentType
from langchain.callbacks import StreamlitCallbackHandler
import os
from dotenv import load_dotenv
import warnings

###
api_wrapper_wiki=WikipediaAPIWrapper(top_k_results=1,doc_content_chars_max=250)
wiki=WikipediaQueryRun(api_wrapper=api_wrapper_wiki)

api_wrapper_arxiv=ArxivAPIWrapper(top_k_results=1,doc_content_chars_max=250)
arxiv=ArxivQueryRun(api_wrapper=api_wrapper_arxiv)


search=DuckDuckGoSearchRun(name="Search")


st.title("Search Engine with LangChain by Arjun")

"""Streamlit call back handler to display thoughts and actions"""

st.sidebar.title("Settings")
api_key=st.sidebar.text_input("Enter your Groq API information",type="password")

if "messages" not in st.session_state:
    st.session_state["messages"]=[{"role":"assistant","content":"I am a chatbot who can search the Web , How can I help you?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])
if api_key:
    if prompt:=st.chat_input(placeholder="what is Machine learning?"):
        st.session_state.messages.append({"role":"user","content":prompt})
        st.chat_message("user").write(prompt)

        llm=ChatGroq(groq_api_key=api_key,model="Llama3-8b-8192",streaming=True)
        tools=[search,arxiv,wiki]
        search_agent=initialize_agent(tools,llm,agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,handle_parsing_errors=True)

        with st.chat_message("assistant"):
            st_cb=StreamlitCallbackHandler(st.container(),expand_new_thoughts=False)
            response=search_agent.run(st.session_state.messages,callbacks=[st_cb])
            st.session_state.messages.append({"role":"assistant","content":response})
            st.write(response)
else:
    st.warning("please enter your API information")
