import time
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import os

# Authenticate and create the PyDrive client
gauth = GoogleAuth()
gauth.LocalWebserverAuth()  # Opens a window to authenticate with Google
drive = GoogleDrive(gauth)

# Function to find the message.txt file in Google Drive
def find_message_file():
    file_list = drive.ListFile({'q': "title='message.txt' and trashed=false"}).GetList()
    if file_list:
        return file_list[0]  # Assuming there's only one file named message.txt
    else:
        return None

# Function to find the response.txt file in Google Drive
def find_response_file():
    file_list = drive.ListFile({'q': "title='response.txt' and trashed=false"}).GetList()
    if file_list:
        return file_list[0]  # Assuming there's only one file named response.txt
    else:
        return None

# Function to send a message to Colab
def send_message(message, file):
    file.SetContentString(message)
    file.Upload()
    print("Sent message:", message)

# Function to read the message from message.txt
def read_message(file):
    file.FetchContent()
    message = file.GetContentString()
    return message.strip()

# Function to read the response from Colab
def read_response(file):
    file.FetchContent()
    response = file.GetContentString()
    return response.strip()

# Function to clear the message.txt file
def clear_message(file):
    file.SetContentString("")  # Set content to empty string
    file.Upload()

# Function to clear the response.txt file
def clear_response(file):
    file.SetContentString("")  # Set content to empty string
    file.Upload()

if __name__ == "__main__":
    message_file = find_message_file()
    response_file = find_response_file()
    clear_message(message_file)
    clear_response(response_file)

    if message_file and response_file:
        while True:
            # Ask for user input
            user_input = input("Enter your message ('exit' to quit): ")
            if user_input.lower() == 'exit':
                break

            # Send user input to Colab by writing to message.txt
            send_message(user_input, message_file)

            # Poll for response
            max_polls = 100  # Maximum number of polls
            poll_interval = 10  # Poll interval in seconds
            response = ""
            for _ in range(max_polls):
                response = read_response(response_file)
                if response:
                    break
                time.sleep(poll_interval)

            # Print the response from Colab
            print("Response:", response)

            # Clear the message and response after reading
            clear_message(message_file)
            clear_response(response_file)

    else:
        print("message.txt or response.txt file not found in Google Drive.")
