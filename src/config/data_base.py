from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Configurações da aplicação
app = Flask(__name__)
app.config['HOST'] = '0.0.0.0'
app.config['PORT'] = 8000
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///market_management.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicialize o SQLAlchemy sem passar o app diretamente
db = SQLAlchemy()

def init_db(app):
    """
    Inicializa a base de dados com o app Flask e o SQLAlchemy.
    """
    db.init_app(app)  # Associa o banco de dados ao app Flask
    with app.app_context():
        db.create_all()  # Cria as tabelas no banco de dados

