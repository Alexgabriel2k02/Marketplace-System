from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Config da aplicação
app = Flask(__name__)
app.config['HOST'] = '0.0.0.0'
app.config['PORT'] = 8000
app.config['DEBUG'] = True

db = SQLAlchemy()

def init_db(app):
    # URI do banco SQLite
    # O banco será criado no arquivo 'mercado.db' na raiz do projeto
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mercado.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
