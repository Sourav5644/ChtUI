# import streamlit as st
# from uibot_backend import chatbot
# from langchain_core.messages import HumanMessage
# import uuid

# # -----------------utility functions---------------------------------------

# def generate_thread_id():
#     thread_id=uuid.uuid4()
#     return thread_id


# def reset_chat():
#     thread_id=generate_thread_id()
#     st.session_state['thread_id']=thread_id
#     add_thread(st.session_state['thread_id'])
#     st.session_state['message_history']=[]

# def add_thread(thread_id):
#     if thread_id not in st.session_state['chat_threads']:
#         st.session_state['chat_threads'].append(thread_id)


# def load_conversation(thread_id):
#     return chatbot.get_state(config={'configurable':{'thread_id':thread_id}}).values['messages']




# # ----------------------session setup-----------------------------------------------

# if 'message_history' not in st.session_state:
#     st.session_state['message_history'] = []

# if 'thread_id' not in st.session_state:
#     st.session_state['thread_id']=generate_thread_id()

# if 'chat_threads' not in st.session_state:
#     st.session_state['chat_threads']=[]  
# add_thread(st.session_state['thread_id'])

# # --------------------------------side bar ui------------------------------------
# st.sidebar.title('Langgraph chatbot')
# if st.sidebar.button('New Chat'):
#     reset_chat()
# st.sidebar.header('My conversation')

# for thread_id in st.session_state['chat_threads'][::-1]:
#     if st.sidebar.button(str(thread_id)):
#         st.session_state['thread_id']=thread_id
#         messages=load_conversation(thread_id)

#         temp_message=[]

#         for msg in messages:
#             if isinstance(msg, HumanMessage):
#                 role='user'
#             else: 
#                 role='assistant' 
#             temp_message.append({'role':role,'content':msg.content})       
#         st.session_state['message_history']=temp_message



# # ------------------------main ui-------------------------------------------

# # loading the conversation history
# for message in st.session_state['message_history']:
#     with st.chat_message(message['role']):
#         st.text(message['content'])

# #{'role': 'user', 'content': 'Hi'}
# #{'role': 'assistant', 'content': 'Hi=ello'}

# user_input = st.chat_input('Type here')

# if user_input:

#     # first add the message to message_history
#     st.session_state['message_history'].append({'role': 'user', 'content': user_input})
#     with st.chat_message('user'):
#         st.text(user_input)



#     CONFIG = {'configurable': {'thread_id': st.session_state['thread_id']}}



#     # first add the message to message_history
#     with st.chat_message('assistant'):

#         ai_message = st.write_stream(
#             message_chunk.content for message_chunk, metadata in chatbot.stream(
#                 {'messages': [HumanMessage(content=user_input)]},
#                 config= CONFIG,
#                 stream_mode= 'messages'
#             )
#         )

#     st.session_state['message_history'].append({'role': 'assistant', 'content': ai_message})

import streamlit as st
from uibot_backend import chatbot
from langchain_core.messages import HumanMessage

# ----------------- Utility Functions -----------------------------------

def generate_chat_title(user_input):
    """Generate a short, user-friendly chat title from the first message"""
    return user_input[:30]  # first 30 characters

def reset_chat():
    """Reset current conversation"""
    st.session_state['message_history'] = []
    st.session_state['current_chat'] = None

def add_chat_title(chat_title):
    """Add chat title to session if not exists"""
    if chat_title not in st.session_state['chat_threads']:
        st.session_state['chat_threads'].append(chat_title)

def load_conversation(chat_title):
    """Load conversation messages from chatbot state"""
    messages = chatbot.get_state(config={'configurable': {'thread_id': chat_title}}).values['messages']
    temp_message = []
    for msg in messages:
        role = 'user' if isinstance(msg, HumanMessage) else 'assistant'
        temp_message.append({'role': role, 'content': msg.content})
    return temp_message

# ----------------- Session Setup ----------------------------------------

if 'message_history' not in st.session_state:
    st.session_state['message_history'] = []

if 'current_chat' not in st.session_state:
    st.session_state['current_chat'] = None

if 'chat_threads' not in st.session_state:
    st.session_state['chat_threads'] = []

