import pandas as pd
import pymysql
import matplotlib.pyplot as plt
import streamlit as st

st.set_page_config(layout="wide")
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
        connect_timeout=10,
        autocommit=True
    )

conn = get_connection()

# Faturamento por vendedor
df = pd.read_sql("""
SELECT s.name AS seller, COUNT(sa.id) AS total_sales, SUM(sa.total_price) AS total_revenue
FROM sales sa
JOIN sellers s ON sa.seller_id = s.id
GROUP BY s.name
ORDER BY total_revenue DESC;
""", conn)

#  Top 10 produtos mais vendidos
df2 = pd.read_sql("""
SELECT p.name AS product, SUM(sa.quantity) AS total_sold
FROM sales sa
JOIN products p ON sa.product_id = p.id
GROUP BY p.name
ORDER BY total_sold DESC
LIMIT 10;
""", conn)

# --- LAYOUT ---

col1, col2, col3 = st.columns(3)
col1.metric("1º Vendedor", df.iloc[0]["seller"], f'R$ {df.iloc[0]["total_revenue"]:,.2f}')
col2.metric("2º Vendedor", df.iloc[1]["seller"], f'R$ {df.iloc[1]["total_revenue"]:,.2f}')
col3.metric("3º Vendedor", df.iloc[2]["seller"], f'R$ {df.iloc[2]["total_revenue"]:,.2f}')

st.markdown("---")

#  Gráfico de linha 
col4, col5 = st.columns((2, 1))
with col4:
    st.subheader("Faturamento por Vendedor")
    st.line_chart(df.set_index("seller")["total_revenue"])
 
 #pizza
with col5:
    st.subheader("Participação dos Top 10 Produtos")
    fig_pie, ax_pie = plt.subplots(facecolor='none')
    wedges, texts, autotexts = ax_pie.pie(
        df2["total_sold"],
        labels=df2["product"],
        autopct="%.1f%%",
        textprops={'color': 'white'}
    )
    ax_pie.axis("equal")
    # Deixa o fundo dos textos branco
    for text in texts + autotexts:
        text.set_color('white')
    st.pyplot(fig_pie, transparent=True)

st.markdown("---")

# Abaixo: Gráfico de barras (top 10 produtos mais vendidos)
st.subheader("Top 10 Produtos Mais Vendidos")
fig_bar, ax_bar = plt.subplots(figsize=(10, 6), facecolor='none')
ax_bar.bar(df2["product"], df2["total_sold"], color="#1f77b4")
ax_bar.set_xlabel("Produto", color='white')
ax_bar.set_ylabel("Quantidade Vendida", color='white')
ax_bar.set_title("Top 10 Produtos Mais Vendidos", color='white')
ax_bar.tick_params(axis='x', colors='white')
ax_bar.tick_params(axis='y', colors='white')
plt.xticks(rotation=45)
plt.tight_layout()
st.pyplot(fig_bar, transparent=True)