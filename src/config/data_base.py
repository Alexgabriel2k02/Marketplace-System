from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Configurações da aplicação
app = Flask(__name__)
app.config['HOST'] = '0.0.0.0'
app.config['PORT'] = 8000
app.config['DEBUG'] = True

db = SQLAlchemy()

def init_db(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:22121396Jg%40@127.0.0.1:3306/Mercado'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
