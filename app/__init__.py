from flask import Flask
from .site.routes import site
from config import Config
from .authentication.routes import auth
from .api.routes import api
from supabase import create_client, Client
from dotenv import load_dotenv
import os
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from models import db as root_db, login_manager, ma
from flask_cors import CORS
from helpers import JSONEncoder

load_dotenv()

app = Flask(__name__)
CORS(app)

SUPABASE_URL = os.getenv('SUPABASE_URL')
# SUPABASE_KEY = os.getenv('SUPABASE_KEY')

app.register_blueprint(site)
app.register_blueprint(auth)
app.register_blueprint(api)

app.json_encoder = JSONEncoder
app.config.from_object(Config)
root_db.init_app(app)
login_manager.init_app(app)
ma.init_app(app)
migrate = Migrate(app, root_db)
