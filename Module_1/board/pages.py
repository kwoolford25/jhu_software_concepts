from flask import Blueprint, render_template

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