from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Configurações da aplicação
app = Flask(__name__)
app.config['HOST'] = '0.0.0.0'
app.config['PORT'] = 8000
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///market_management.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

def init_db(app):
    """
    Inicializa a base de dados com o app Flask e o SQLAlchemy.
    """
    # Remova a chamada redundante db.init_app(app)
    pass

