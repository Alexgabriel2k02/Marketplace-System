import pandas as pd
import pymysql
import matplotlib.pyplot as plt
import streamlit as st

st.title("Dashboard Marketplace")

# Conexão com o banco
@st.cache_resource
def get_connection():
    return pymysql.connect(
        host='127.0.0.1',
        user='root',
        password='Joao@321',
        database='marketplacesystem',
        port=3306,
        connect_timeout=10
    )

conn = get_connection()

# Vendas por vendedor
query = """
SELECT s.name AS seller, COUNT(sa.id) AS total_sales, SUM(sa.total_price) AS total_revenue
FROM sales sa
JOIN sellers s ON sa.seller_id = s.id
GROUP BY s.name
ORDER BY total_revenue DESC;
"""
df = pd.read_sql(query, conn)
st.subheader("Faturamento por Vendedor")
st.dataframe(df)

fig1, ax1 = plt.subplots(figsize=(10,6))
ax1.bar(df['seller'], df['total_revenue'])
ax1.set_title('Faturamento por Vendedor')
ax1.set_xlabel('Vendedor')
ax1.set_ylabel('Faturamento (R$)')
plt.xticks(rotation=45)
plt.tight_layout()
st.pyplot(fig1)

# Produtos mais vendidos
query2 = """
SELECT p.name AS product, SUM(sa.quantity) AS total_sold
FROM sales sa
JOIN products p ON sa.product_id = p.id
GROUP BY p.name
ORDER BY total_sold DESC
LIMIT 10;
"""
df2 = pd.read_sql(query2, conn)
st.subheader("Top 10 Produtos Mais Vendidos")
st.dataframe(df2)

fig2, ax2 = plt.subplots(figsize=(10,6))
ax2.bar(df2['product'], df2['total_sold'])
ax2.set_title('Top 10 Produtos Mais Vendidos')
ax2.set_xlabel('Produto')
ax2.set_ylabel('Quantidade Vendida')
plt.xticks(rotation=45)
plt.tight_layout()
st.pyplot(fig2)

conn.close()