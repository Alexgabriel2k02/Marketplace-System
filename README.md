# 📦 Gestão de Estoque para Mini Mercados

## 📌 Objetivo
Desenvolver um sistema para gestão de estoque e vendas de mini mercados, garantindo segurança, controle de acesso e gestão eficiente de produtos e vendas.

---


## 🚀 Funcionalidades Principais

### 1️⃣ Cadastro de Mini Mercado (Seller)
Os mini mercados devem se cadastrar informando os seguintes campos:
- **Nome**
- **CNPJ**
- **E-mail**
- **Celular**
- **Senha**
- **Status** (Padrão: Inativo)

#### 🔹 Fluxo de Ativação do Seller:
1. Após o cadastro, um código de 4 dígitos é enviado via **WhatsApp (Twilio)** para o seller.
2. O seller deve inserir o código recebido para ativar sua conta.
3. Somente sellers ativados podem fazer login e gerenciar produtos.

---

### 2️⃣ Autenticação do Seller
- O sistema deve utilizar **JWT** ou **OAuth** para autenticação.
- Sellers inativados não podem fazer login.

---

### 3️⃣ Gerenciamento de Produtos
Um seller autenticado pode:
- **Cadastrar produtos** com os seguintes campos:
  - Nome
  - Preço
  - Quantidade
  - Status (Ativo/Inativo)
  - Imagem
- **Listar produtos** cadastrados
- **Editar produto**
- **Ver detalhes de um produto**
- **Inativar produtos**

**Regras:**
- O seller só pode visualizar e gerenciar seus próprios produtos.

---

### 4️⃣ Venda de Produtos
- O seller pode realizar uma venda informando:
  - Produto
  - Quantidade
- As vendas devem ser armazenadas na tabela `Vendas`, contendo:
  - ID do Produto
  - Quantidade vendida
  - Preço do produto no momento da venda

**Regras:**
- Não é possível vender mais do que a quantidade disponível em estoque.
- Produtos inativados não podem ser vendidos.
- Sellers inativos não podem realizar vendas.

---

## 🛠️ Configuração do Banco de Dados (MySQL)

### Pré-requisitos
1. Certifique-se de que o MySQL está instalado e em execução no seu sistema.
2. Crie um banco de dados para o projeto:
   ```sql
   CREATE DATABASE nome_do_banco_de_sua_preferencia;
   ```

3. Crie um usuário no MySQL (se necessário) ou use o usuário padrão `root`.

---

### Configuração no Projeto
1. No arquivo `src/config/data_base.py`, configure a URI de conexão com o MySQL:
   ```python
   app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://usuario:senha@host:porta/nome_do_banco'
   ```
   Substitua:
   - `usuario`: Pelo nome do usuário do MySQL (ex.: `root`).
   - `senha`: Pela senha do usuário.
   - `host`: Pelo endereço do servidor MySQL (ex.: `localhost`).
   - `porta`: Pela porta do MySQL (padrão é `3306`).
   - `nome_do_banco`: Pelo nome do banco de dados criado (ex.: `nome_do_banco_de_sua_preferencia`).

2. Instale o driver `pymysql` para conectar ao MySQL:
   ```bash
   pip install pymysql
   ```

3. Execute o projeto para inicializar as tabelas no banco de dados:
   ```bash
   python run.py
   ```

4. Verifique no MySQL se as tabelas foram criadas:
   ```sql
   USE nome_do_banco_de_sua_preferencia;
   SHOW TABLES;
   ```
---

## 📡 Endpoints da API

### 1️⃣ Cadastro e Ativação do Seller
- **Criar Seller**
  ```bash
  curl -X POST "http://localhost:8080/api/sellers" \
       -H "Content-Type: application/json" \
       -d '{"nome": "Mini Mercado X", "cnpj": "00.000.000/0001-00", "email": "mercado@email.com", "celular": "+559999999999", "senha": "123456"}'
  ```
- **Ativar Seller via WhatsApp (Twilio)**
  ```bash
  curl -X POST "http://localhost:8080/api/sellers/activate" \
       -H "Content-Type: application/json" \
       -d '{"celular": "+559999999999", "codigo": "1234"}'
  ```

### 2️⃣ Autenticação
- **Login**
  ```bash
  curl -X POST "http://localhost:8080/api/auth/login" \
       -H "Content-Type: application/json" \
       -d '{"email": "mercado@email.com", "senha": "123456"}'
  ```

### 3️⃣ Gerenciamento de Produtos
- **Cadastrar Produto**
  ```bash
  curl -X POST "http://localhost:8080/api/products" \
       -H "Authorization: Bearer SEU_TOKEN" \
       -H "Content-Type: application/json" \
       -d '{"nome": "Arroz", "preco": 10.50, "quantidade": 100, "status": "Ativo", "img": "url_da_imagem"}'
  ```
- **Listar Produtos**
  ```bash
  curl -X GET "http://localhost:8080/api/products" \
       -H "Authorization: Bearer SEU_TOKEN"
  ```
- **Editar Produto**
  ```bash
  curl -X PUT "http://localhost:8080/api/products/1" \
       -H "Authorization: Bearer SEU_TOKEN" \
       -H "Content-Type: application/json" \
       -d '{"nome": "Arroz Integral", "preco": 12.00, "quantidade": 50, "status": "Ativo"}'
  ```
- **Ver Detalhes de um Produto**
  ```bash
  curl -X GET "http://localhost:8080/api/products/1" \
       -H "Authorization: Bearer SEU_TOKEN"
  ```
- **Inativar Produto**
  ```bash
  curl -X PATCH "http://localhost:8080/api/products/1/inactivate" \
       -H "Authorization: Bearer SEU_TOKEN"
  ```

### 4️⃣ Realizar Venda
- **Criar Venda**
  ```bash
  curl -X POST "http://localhost:8080/api/sales" \
       -H "Authorization: Bearer SEU_TOKEN" \
       -H "Content-Type: application/json" \
       -d '{"produtoId": 1, "quantidade": 2}'
  ```

---

## 🛠️ Tecnologias Utilizadas
- **Back-end:** Python (Flask)
- **Front-end:** React.js
- **Banco de Dados:** MySQL 
- **Autenticação:** JWT ou 
- **Mensageria:** Twilio (para envio do código de ativação no WhatsApp)

---

## 📊 Dashboard e Relatórios
- Implementação de um painel para exibição de relatórios e análise de vendas.
- Monitoramento de estoque em tempo real.

---

## 📌 Considerações Finais
Este projeto fornece um sistema completo para mini mercados gerenciarem seus estoques e vendas com segurança e eficiência. 🚀

