"""
This module serves as the entry point for running the Flask application.

It imports the Flask application instance from the app package and 
is used to start the application server for handling CRUD operations 
related to job reviews.
"""
from app import app
def __init__():
    app.run(debug=True)
