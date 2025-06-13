from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Config da aplicação
app = Flask(__name__)
app.config['HOST'] = '0.0.0.0'
app.config['PORT'] = 8000
app.config['DEBUG'] = True

db = SQLAlchemy()

def init_db(app):
    # Substitua a string abaixo pela URI do seu banco de dados
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://usuario:senha@host:porta/nome_do_banco'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
