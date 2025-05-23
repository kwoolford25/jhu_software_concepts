from flask import Blueprint, render_template, request, jsonify, session
import os
from dotenv import load_dotenv
from openai import OpenAI
import json
import time


# Create a Blueprint named "pages"
bp = Blueprint("pages", __name__)

# Route for homepage
@bp.route("/")
def home():
    # Passing information to the template
    return render_template(
        "pages/home.html",
        name="Kyle Woolford",
        position="MLOps Programmer Analyst at Johns Hopkins",
    )

# Route for contact page
@bp.route("/contact")
def contact():
    # Passing contact information to the template
    return render_template(
        "pages/contact.html",
        email="kwoolfo4@jh.edu",
        linkedin_url="https://www.linkedin.com/in/kyle-woolford-951036232/",
        linkedin_name="Kyle Woolford",
        # You can add more contact methods here
    )

# Route for projects page
@bp.route("/projects")
def projects():
    # Create a list of projects to display
    projects = [
        {
            "title": "Personal Website with Custom Chatbot",
            "description": "A Flask-based personal website featuring a custom OpenAI-powered chatbot trained on personal data to answer questions about me.",
            "github_url": "https://github.com/kwoolford25/jhu_software_concepts/tree/main/Module_1",
            "technologies": ["Python", "Flask", "HTML/CSS", "OpenAI API"]
        },
        # More projects will be added here
    ]
    
    return render_template("pages/projects.html", projects=projects)

@bp.route("/chat")
def chat():
    """Render the chatbot interface page"""
    return render_template("pages/chat.html")

@bp.route("/api/chat", methods=["POST"])
def process_chat():
    """Process chat messages using OpenAI Assistants API"""
    try:
        # Get message from request
        data = request.json
        user_message = data.get("message", "")
        
        # Check if API key is configured
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key or api_key == "your_api_key_here":
            return jsonify({
                "response": "Sorry, the chatbot is not configured correctly. Please check the README for setup instructions.",
                "error": "API key not configured"
            })
        
        client = OpenAI(api_key=api_key)
        
        # Get or create thread ID from session
        thread_id = session.get("thread_id")
        if not thread_id:
            # Create a new thread
            thread = client.beta.threads.create()
            thread_id = thread.id
            session["thread_id"] = thread_id
        
        # Get assistant ID from environment or create if not exists
        assistant_id = os.getenv("ASSISTANT_ID")
        if not assistant_id:
            # This is a one-time setup that should be done manually
            # and the ID stored in the .env file
            return jsonify({
                "response": "Assistant ID not configured. Please create an assistant and add its ID to the .env file.",
                "error": "Assistant not configured"
            })
        
        # Add the user message to the thread
        client.beta.threads.messages.create(
            thread_id=thread_id,
            role="user",
            content=user_message
        )
        
        # Run the assistant on the thread
        run = client.beta.threads.runs.create(
            thread_id=thread_id,
            assistant_id=assistant_id
        )
        
        # Poll for the run to complete
        while run.status in ["queued", "in_progress"]:
            time.sleep(0.5)  # Wait half a second before checking again
            run = client.beta.threads.runs.retrieve(
                thread_id=thread_id,
                run_id=run.id
            )
        
        # Check if run failed
        if run.status != "completed":
            return jsonify({
                "response": "Sorry, there was an error processing your message. Please try again later.",
                "error": f"Run status: {run.status}"
            })
        
        # Get the latest message (the assistant's response)
        messages = client.beta.threads.messages.list(thread_id=thread_id)
        
        # The first message should be the latest assistant response
        for message in messages.data:
            if message.role == "assistant":
                # Check for special commands in the response
                response_text = message.content[0].text.value
                
                if "resume=true" in response_text.lower():
                    return jsonify({
                        "response": "I'd be happy to show you Kyle's resume!",
                        "action": "show_resume"
                    })
                
                return jsonify({"response": response_text})
        
        # Fallback if no assistant message found
        return jsonify({
            "response": "Sorry, I couldn't generate a response. Please try again.",
            "error": "No assistant message found"
        })
            
    except Exception as e:
        return jsonify({
            "response": "An error occurred processing your request.",
            "error": str(e)
        })

@bp.route("/api/reset-chat", methods=["POST"])
def reset_chat():
    """Reset the chat thread"""
    if "thread_id" in session:
        session.pop("thread_id")
    return jsonify({"status": "success", "message": "Chat history reset"})