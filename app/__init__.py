from flask import Flask

app = Flask(__name__)
app.config['SECRET_KEY'] = 'put-your-secret-key-here'
from app import views
