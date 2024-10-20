# app/db.py
from flask_pymongo import PyMongo
from . import mongo

users_collection = mongo.db.users