"""
This module defines the database models for the application.

It includes the Reviews model, which stores information about job reviews submitted
by users, including department, location, job details, compensation, benefits, and ratings.
Each review is represented as a row in the Reviews table within the database.
"""
from app import DB

class Reviews(DB.Model):
    """Model which stores the information of the reviews submitted"""
    id = DB.Column(DB.Integer, primary_key=True)
    department = DB.Column(DB.String(64), index=True, nullable=False)
    locations = DB.Column(DB.String(120), index=True, nullable=False)
    job_title = DB.Column(DB.String(64), index=True, nullable=False)
    job_description = DB.Column(DB.String(120), index=True, nullable=False)
    hourly_pay = DB.Column(DB.Integer, nullable=False)
    benefits = DB.Column(DB.String(120), index=True, nullable=False)
    review = DB.Column(DB.String(120), index=True, nullable=False)
    rating = DB.Column(DB.Integer, nullable=False)
    recommendation = DB.Column(DB.Integer, nullable=False)
