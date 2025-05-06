import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Configuração inicial da página
st.set_page_config(page_title="Análise de Vendas de Jogos", layout="wide")
st.title("🎮 Análise de Vendas de Jogos - VG Sales")

# Upload do arquivo
st.header("📂 Upload do Arquivo CSV")

uploaded_file = st.file_uploader("Envie o arquivo vgsales.csv", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    # Visualização dos Dados
    st.header("🔎 Visualização dos Dados")
    st.dataframe(df, use_container_width=True)

    # Estatísticas Descritivas
    st.header("📊 Estatísticas Descritivas")
    st.write(df.describe())

    # Barra lateral com Filtros
    st.sidebar.header("🎯 Filtros")
    platforms = df['Platform'].dropna().unique()
    selected_platform = st.sidebar.selectbox('Selecione uma Plataforma:', options=['Todas'] + sorted(platforms))

    years = df['Year'].dropna().unique()
    selected_year = st.sidebar.selectbox('Selecione um Ano:', options=['Todos'] + sorted(years))

    # Aplicar filtros
    filtered_df = df.copy()

    if selected_platform != 'Todas':
        filtered_df = filtered_df[filtered_df['Platform'] == selected_platform]

    if selected_year != 'Todos':
        filtered_df = filtered_df[filtered_df['Year'] == selected_year]

    st.header("📈 Gráficos de Análise")

    # Top 10 Jogos Mais Vendidos
    st.subheader("🏆 Top 10 Jogos Mais Vendidos (Global Sales)")

    top_games = filtered_df.sort_values(by="Global_Sales", ascending=False).head(10)

    fig1, ax1 = plt.subplots(figsize=(10, 6))
    sns.barplot(x="Global_Sales", y="Name", data=top_games, palette="viridis", ax=ax1)
    ax1.set_xlabel("Vendas Globais (em milhões)")
    ax1.set_ylabel("Nome do Jogo")
    ax1.set_title("Top 10 Jogos Mais Vendidos")
    st.pyplot(fig1)

    # Distribuição de Vendas por Região
    st.subheader("🌎 Distribuição de Vendas por Região")

    regions = ['NA_Sales', 'EU_Sales', 'JP_Sales', 'Other_Sales']
    region_sales = filtered_df[regions].sum()

    fig2, ax2 = plt.subplots(figsize=(8, 6))
    region_sales.plot(kind='bar', color='skyblue', ax=ax2)
    ax2.set_ylabel("Vendas (em milhões)")
    ax2.set_title("Vendas Totais por Região")
    st.pyplot(fig2)

    # Vendas Totais por Plataforma
    st.subheader("🕹️ Vendas Totais por Plataforma")

    platform_sales = filtered_df.groupby('Platform')['Global_Sales'].sum().sort_values(ascending=False).head(10)

    fig3, ax3 = plt.subplots(figsize=(10, 6))
    platform_sales.plot(kind='bar', color='salmon', ax=ax3)
    ax3.set_ylabel("Vendas Globais (em milhões)")
    ax3.set_xlabel("Plataforma")
    ax3.set_title("Top 10 Plataformas com Mais Vendas Globais")
    st.pyplot(fig3)

    st.success("✅ Análise concluída!")

else:
    st.warning("Por favor, envie um arquivo CSV para começar a análise.")
