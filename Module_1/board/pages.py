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
        data = request.json
        user_message = data.get("message", "").strip()

        if not user_message:
            return jsonify({"response": "Please enter a message."})

        api_key = os.getenv("OPENAI_API_KEY")
        assistant_id = os.getenv("ASSISTANT_ID")

        if not api_key or not assistant_id:
            return jsonify({
                "response": "API key or Assistant ID is missing. Please check your .env file.",
                "error": "Missing credentials"
            })

        client = OpenAI(api_key=api_key)

        # Get or create thread
        thread_id = session.get("thread_id")
        if not thread_id:
            thread = client.beta.threads.create()
            thread_id = thread.id
            session["thread_id"] = thread_id

        # Add user message to thread
        client.beta.threads.messages.create(
            thread_id=thread_id,
            role="user",
            content=user_message
        )

        # Run assistant
        run = client.beta.threads.runs.create(
            thread_id=thread_id,
            assistant_id=assistant_id
            )

        # Poll for completion
        while run.status in ["queued", "in_progress"]:
            time.sleep(1)
            run = client.beta.threads.runs.retrieve(
            thread_id=thread_id,
            run_id=run.id
            )

        if run.status != "completed":
            return jsonify({
                "response": "Sorry, something went wrong while generating a response.",
                "error": f"Run status: {run.status}"
                })

        # Get assistant's reply
        messages = client.beta.threads.messages.list(thread_id=thread_id)
        for message in messages.data:
            if message.role == "assistant":
                response_text = message.content[0].text.value

                # Optional: trigger resume modal
                if "resume=true" in response_text.lower():
                    return jsonify({
                    "response": "I'd be happy to show you Kyle's resume!",
                    "action": "show_resume"
                })

                return jsonify({"response": response_text})

            return jsonify({
                "response": "No assistant response found.",
                "error": "Empty message list"
        })

    except Exception as e:
        return jsonify({
            "response": "An unexpected error occurred.",
            "error": str(e)
        })

@bp.route("/api/reset-chat", methods=["POST"])
def reset_chat():
    """Reset the chat thread"""
    if "thread_id" in session:
        session.pop("thread_id")
    return jsonify({"status": "success", "message": "Chat history reset"})