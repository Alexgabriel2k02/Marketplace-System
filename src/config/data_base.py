from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Config da aplicação
app = Flask(__name__)
app.config['HOST'] = '0.0.0.0'
app.config['PORT'] = 8000
app.config['DEBUG'] = True

db = SQLAlchemy()

def init_db(app):
    # URI do banco ajustada com o nome do banco e senha informados
    # Observação: o caractere '@' na senha foi percent-encoded como '%40'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:22121396Jg%40@127.0.0.1:3306/mercado'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
