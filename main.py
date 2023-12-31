from dotenv import load_dotenv          # Dotenv for loading environment variables.
import os                               # OS module for interacting with the operating system.
import streamlit as st                  # Streamlit library for creating web apps.
from streamlit_chat import message      # Streamlit's chat UI component.

# Import chat-related modules from LangChain.
from langchain_community.chat_models import ChatOpenAI
from langchain.schema import (
    SystemMessage,
    HumanMessage,
    AIMessage
)

def init():
    if not load_dotenv():
        print("Could not load .env file or it is empty. Please check if it exists and is readable.")
        exit(1)     # exit(0) : successful execution, exit(1) : some issue/error occurred while executing a program. 
        
    # Load the OpenAI API key from an environment variable.
    if os.getenv("OPENAI_API_KEY") is None or os.getenv("OPEN_API_KEY") == "":
        print(">> OPENAI_API_KEY is not set")
        exit(1)

    # Initialize the Streamlit session state to keep track of the messages.
    if "messages" not in st.session_state:
        st.session_state.messages = []
        
    if 'user_input' not in st.session_state:
        st.session_state.user_input = ""

# Clearing input field
def clear_text():
    global input_value
    input_value = st.session_state.user_input
    st.session_state.user_input = ""

def change_role_prompt(role):
    match role:
        case "Assistant":
            role_descr="You are a helpful assistant."
        case "Counselor":
            role_descr="You are a counselor who provides effective solutions to user's problem with an empathetic tone."
        case "Teacher":
            role_descr="You are an understanding teacher who explains concepts user asks about with easy explanations. If possible, give analogies or useful examples. "
        case "Artist":
            role_descr="You are a creative artist who provides innovative and creative ideas."
    return role_descr

def main():
    # Call the initialization function
    init()
    
    # Define Streamlit page configuration.
    st.set_page_config(
        page_title="Your own ChatGPT",  # Title of the page.
        page_icon="💬"                   # Icon of the page.
    )
        
    # Set up the header of the page.
    st.header("Your own ChatGPT 💬")
    
    # Provide options on sidebar
    with st.sidebar:
        show_message = st.radio(
            "Set a message visibility 👀",
            key="visibility",
            options=["hidden", "visible"],
            index=0,
        )
    
        role = st.radio(
            "Assign a role to the bot 🤖",
            key="role",
            options=["Assistant", "Counselor", "Teacher", "Artist"],
        )
        
        role_desc = st.text_area("role descr", value=change_role_prompt(role))
        
    st.text_input("Your message: ", on_change=clear_text(), key="user_input")
   
    # Create an instance of ChatOpenAI from LangChain
    chat = ChatOpenAI(temperature=0)  # Temperature parameter determines the creativity of the conversation.
   
    # Process the user's message.
    if input_value:

        st.session_state.messages.append(SystemMessage(content=role_desc))   
        st.session_state.messages.append(HumanMessage(content=input_value))  # Add the user's message to the session state.

        with st.spinner("Thinking..."):                                     # Show a spinner while waiting for a response.
            response = chat(st.session_state.messages)                      # Get a response from the LangChain chatbot.

        st.session_state.messages.append(AIMessage(content=response.content))  # Add the AI's response to the session state.

    # Iterate through the stored messages and display them on the screen.
    messages = st.session_state.get('messages', [])
    
    for i, msg in enumerate(messages):                                                  # Display all messages
        if i % 3 == 0:                                                          
            continue                                                                    # Do not display system messages. 
        elif i % 3 == 1:
            message(msg.content, is_user=True, key=str(i) + '_user')                    # Display user messages.
        else:
            message(msg.content, is_user=False, key=str(i) + '_ai', seed = role)        # Display AI messages.

    if show_message == "visible":
        st.write(messages)

if __name__ == '__main__':
    main()