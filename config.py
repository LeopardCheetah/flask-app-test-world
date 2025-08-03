import os
from dotenv import load_dotenv

base_db_dir = os.path.abspath(os.path.dirname(__file__))

load_dotenv()

# use wrapper so flask automates a buncha stuff for us
class Config:
    SECRET_KEY = os.getenv('CSRF_SECRET') or 'some other key'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(base_db_dir, 'app.db')
