from langgraph.graph import StateGraph,START,END
from typing import TypedDict
import os
from dotenv import load_dotenv
from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage, HumanMessage
from langgraph.checkpoint.memory import InMemorySaver

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

checkpointer=InMemorySaver()

graph=StateGraph(chatstate)
graph.add_node('chat_node',chat_node)
graph.add_edge(START,'chat_node')
graph.add_edge('chat_node',END)

chatbot=graph.compile(checkpointer=checkpointer)
