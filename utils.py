import os
import sys
from pymongo import MongoClient


def get_DB(isTest=False):
    with open(os.path.join(sys.path[0], "config.ini"), "r") as f:
        content = f.readlines()
    client = MongoClient("mongodb+srv://anishd1910:" +
                         content[0]+"@cluster0.oagwk.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0&ssl=true")

    if (isTest):
        return client.SETestProj
    else:
        return client.SEProj2
