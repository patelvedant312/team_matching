import os
from app import create_app  # Import the create_app function from app/__init__.py

# Create the app instance
app = create_app()

# Run the app only if this file is executed directly
if __name__ == "__main__":
    # Use the PORT environment variable provided by Render or default to 5000
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
