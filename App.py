import os
from flask import Flask
from extensions import db, mail, bcrypt
from dotenv import load_dotenv

# Load .env file
load_dotenv()

app = Flask(__name__)
app.config.from_prefixed_env()

# FIX: Set a Secret Key for Sessions (Required for Admin & Auth)
app.secret_key = os.getenv("SECRET_KEY") or "this-is-a-secret-key-for-dev"

# Database Config: Safety check to prevent crashes
uri = os.getenv("SQLALCHEMY_DATABASE_URI") or os.getenv("FLASK_SQLALCHEMY_DATABASE_URI")
if uri:
    app.config["SQLALCHEMY_DATABASE_URI"] = uri
else:
    app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///database.db'

# Initialize Extensions
db.init_app(app)
mail.init_app(app)
bcrypt.init_app(app)

# Import Blueprints
from Apps.main import main
from Apps.auth import auth
from Apps.crop import crop
from Apps.shop import shop
from Apps.query import query
# NEW IMPORTS FOR FEATURES
from Apps.admin import admin      
from Apps.chatbot import chatbot  
from Api.api import api

# Register Blueprints
app.register_blueprint(auth)
app.register_blueprint(main)
app.register_blueprint(crop)
app.register_blueprint(shop)
app.register_blueprint(query)
# REGISTER NEW FEATURES
app.register_blueprint(admin)     
app.register_blueprint(chatbot)   
api.init_app(app)

if __name__ == "__main__":
    app.run(debug=True)