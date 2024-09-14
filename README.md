# Intelligent QA System with Real-Time Communication

This project implements an intelligent Question Answering (QA) system that interacts with users through a live chat interface. The system uses a combination of language models and speech processing to provide text and voice-based responses.

## Tech Stack

- **Libraries/Models**: HuggingFace, OpenAI, Gemini, etc.
- **Speech Processing**: whisper, gTTS, SpeechRecognition
- **SocketIO**: Flask-SocketIO for real-time communication

## Setup and Running Instructions

### Prerequisites

- Python 3.9 or higher
- Flask
- Flask-SocketIO
- HuggingFace Transformers
- OpenAI API
- gTTS

### Installation

1. **Clone the repository:**
    ```bash
    git clone https://github.com/yourusername/qa-system.git
    cd qa-system
    ```

2. **Create a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install the required packages:**
    ```bash
    pip install -r requirements.txt
    ```

### Running the Application

1. **Start the Flask application:**
    ```bash
    python main.py
    ```

2. **Access the application:**
    Open your web browser and go to `http://127.0.0.1:5000`.

### File Structure

- `main.py`: Main Flask application file that sets up routes and SocketIO events.
- `main_rag.py`: Contains functions for generating text from the language model and converting text to speech.
- `templates/`: Contains HTML templates for the web interface.
- `static/css/style.css`: Contains CSS styles for the web interface.

### Folder Structure
```
system/
├── flagged
├── Output
│   └── audio.wav
├── main_rag.py
├── main.py
├── templates/
│   ├── base.html
│   ├── home.html
│   └── room.html
├── static/
│   └── css/
│       └── style.css/
```
### Explanation of the Models and Libraries Used

- **HuggingFace Transformers**: Used for implementing the language model to generate text responses.
- **OpenAI API**: Used for accessing advanced language models like GPT-3.
- **gTTS (Google Text-to-Speech)**: Used for converting text responses to speech.
- **Flask-SocketIO**: Used for real-time communication between the client and server.

### Features

- **Real-Time Chat**: Users can interact with the system in real-time using text messages.
- **Voice Responses**: The system can convert text responses to speech and play them back to the user.
- **Room Management**: Users can create or join chat rooms using unique room codes.

### Usage

1. **Enter the Chat Room**: Provide your name and a room code to join an existing room or create a new one.
2. **Send Messages**: Type your message and send it to the chat. The system will respond with text and optionally with voice.
3. **Voice Responses**: Click the "Speak" button next to the system's response to hear the voice output.

### Troubleshooting

- **Dependencies**: Ensure all required packages are installed. Use `pip install -r requirements.txt` to install them.
- **Server Issues**: Make sure the Flask server is running and accessible at `http://127.0.0.1:5000`.
- **Audio Playback**: Ensure your browser supports audio playback and that your system's audio settings are correctly configured.

### Contributing

Feel free to fork this repository and contribute by submitting pull requests. For major changes, please open an issue first to discuss what you would like to change.

### License

This project is licensed under the MIT License. See the `LICENSE` file for details.
