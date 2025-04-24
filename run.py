from flask import Flask
from flask_jwt_extended import JWTManager
from src.routes import init_routes
from src.config.data_base import app, init_db, db
from src.Infrastructure.Model.seller import Seller
from src.Infrastructure.Model.product import Product
from src.Infrastructure.Model.sales import Sale
from src.Infrastructure.Model.orders import Order

# Configuração do JWT
app.config["JWT_SECRET_KEY"] = (
    "your_jwt_secret_key"  # Substituir por uma chave secreta segura
)
jwt = JWTManager(app)

# Inicializa o banco de dados
init_db(app)

# Cria as tabelas no banco de dados
with app.app_context():
    db.create_all()

# Inicializa as rotas
init_routes(app)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
