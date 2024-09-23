from flask import Flask, render_template
from flask_socketio import SocketIO, send

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

# Store chat history
chat_history = []

@app.route('/')
def index():
    return "Chat Server is Running"

# Handle incoming messages from clients
@socketio.on('message')
def handle_message(msg):
    print(f"Message: {msg}")
    chat_history.append(msg)
    send(msg, broadcast=True)  # Broadcast the message to all connected clients

if __name__ == '__main__':
    socketio.run(app, host="0.0.0.0", port=5000)
