# InfoStream: Interactive Chatbot

## Overview
The **InfoStream: Interactive Chatbot** project showcases a dynamic chatbot that leverages Flask for backend interactions, a web interface for frontend interactions, and a Python-based external processing source for data aggregation through web scraping and API calls. This solution uses a unique architecture combining a real-time chat experience with external sources of information.

---

## Architecture

### 1. **Frontend (HTML/JS - `index4.html`)**

#### User Interaction
- **Chat Window:** Users can interact by typing messages or using a microphone for speech recognition.
- **Speech Recognition:** Utilizes `webkitSpeechRecognition` to capture spoken words and translate them to English via the `/translate` endpoint.

#### User Input Handling
- **Text Input:** Typed messages are sent using `fetch` as a `POST` request to the `/chatbot` endpoint.
- **Voice Input:** Captured speech is converted to text, sent to the `/translate` endpoint, and then forwarded to the bot.

---

### 2. **Backend (Flask Server - `app.py`)**

#### Handling User Messages - `/chatbot`
- **Predefined Responses:** The server checks for predefined messages (e.g., "hello", "bye"). If found, it sends a pre-configured response to the frontend.
- **External Query Handling:**
  - **No Match Found:** If no predefined response matches the user’s message, it is written to `message.txt` via the `send_message()` function.
  - **Waiting for External Source:** The backend waits for an external processing system to generate a response.

---

### 3. **External Processing Source (Python Script)**

#### Continuous Monitoring of `message.txt`
- **File Monitoring:** The script continuously monitors `message.txt` for new user queries.
- **Processing the Query:**
  - **Web Scraping & Data Aggregation:** Once a query is detected, a Bing Web Search API call is made, and relevant web content is scraped using `BeautifulSoup`.
  - **Response Generation:** The first 2000 characters of relevant content are compiled and written to `response.txt` using the `write_response()` function.

#### Regeneration Handling
- **User Feedback:** If the user requests regeneration (via feedback such as "Apologies, I will regenerate it!"), the script repeats the process, increasing the `top_k` value to fetch more web results.

---

### 4. **Backend (Flask Server) - Response Handling**

#### Polling for Response
- **Polling `response.txt`:** Flask continuously polls `response.txt` to check if the external system has generated a response.
- **Sending Response to Frontend:**
  - The bot response is read from `response.txt` using the `read_response()` function.
  - After sending the response to the frontend, both `message.txt` and `response.txt` are cleared to handle future queries properly.

---

### 5. **Frontend - Displaying Bot Response**

#### Receiving the Response
- The response is received from the Flask `/chatbot` endpoint in JSON format.

#### Displaying the Response
- The bot's response is displayed as a new message bubble in the chat window.
- **User Feedback:** The user can give a thumbs-up or thumbs-down. A negative response (thumbs-down) will resend the query for regeneration, restarting the cycle.

---

## Summary of Workflow

1. **User Interaction:** The user sends a message (via text or voice) through the chat interface.
2. **Backend Processing:** Flask checks for predefined responses. If none exist, the message is written to Google Drive (`message.txt`).
3. **External Processing:** An external script reads `message.txt`, processes the query through web scraping and API calls, and writes the response to `response.txt`.
4. **Backend Response:** Flask reads the generated response from `response.txt`, clears the files, and sends the response to the frontend.
5. **Frontend Display:** The bot's response is displayed. User feedback is incorporated, allowing for potential regeneration of the response.

---

