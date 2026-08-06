from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import StateGraph  , START , END
from dotenv import load_dotenv
from typing import TypedDict , Literal , Annotated
from math import sqrt
from pydantic import BaseModel , Field
from langchain_core.messages import BaseMessage, HumanMessage
from langgraph.graph import add_messages
from langgraph.checkpoint.sqlite import SqliteSaver
import sqlite3 
load_dotenv()

model = ChatGoogleGenerativeAI(model = "gemini-2.5-flash")

class LLMstate(TypedDict):
    messages : Annotated[list[BaseMessage] , add_messages]

def chat_node(state: LLMstate) :
    messages = state["messages"]
    response = model.invoke(messages)
    return {"messages":[response]}


conn = sqlite3.connect(database = "chatbot.db" , check_same_thread=False)

checkpointer = SqliteSaver(conn = conn)

graph = StateGraph(LLMstate)

graph.add_node("chat_node" , chat_node)

graph.add_edge(START , "chat_node")
graph.add_edge("chat_node" , END)

workflow = graph.compile(checkpointer = checkpointer)

####test

CONFIG = {'configurable': {'thread_id': 'thread-1'}}

response = workflow.invoke(
    {'messages': [HumanMessage(content='what is my name?')]},
    config = CONFIG
)

print(response)

# stream = workflow.stream(
#     {"messages":[HumanMessage(content ='what is STreaming')]},
#     config = {'configurable':{"thread_id":'1'}},
#     stream_mode = "messages"
# )

# for message_chunk , metadata in stream:
#     if message_chunk.content:
#         print(message_chunk.content , flush = False)