from flask import Flask, request, jsonify, send_from_directory
from integration import send_message, read_response, clear_message, clear_response, find_message_file, find_response_file
import time

app = Flask(__name__)

# Sample predefined responses for specific queries
responses = {
    "hello": "Hello! How are you?",
    "how are you": "I'm doing well, thank you!",
    "bye": "Goodbye! Have a great day!",
    "can you help me with a scheme information": "which scheme?"
}

@app.route('/')
def home():
    return send_from_directory('.', 'index4.html')

@app.route('/chatbot', methods=['POST'])
def chatbot():
    data = request.json
    user_message = data['message'].lower()  # Convert message to lowercase for case-insensitive matching

    # Check if the user's message matches any predefined query
    if user_message in responses:
        response = responses[user_message]
    else:
        # Send user message to message.txt
        message_file = find_message_file()
        if message_file:
            send_message(user_message, message_file)
        else:
            return jsonify({"response": "message.txt not found in Google Drive"})

        # Wait indefinitely for response from response.txt
        while True:
            response = read_response(find_response_file())
            if response:
                break

    # Clear message and response files after reading
    clear_message(find_message_file())
    clear_response(find_response_file())

    # Return the bot's response as a JSON object
    return jsonify({"response": response})



@app.route('/get_logo')
def get_logo():
    return send_from_directory('static', 'logo4.png')

if __name__ == '__main__':
    app.run()
