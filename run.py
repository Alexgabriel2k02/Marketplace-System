from flask import Flask
from flask_jwt_extended import JWTManager
from src.routes import init_routes
from src.config.data_base import app, init_db, db

app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'  # Substitua por uma chave secreta segura
jwt = JWTManager(app)

init_routes(app)

if __name__ == '__main__':
    with app.app_context():
        init_db(app)
        db.create_all()  # Cria as tabelas no banco de dados
    app.run(host=app.config['HOST'], port=app.config['PORT'], debug=app.config['DEBUG'])