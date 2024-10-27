import os
import sys
from pymongo import MongoClient


def get_DB():
    with open(os.path.join(sys.path[0], "config.ini"), "r") as f:
        content = f.readlines()
    client = MongoClient("mongodb+srv://anishd1910:" +
                         content[0]+"@cluster0.oagwk.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")

    return client.SEProj2
