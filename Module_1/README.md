# Kyle Woolford's Personal Website

A Flask-based personal website with an OpenAI-powered chatbot assistant.

## Quick Setup

### Prerequisites
- Python 3.10+
- OpenAI API key

### Installation

1. **Clone and navigate to the repository**
   ```bash
   git clone https://github.com/kwoolford25/jhu_software_concepts.git
   cd jhu_software_concepts/Module_1

2. **Set up a Python environment**
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    pip install -r requirements.txt

3. **Configure environment variables**
    Create a .env file with the format of .envsample
    FLASK_SECRET_KEY=(Generate with python -c "import secrets; print(secrets.token_hex(16))")
    OPENAI_API_KEY=your_openai_api_key
    ASSISTANT_ID=your_openai_assistant_id

4. **Run the Website**
python run.py
The website will be available at http://127.0.0.1:5000/