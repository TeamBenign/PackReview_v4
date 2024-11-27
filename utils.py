"""
utils.py

This module provides utility functions for interacting with a MongoDB database.

Functions:
- get_db(is_test=False): Connects to the MongoDB database and returns the appropriate
  database instance based on the test flag.

Usage:
    Call `get_db()` to retrieve the main project database, or `get_db(is_test=True)` to retrieve the
    test database. The MongoDB password should be stored in a configuration file named `config.ini`
    located in the same directory as this script.

Notes:
    Ensure that the `config.ini` file contains the correct password for the MongoDB connection.
"""

import os
import sys
from pymongo import MongoClient
from urllib.parse import quote_plus


def get_db(is_test=False):
    """Connect to the MongoDB database and return the appropriate database based on the test flag.

    Args:
        is_test (bool): If True, return the test database. Defaults to False.

    Returns:
        Database: The MongoDB database instance.
    """
    with open(os.path.join(sys.path[0], "config.ini"), "r", encoding="utf-8") as f:
        content = f.readlines()
    password = quote_plus(content[0].strip())
    mongo_uri = (
        f"mongodb+srv://kishan:kishan123@cluster0.fdzgd.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
    )
    with MongoClient(mongo_uri) as client:
        client = MongoClient(mongo_uri)
        return client.SETestProj if is_test else client.SEProj2
