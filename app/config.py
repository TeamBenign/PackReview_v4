"""
config.py

This module contains configuration settings for the application.
"""

import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    """Configuration settings for the database connection."""
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    def get_database_uri(self):
        """Returns the database URI."""
        return self.SQLALCHEMY_DATABASE_URI

    def is_sqlalchemy_tracking_enabled(self):
        """Returns whether SQLAlchemy tracking modifications is enabled."""
        return self.SQLALCHEMY_TRACK_MODIFICATIONS
