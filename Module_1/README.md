# Personal Website with AI Assistant

This is my personal website built with Flask for JHU EP 605.256 – Modern Software Concepts.

## Features

- Personal bio and professional information
- Project showcase
- Contact information
- Interactive AI assistant chatbot

## Setup Instructions

### Prerequisites

- Python 3.10 or higher
- OpenAI API key (for chatbot functionality)

### Installation

1. Clone the repository
2. Create a virtual environment:
    python -m venv venv
3. Activate the virtual environment:
- Windows: `venv\Scripts\activate`
- macOS/Linux: `source venv/bin/activate`
4. Install dependencies:
    pip install -r requirements.txt
5. Create a `.env` file in the project root (copy from `.env.example`):
    SECRET_KEY=your_secret_key_here

    OpenAI API Configuration
    OPENAI_API_KEY=your_api_key_here
    OPENAI_MODEL=gpt-3.5-turbo
    MAX_TOKENS_PER_REQUEST=150
6. Replace `your_api_key_here` with your actual OpenAI API key
7. Generate a random secret key (you can use `python -c "import secrets; print(secrets.token_hex(16))"`)

### Running the Application

Run the application with:
    python run.py

The website will be available at http://127.0.0.1:5000/

## Chatbot Functionality

The chatbot is powered by OpenAI's API and can:
- Answer questions about my background and skills
- Provide information about my projects
- Show my resume when requested

## Note for Instructors

To test the chatbot functionality, you'll need to:
1. Create a `.env` file as described above
2. Add your own OpenAI API key
3. Run the application

If you don't have an OpenAI API key, the chatbot will display a message indicating it's not configured.