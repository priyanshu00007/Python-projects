import streamlit as st
import socketio

# Connect to the SocketIO server
sio = socketio.Client()

# Function to handle incoming messages
@sio.on('message')
def on_message(data):
    st.session_state.chat_history.append(data)
    st.experimental_rerun()

# Function to connect to the server
def connect():
    sio.connect('http://localhost:5000')
    sio.emit('message', f"{st.session_state.username} has joined the chat.")

# Set up Streamlit UI
st.title("Real-Time Chat App")

if 'username' not in st.session_state:
    st.session_state.username = st.text_input("Enter your name", "")
    if st.button("Join Chat"):
        st.session_state.chat_history = []
        connect()

else:
    st.write(f"Welcome, {st.session_state.username}!")

    # Display chat history
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []

    st.write("Chat history:")
    for message in st.session_state.chat_history:
        st.write(message)

    # Input field for the chat message
    message = st.text_input("Type your message:")
    if st.button("Send"):
        sio.emit('message', f"{st.session_state.username}: {message}")
