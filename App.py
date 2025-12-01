import os
from flask import Flask
from extensions import db, mail, bcrypt
from dotenv import load_dotenv

# 1. Load the .env file explicitly
# This is crucial so that os.getenv can find your variables
load_dotenv()

app = Flask(__name__)

# 2. Load config from .env (looks for FLASK_SQLALCHEMY_DATABASE_URI)
app.config.from_prefixed_env()

# 3. SAFETY CHECK: Manually set the database URI if the prefix method missed it.
# This ensures db.init_app(app) never fails with a RuntimeError.
uri = os.getenv("SQLALCHEMY_DATABASE_URI") or os.getenv("FLASK_SQLALCHEMY_DATABASE_URI")
if uri:
    app.config["SQLALCHEMY_DATABASE_URI"] = uri
else:
    # Final fallback: Use a local file database so it runs no matter what
    # This prevents the "RuntimeError" you were seeing
    app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///database.db'
    print("WARNING: Could not find database URL in .env. Using default sqlite.")

# Initialize extensions
db.init_app(app)
mail.init_app(app)
bcrypt.init_app(app)

# Import and Register Blueprints
from Apps.main import main
from Apps.auth import auth
from Apps.crop import crop
from Apps.shop import shop
from Apps.query import query
from Api.api import api

app.register_blueprint(auth)
app.register_blueprint(main)
app.register_blueprint(crop)
app.register_blueprint(shop)
app.register_blueprint(query)
api.init_app(app)

if __name__ == "__main__":
    app.run(debug=True)