# iniciar o codigo com o comando: streamlit run ./jogo/principal.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import numpy as np
import os

# Configuração da página
st.set_page_config(
    page_title="Dashboard de Vendas de Videogames",
    page_icon="🎮",
    layout="wide"
)

# Exibir diretório atual e arquivos disponíveis para debug
st.sidebar.text("Diretório atual: " + os.getcwd())
arquivos = os.listdir()
st.sidebar.text("Arquivos disponíveis:")
for arquivo in arquivos:
    st.sidebar.text("- " + arquivo)

# Função para carregar dados
# Modifique apenas a função carregar_dados()

@st.cache_data
def carregar_dados():
    # Lista de possíveis nomes de arquivo com foco no diretório correto
    arquivos_possiveis = [
        '/workspaces/pandas/jogo/vgsales.csv',  # Caminho completo para o arquivo baixado
        'vgsales.csv',
        '../vgsales.csv'
    ]
    
    # Exibir caminho atual para debug
    st.sidebar.text(f"Procurando arquivo em: {os.getcwd()}")
    
    # Tenta abrir cada um dos arquivos possíveis
    for arquivo in arquivos_possiveis:
        try:
            st.sidebar.text(f"Tentando abrir: {arquivo}")
            df = pd.read_csv(arquivo)
            st.sidebar.success(f"Arquivo carregado com sucesso: {arquivo}")
            # Evitar o uso de inplace=True em operações encadeadas
            df = df.copy()
            df['Publisher'] = df['Publisher'].fillna('Desconhecido')
            # Convertendo Year para numérico
            df['Year'] = pd.to_numeric(df['Year'], errors='coerce')
            return df
        except FileNotFoundError:
            st.sidebar.text(f"Arquivo não encontrado: {arquivo}")
            continue
        except Exception as e:
            st.sidebar.error(f"Erro ao carregar {arquivo}: {str(e)}")
            continue
    
    # Se nenhum arquivo for encontrado, cria um dataset de exemplo
    st.sidebar.error("Arquivo de dados não encontrado. Usando dataset de exemplo.")
    
    # Criando um dataset de exemplo
    exemplo = {
        'Name': ['Super Mario Bros', 'Tetris', 'Mario Kart', 'Pokemon Red/Blue', 'Minecraft'],
        'Platform': ['NES', 'GB', 'SNES', 'GB', 'PC'],
        'Year': [1985, 1989, 1992, 1996, 2011],
        'Genre': ['Platform', 'Puzzle', 'Racing', 'Role-Playing', 'Sandbox'],
        'Publisher': ['Nintendo', 'Nintendo', 'Nintendo', 'Nintendo', 'Mojang'],
        'NA_Sales': [29.08, 23.2, 15.0, 11.27, 6.42],
        'EU_Sales': [3.58, 2.26, 3.91, 8.89, 5.31],
        'JP_Sales': [6.81, 4.22, 3.28, 10.22, 0.24],
        'Other_Sales': [0.77, 0.58, 0.41, 1.0, 3.33],
        'Global_Sales': [40.24, 30.26, 22.6, 31.38, 15.3]
    }
    
    return pd.DataFrame(exemplo)

# Carregando os dados
df = carregar_dados()

# Título do Dashboard
st.title("📊 Dashboard de Análise de Vendas de Videogames")
st.markdown("Análise de dados de vendas globais de videogames")

# Sidebar para filtros globais
st.sidebar.header("Filtros Globais")

# Filtros de ano
anos_disponiveis = df['Year'].dropna().astype(int).unique()
anos_disponiveis.sort()
min_ano, max_ano = int(min(anos_disponiveis)), int(max(anos_disponiveis))
ano_filtro = st.sidebar.slider("Intervalo de Anos", min_ano, max_ano, (min_ano, max_ano))

# Filtros de gênero
todos_generos = ['Todos'] + sorted(df['Genre'].unique().tolist())
genero_selecionado = st.sidebar.selectbox("Gênero", todos_generos)

