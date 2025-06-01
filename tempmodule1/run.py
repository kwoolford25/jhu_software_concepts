from board import create_app

# Create the Flask application
app = create_app()

# Run the application when this script is executed directly
if __name__ == "__main__":
    app.run(debug=True)