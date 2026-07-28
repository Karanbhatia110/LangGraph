from langchain_core.messages import HumanMessage , AIMessage
import streamlit as st
from backend import workflow
import uuid


def generate_thread_id():
    thread_id = uuid.uuid4()
    return thread_id

def reset_chat():
    thread_id = generate_thread_id()
    st.session_state['thread_id'] = thread_id
    st.session_state["message_history"] = []

if 'message_history' not in st.session_state:
    st.session_state['message_history'] = []

if 'thread_id' not in st.session_state:
    st.session_state['thread_id'] = generate_thread_id()

CONFIG = {'configurable':{'thread_id': st.session_state['thread_id']}}

if 'message_history' not in st.session_state:
    st.session_state['message_history'] = []

####sidebar

st.sidebar.title("LangGraph ChatBot")

if st.sidebar.button("New Chat"):
    reset_chat()

st.sidebar.header("My Conversation")

st.sidebar.text(st.session_state['thread_id'])


for message in st.session_state['message_history']:
    with st.chat_message(message['role']):
        st.text(message['content'])

user_input = st.chat_input('Enter')

if user_input:
    st.session_state['message_history'].append({'role': 'user' , 'content': user_input})
    with st.chat_message('user'):
        st.text(user_input)

    # response = workflow.invoke({'messages': HumanMessage(content = user_input)}, config = CONFIG)

    # ai_message = response['messages'][-1].content

    with st.chat_message('assistant'):

        ai_message = st.write_stream(
            message_chunk.text for message_chunk, metadata in workflow.stream(
                {'messages': [HumanMessage(content=user_input)]},
                config= CONFIG,
                stream_mode= 'messages'
            )
        )

    st.session_state['message_history'].append({'role': 'assistant', 'content': ai_message})