from langgraph.graph import StateGraph,START,END
from typing import TypedDict
import os
import sqlite3
from dotenv import load_dotenv
from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage, HumanMessage
from langgraph.checkpoint.sqlite import SqliteSaver

from langchain_groq import ChatGroq
from langchain.chat_models import init_chat_model
from dotenv import load_dotenv
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
llm =ChatGroq(model='llama-3.1-8b-instant')


from typing import Annotated
from typing_extensions import TypedDict



class chatstate(TypedDict):
    messages: Annotated[list[BaseMessage],add_messages]

def chat_node(state:chatstate):
    messages=state['messages']
    response=llm.invoke(messages)
    return {'messages':[response]}

conn=sqlite3.connect(database='chatbot.db',check_same_thread=False)

checkpointer=SqliteSaver(conn=conn)

graph=StateGraph(chatstate)
graph.add_node('chat_node',chat_node)
graph.add_edge(START,'chat_node')
graph.add_edge('chat_node',END)

chatbot=graph.compile(checkpointer=checkpointer)

def retrieve_all_threads():
    all_threads=set()
    for checkpoint in checkpointer.list(None):
        all_threads.add(checkpoint.config['configurable']['thread_id'])

    return list(all_threads)

# CONFIG = {'configurable': {'thread_id': 'thread-1'}}
# response=chatbot.invoke(
#                 {'messages': [HumanMessage(content='what is the capital of India. Acknowledge my name while answering')]},
#                 config= CONFIG
#             )
# print(response)    
    
