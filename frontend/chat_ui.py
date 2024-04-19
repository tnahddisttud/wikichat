import streamlit as st
import requests

INDEX_DATA_ENDPOINT = "http://localhost:8000/index_data"
CHAT_ENDPOINT = "http://localhost:8000/chat"

questions = [
    "What's your name?",
    "What is Artificial Intelligence?",
    "Who was Allan Turing?",
    "Define Computer Vision",
    "Tell me a joke",
    "What's the latest news?",
    "What are some other fields that AI draws upon?",
    "Explain automated decision making.",
    "Can you provide information on Natural language processing?"
]


# Function to create database
def create_database(input_url):
    response = requests.post(INDEX_DATA_ENDPOINT, json={"url": input_url})
    return response


# Function to interact with chatbot API
def interact_with_chatbot(prompt):
    response = requests.post(CHAT_ENDPOINT, json={"message": prompt})
    return response.json()['message']


st.set_page_config(
    page_title="WikiChat",
    page_icon="🤖")
st.title("WikiChat")

# Sidebar for creating database
with st.sidebar:
    st.title("Create Database:")
    url = st.text_input("Enter the URL", value='https://en.wikipedia.org/wiki/Artificial_intelligence')
    if st.button("Create"):
        create_response = create_database(url)
        if create_response.status_code == 201:
            st.success(create_response.text)
        else:
            st.error("Error creating database")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
selected_question = st.selectbox(label="Select a question", label_visibility="hidden", options=questions, index=None,
                                 placeholder="Select a question")
manual_question = st.chat_input("Or type your question here")
if selected_question and not manual_question:
    user_input = selected_question
else:
    user_input = manual_question

if user_input:
    st.chat_message("user").markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})
    bot_response = interact_with_chatbot(user_input)

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        st.markdown(bot_response)
    st.session_state.messages.append({"role": "assistant", "content": bot_response})