# Filtros de plataforma
todas_plataformas = ['Todas'] + sorted(df['Platform'].unique().tolist())
plataforma_selecionada = st.sidebar.selectbox("Plataforma", todas_plataformas)

# Filtros de editora
top_editoras = ['Todas'] + df['Publisher'].value_counts().head(15).index.tolist()
editora_selecionada = st.sidebar.selectbox("Editora", top_editoras)

# Aplicar filtros
filtro_df = df.copy()

# Filtrar por ano
filtro_df = filtro_df[(filtro_df['Year'] >= ano_filtro[0]) & (filtro_df['Year'] <= ano_filtro[1])]

# Filtrar por gênero
if genero_selecionado != 'Todos':
    filtro_df = filtro_df[filtro_df['Genre'] == genero_selecionado]

# Filtrar por plataforma
if plataforma_selecionada != 'Todas':
    filtro_df = filtro_df[filtro_df['Platform'] == plataforma_selecionada]

# Filtrar por editora
if editora_selecionada != 'Todas':
    filtro_df = filtro_df[filtro_df['Publisher'] == editora_selecionada]

# Métricas Gerais - Row 1
st.header("Métricas Gerais")

col1, col2, col3, col4 = st.columns(4)

with col1:
    total_jogos = len(filtro_df['Name'].unique())
    st.metric("Total de Jogos Únicos", f"{total_jogos:,}")

with col2:
    jogos_com_ano = filtro_df.dropna(subset=['Year'])
    st.metric("Ano do Jogo Mais Antigo", int(jogos_com_ano['Year'].min()))
    st.metric("Ano do Jogo Mais Recente", int(jogos_com_ano['Year'].max()))

with col3:
    media_vendas = filtro_df['Global_Sales'].mean()
    st.metric("Média de Vendas Globais (milhões)", f"{media_vendas:.2f}")

with col4:
    top_publisher = filtro_df['Publisher'].value_counts().idxmax()
    jogos_top_publisher = filtro_df[filtro_df['Publisher'] == top_publisher].shape[0]
    st.metric("Editora com Mais Jogos", f"{top_publisher} ({jogos_top_publisher} jogos)")

# Top Jogos por Vendas - Row 2
st.header("Top Jogos por Vendas")

col1, col2 = st.columns(2)

with col1:
    top_n = st.radio("Número de jogos para exibir:", [5, 10, 20], horizontal=True)

with col2:
    tipo_venda = st.selectbox(
        "Tipo de Venda:",
        ["Global_Sales", "NA_Sales", "EU_Sales", "JP_Sales", "Other_Sales"]
    )

# Gráfico de barras horizontais para top jogos
top_jogos = filtro_df.sort_values(tipo_venda, ascending=False).head(top_n)
top_jogos['Detalhes'] = top_jogos['Name'] + ' | ' + top_jogos['Platform'] + ' | ' + top_jogos['Year'].astype(str)

fig_top_jogos = px.bar(
    top_jogos,
    x=tipo_venda,
    y='Detalhes',
    orientation='h',
    title=f'Top {top_n} Jogos por {tipo_venda.replace("_", " ")} (milhões)',
    labels={tipo_venda: 'Vendas (milhões)', 'Detalhes': 'Jogo'},
    hover_data=['Name', 'Platform', 'Year', 'Genre', 'Publisher'],
    color=tipo_venda,
    color_continuous_scale='Viridis'
)
fig_top_jogos.update_layout(height=500)
st.plotly_chart(fig_top_jogos, use_container_width=True)

# Distribuição de Vendas por Região - Row 3
st.header("Distribuição de Vendas por Região")

# Filtro por década
decadas = {
    'Todas': (min_ano, max_ano),
    '1980-1990': (1980, 1990),
    '1991-2000': (1991, 2000),
    '2001-2010': (2001, 2010),
    '2011-2020': (2011, 2020)
}

# Seleção de década
decada_selecionada = st.selectbox("Selecione a Década:", list(decadas.keys()))
decada_df = filtro_df.copy()

# Aplicando filtro de década (se não for "Todas")
if decada_selecionada != 'Todas':
    decada_inicio, decada_fim = decadas[decada_selecionada]
    decada_df = decada_df[(decada_df['Year'] >= decada_inicio) & (decada_df['Year'] <= decada_fim)]

