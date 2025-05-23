from flask import Blueprint, render_template, request, jsonify, session
import os
from dotenv import load_dotenv
import openai
import json


# Create a Blueprint named "pages"
bp = Blueprint("pages", __name__)

# Route for homepage - includes bio, picture, name, position
@bp.route("/")
def home():
    # Pass your information to the template
    return render_template(
        "pages/home.html",
        name="Kyle Woolford",
        position="MLOps Engineer",  # Update with your actual position
        # You can add more context variables here if needed
    )

# Route for contact page - includes email and LinkedIn
@bp.route("/contact")
def contact():
    # Pass your contact information to the template
    return render_template(
        "pages/contact.html",
        email="kwoolfo4@jh.edu",
        linkedin_url="https://www.linkedin.com/in/kyle-woolford-951036232/",
        linkedin_name="Kyle Woolford",
        # You can add more contact methods here
    )

# Route for projects page - includes your M1 project and other work
@bp.route("/projects")
def projects():
    # Create a list of projects to display
    projects = [
        {
            "title": "Personal Website with Custom Chatbot",
            "description": "A Flask-based personal website featuring a custom OpenAI-powered chatbot trained on personal data to answer questions about me.",
            "github_url": "https://github.com/yourusername/jhu_software_concepts",
            "technologies": ["Python", "Flask", "HTML/CSS", "OpenAI API"]
        },
        # You can add more projects here
    ]
    
    return render_template("pages/projects.html", projects=projects)

@bp.route("/chat")
def chat():
    """Render the chatbot interface page"""
    return render_template("pages/chat.html")

@bp.route("/api/chat", methods=["POST"])
def process_chat():
    """Process chat messages and return AI responses"""
    try:
        # Get message from request
        data = request.json
        user_message = data.get("message", "")
        
        # Initialize chat history if it doesn't exist
        if "chat_history" not in session:
            session["chat_history"] = []
        
        # Add user message to history
        session["chat_history"].append({"role": "user", "content": user_message})
        
        # Prepare messages for OpenAI API
        messages = [
            {"role": "system", "content": "You are Kyle's personal assistant chatbot. You help users learn about Kyle's background, projects, and skills. If someone asks for Kyle's resume, respond with exactly 'resume=true' and nothing else. Keep responses concise and helpful. If you don't know something, say so politely."},
        ]
        
        # Add chat history (limit to last 10 messages to save tokens)
        messages.extend(session["chat_history"][-10:])
        
        # Check if API key is configured
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key or api_key == "your_api_key_here":
            # No valid API key found
            response = "Sorry, the chatbot is not configured correctly. Please check the README for setup instructions."
            session["chat_history"].append({"role": "assistant", "content": response})
            return jsonify({"response": response, "error": "API key not configured"})
        
        # Call OpenAI API
        try:
            openai.api_key = api_key
            completion = openai.ChatCompletion.create(
                model=os.getenv("OPENAI_MODEL", "gpt-3.5-turbo"),
                messages=messages,
                max_tokens=int(os.getenv("MAX_TOKENS_PER_REQUEST", 150)),
                temperature=0.7,
            )
            
            # Extract response
            ai_response = completion.choices[0].message.content
            
            # Add AI response to history
            session["chat_history"].append({"role": "assistant", "content": ai_response})
            
            # Check for special commands
            if ai_response.strip().lower() == "resume=true":
                return jsonify({
                    "response": "I'd be happy to show you Kyle's resume!",
                    "action": "show_resume"
                })
            
            return jsonify({"response": ai_response})
            
        except Exception as e:
            # Log the error (in a production app)
            print(f"OpenAI API Error: {str(e)}")
            
            # Return friendly error message
            error_message = "Sorry, I'm having trouble connecting to my brain right now. Please try again later."
            session["chat_history"].append({"role": "assistant", "content": error_message})
            return jsonify({"response": error_message, "error": str(e)})
            
    except Exception as e:
        return jsonify({"response": "An error occurred processing your request.", "error": str(e)})

@bp.route("/api/reset-chat", methods=["POST"])
def reset_chat():
    """Reset the chat history"""
    if "chat_history" in session:
        session.pop("chat_history")
    return jsonify({"status": "success", "message": "Chat history reset"})