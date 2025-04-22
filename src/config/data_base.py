from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Configurações da aplicação
app = Flask(__name__)
app.config['HOST'] = '0.0.0.0'
app.config['PORT'] = 8000
app.config['DEBUG'] = True

# Configuração do banco de dados MySQL
# Substituir 'usuario', 'senha', 'host', 'porta' e 'nome_do_banco' pelas suas credenciais reais
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://usuario:senha@host:porta/nome_do_banco'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicialize o SQLAlchemy sem passar o app diretamente
db = SQLAlchemy()

def init_db(app):
    """
    Inicializa a base de dados com o app Flask e o SQLAlchemy.
    """
    db.init_app(app) 
    with app.app_context():
        db.create_all()