# Calculando vendas por região
vendas_por_regiao = pd.DataFrame({
    'Região': ['América do Norte', 'Europa', 'Japão', 'Outros'],
    'Vendas': [
        decada_df['NA_Sales'].sum(),
        decada_df['EU_Sales'].sum(),
        decada_df['JP_Sales'].sum(),
        decada_df['Other_Sales'].sum()
    ]
})

col1, col2 = st.columns(2)

with col1:
    # Gráfico de pizza
    fig_pizza = px.pie(
        vendas_por_regiao,
        names='Região',
        values='Vendas',
        title=f'Distribuição de Vendas por Região (Década: {decada_selecionada})',
        hover_data=['Vendas'],
        labels={'Vendas': 'Vendas (milhões)'}
    )
    fig_pizza.update_traces(textposition='inside', textinfo='percent+label')
    st.plotly_chart(fig_pizza, use_container_width=True)

with col2:
    # Treemap - Correção: usar opções de textinfo válidas para treemap
    fig_treemap = px.treemap(
        vendas_por_regiao,
        names='Região',
        values='Vendas',
        title=f'Distribuição de Vendas por Região (Década: {decada_selecionada})',
        hover_data=['Vendas'],
        color='Vendas',
        color_continuous_scale='RdBu'
    )
    # Corrigindo as opções de textinfo para treemap
    fig_treemap.update_traces(textinfo='label+value+percent entry')
    st.plotly_chart(fig_treemap, use_container_width=True)

# Popularidade de Gêneros - Row 4
st.header("Popularidade de Gêneros")

# Preparando dados
vendas_genero = filtro_df.groupby('Genre').agg({
    'NA_Sales': 'sum',
    'EU_Sales': 'sum',
    'JP_Sales': 'sum',
    'Other_Sales': 'sum',
    'Global_Sales': 'sum'
}).reset_index().sort_values('Global_Sales', ascending=False)

# Botões para alternar entre exibições
regiao_view = st.radio(
    "Visualizar vendas por:",
    ["Global", "Comparar Regiões"],
    horizontal=True
)

if regiao_view == "Global":
    # Gráfico de barras para vendas globais por gênero
    fig_genero_global = px.bar(
        vendas_genero,
        x='Genre',
        y='Global_Sales',
        title='Vendas Globais por Gênero (milhões)',
        labels={'Genre': 'Gênero', 'Global_Sales': 'Vendas Globais (milhões)'},
        color='Global_Sales',
        color_continuous_scale='Viridis'
    )
    st.plotly_chart(fig_genero_global, use_container_width=True)
else:
    # Dados para gráfico empilhado
    melted_genero = pd.melt(
        vendas_genero,
        id_vars=['Genre'],
        value_vars=['NA_Sales', 'EU_Sales', 'JP_Sales', 'Other_Sales'],
        var_name='Região',
        value_name='Vendas'
    )
    
    # Mapeando códigos para nomes mais amigáveis
    melted_genero['Região'] = melted_genero['Região'].map({
        'NA_Sales': 'América do Norte',
        'EU_Sales': 'Europa',
        'JP_Sales': 'Japão',
        'Other_Sales': 'Outros'
    })
    
    # Gráfico de barras empilhadas
    fig_genero_regiao = px.bar(
        melted_genero,
        x='Genre',
        y='Vendas',
        color='Região',
        title='Vendas por Gênero e Região (milhões)',
        labels={'Genre': 'Gênero', 'Vendas': 'Vendas (milhões)', 'Região': 'Região'},
        barmode='stack'
    )
    st.plotly_chart(fig_genero_regiao, use_container_width=True)

# Tendências Temporais - Row 5
st.header("Tendências Temporais")

# Agrupando dados por ano
vendas_por_ano = filtro_df.dropna(subset=['Year']).groupby('Year').agg({
    'Global_Sales': 'sum',
    'NA_Sales': 'sum',
    'EU_Sales': 'sum',
    'JP_Sales': 'sum',
    'Other_Sales': 'sum',
    'Name': 'count'
}).reset_index()

