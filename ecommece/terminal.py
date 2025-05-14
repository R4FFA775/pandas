import streamlit as st
import pandas as pd
import plotly.express as px
import os

# Configuração da página 
st.set_page_config(page_title="Dashboard E-commerce", layout="wide")

# Configuração de tema e estilo d o dashboard
st.markdown("""
<style>
    /* Tema escuro com destaque em ciano */
    .stApp {
        background-color: #000000;
        color: #ffffff;
    }
    
    h1, h2, h3 {
        color: #00ffff !important;
    }
    
    .stSelectbox, .stMultiSelect {
        background-color: #1a1a1a;
        color: #00ffff;
    }
    
    div[data-testid="stMetricValue"] {
        color: #00ffff !important;
    }
</style>
""", unsafe_allow_html=True)

st.title("Dashboard de Análise de Vendas")

# Carregando dados
@st.cache_data
def load_data():
    try:
        caminho_arquivo = os.path.join(os.path.dirname(__file__), 'Ecommerce_Consumer_Behavior_Analysis_Data (1).csv')
        df = pd.read_csv(caminho_arquivo)

        df['Purchase_Amount'] = df['Purchase_Amount'].str.replace('$', '').astype(float)
        
        return df
    except FileNotFoundError:
        st.error("Arquivo CSV não encontrado!")
        return None
    except Exception as e:
        st.error(f"Erro ao processar os dados: {str(e)}")
        return None
# ...resto do código continua igual...
df = load_data()

if df is not None:
    # Filtros na sidebar
    st.sidebar.header("Filtros")
    gender_filter = st.sidebar.multiselect("Gênero", df['Gender'].unique())
    
    # Aplicar filtros
    filtered_df = df.copy()
    if gender_filter:
        filtered_df = filtered_df[filtered_df['Gender'].isin(gender_filter)]

    # Métricas principais
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total de Clientes", len(filtered_df))
    with col2:
        st.metric("Média de Gastos", f"${filtered_df['Purchase_Amount'].mean():,.2f}")

    # Gráficos
    col1, col2 = st.columns(2)


    with col1:
        # Gráfico de Barras - Categorias mais Vendidas
        fig1 = px.bar(
            filtered_df['Purchase_Category'].value_counts(),  # Corrigido o nome da coluna
            title='Top Categorias de Produtos',
            template="plotly_dark",
            color_discrete_sequence=['#00ffff']
        )
        fig1.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            showlegend=False
        )
        st.plotly_chart(fig1, use_container_width=True)
    with col2:
        # Gráfico de Pizza - Métodos de Pagamento
        fig2 = px.pie(
            filtered_df,
            names='Payment_Method',
            title='Métodos de Pagamento',
            template="plotly_dark",
            color_discrete_sequence=['#00ffff', '#ffffff', '#666666', '#999999']
        )
        fig2.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig2, use_container_width=True)

    # Dados detalhados
    with st.expander("Ver Dados"):
        st.dataframe(filtered_df)