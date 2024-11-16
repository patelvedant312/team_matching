# main.py
import os
from app import create_app  # Import the create_app function from app/__init__.py

app = create_app()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