vendas_por_ano['Year'] = vendas_por_ano['Year'].astype(int)
vendas_por_ano = vendas_por_ano.sort_values('Year')

# Gráfico de linha
fig_tendencia = px.line(
    vendas_por_ano,
    x='Year',
    y='Global_Sales',
    title='Tendência de Vendas Globais ao Longo do Tempo',
    labels={'Year': 'Ano', 'Global_Sales': 'Vendas Globais (milhões)'},
    markers=True
)

# Adicionando linha de contagem de jogos (eixo Y secundário)
fig_tendencia.add_scatter(
    x=vendas_por_ano['Year'],
    y=vendas_por_ano['Name'],
    name='Número de Jogos',
    yaxis='y2',
    line=dict(color='red', dash='dot')
)

# Configurando eixo Y secundário
fig_tendencia.update_layout(
    yaxis2=dict(
        title='Número de Jogos',
        overlaying='y',
        side='right'
    ),
    legend=dict(
        orientation='h',
        yanchor='bottom',
        y=1.02,
        xanchor='right',
        x=1
    )
)

st.plotly_chart(fig_tendencia, use_container_width=True)

# Busca de Jogos - Row 6
st.header("Busca de Jogos")

# Campo de busca
busca = st.text_input("Digite o nome do jogo para buscar:")

if busca:
    # Pesquisa por jogos que contenham o termo de busca (case-insensitive)
    resultados = df[df['Name'].str.contains(busca, case=False)]
    
    if not resultados.empty:
        st.write(f"Encontrados {len(resultados)} resultados para '{busca}':")
        
        # Exibindo resultados em uma tabela
        st.dataframe(
            resultados[['Name', 'Platform', 'Year', 'Genre', 'Publisher', 'Global_Sales']],
            hide_index=True,
            use_container_width=True
        )
        
        # Seleção de jogo para análise detalhada
        jogos_encontrados = resultados['Name'].unique().tolist()
        jogo_selecionado = st.selectbox("Selecione um jogo para análise detalhada:", jogos_encontrados)
        
        if jogo_selecionado:
            # Filtrando dados do jogo selecionado
            jogo_df = resultados[resultados['Name'] == jogo_selecionado]
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Informações do jogo
                st.subheader(f"Detalhes do Jogo: {jogo_selecionado}")
                
                info_df = jogo_df.head(1)
                st.write(f"**Plataforma:** {info_df['Platform'].iloc[0]}")
                st.write(f"**Ano de Lançamento:** {int(info_df['Year'].iloc[0]) if not pd.isna(info_df['Year'].iloc[0]) else 'Desconhecido'}")
                st.write(f"**Gênero:** {info_df['Genre'].iloc[0]}")
                st.write(f"**Editora:** {info_df['Publisher'].iloc[0]}")
                st.write(f"**Vendas Globais:** {info_df['Global_Sales'].iloc[0]:.2f} milhões")
            
            with col2:
                # Gráfico de vendas por região para o jogo selecionado
                vendas_jogo = pd.DataFrame({
                    'Região': ['América do Norte', 'Europa', 'Japão', 'Outros'],
                    'Vendas': [
                        jogo_df['NA_Sales'].iloc[0],
                        jogo_df['EU_Sales'].iloc[0],
                        jogo_df['JP_Sales'].iloc[0],
                        jogo_df['Other_Sales'].iloc[0]
                    ]
                })
                
                fig_jogo = px.pie(
                    vendas_jogo,
                    names='Região',
                    values='Vendas',
                    title=f'Distribuição de Vendas por Região: {jogo_selecionado}',
                    hole=.3
                )
                fig_jogo.update_traces(textposition='inside', textinfo='percent+label')
                st.plotly_chart(fig_jogo, use_container_width=True)
    else:
        st.warning(f"Nenhum resultado encontrado para '{busca}'.")

# Rodapé
st.markdown("---")
st.markdown("Dashboard criado com Streamlit e Plotly. Dados de vendas de videogames.")