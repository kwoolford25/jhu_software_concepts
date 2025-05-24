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

@bp.route("/chat", methods=["GET", "POST"])
def chat():
    # Initialize session if needed
    if "messages" not in session:
        session["messages"] = []
        
    error = None
    show_resume = False
    processing = False
    
    if request.method == "POST":
        action = request.form.get("action")
        
        # Handle reset action
        if action == "reset":
            session["messages"] = []
            if "thread_id" in session:
                session.pop("thread_id")
        
        # Handle send action
        elif action == "send":
            user_message = request.form.get("user_message", "").strip()
            
            if user_message:
                # Add user message immediately
                session["messages"].append({"role": "user", "content": user_message})
                session.modified = True
                
                # Show processing indicator
                processing = True
                
                # Process with OpenAI
                try:
                    api_key = os.getenv("OPENAI_API_KEY")
                    assistant_id = os.getenv("ASSISTANT_ID")
                    
                    if not api_key or not assistant_id:
                        error = "API key or Assistant ID is missing. Please check your .env file."
                    else:
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
                        
                        # Poll for completion (with timeout)
                        start_time = time.time()
                        timeout = 30  # 30 seconds timeout
                        
                        while run.status in ["queued", "in_progress"]:
                            # Check for timeout
                            if time.time() - start_time > timeout:
                                error = "Request timed out. Please try again."
                                break
                                
                            time.sleep(1)
                            run = client.beta.threads.runs.retrieve(
                                thread_id=thread_id,
                                run_id=run.id
                            )
                        
                        if not error and run.status == "completed":
                            # Get assistant's reply
                            messages = client.beta.threads.messages.list(thread_id=thread_id)
                            
                            assistant_response = None
                            for message in messages.data:
                                if message.role == "assistant":
                                    response_text = message.content[0].text.value
                                    
                                    # Check for resume trigger
                                    if "resume=true" in response_text.lower():
                                        assistant_response = "I'd be happy to show you Kyle's resume!"
                                        show_resume = True
                                    else:
                                        assistant_response = response_text
                                        
                                    break
                            
                            if assistant_response:
                                session["messages"].append({"role": "assistant", "content": assistant_response})
                                session.modified = True
                            else:
                                error = "No response received from assistant."
                        elif not error:
                            error = f"Error: Assistant run failed with status {run.status}"
                            
                except Exception as e:
                    error = f"An error occurred: {str(e)}"
    
    # Make a copy of the messages for the template
    # (This is needed because session objects can't be modified directly in templates)
    messages = session.get("messages", []).copy()
    
    # Render the template with messages and any errors
    return render_template(
        "pages/chat.html",
        messages=messages,
        error=error,
        show_resume=show_resume,
        processing=processing
    )