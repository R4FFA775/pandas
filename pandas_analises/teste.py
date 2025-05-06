import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st
import os

# Configurando a página
st.set_page_config(page_title="Análise E-commerce", layout="wide")
st.title("Análise de Dados E-commerce")

# Carregando os dados com caminho correto
caminho_arquivo = os.path.join(os.path.dirname(__file__), '..', 'ecommece', 'Ecommerce_Consumer_Behavior_Analysis_Data (1).csv')
df = pd.read_csv(caminho_arquivo)
st.success("Dados carregados com sucesso!")

# 1. Distribuição de Idade
st.header("1. Distribuição de Idade")
fig1, ax1 = plt.subplots(figsize=(10, 6))
sns.histplot(data=df, x='Age', kde=True, ax=ax1)
plt.title('Distribuição de Idade dos Clientes')
plt.xlabel('Idade')
plt.ylabel('Contagem')
st.pyplot(fig1)

# 2. Proporção de Gênero
st.header("2. Proporção de Gênero")
fig2, ax2 = plt.subplots(figsize=(8, 6))
gender_counts = df['Gender'].value_counts()
gender_percentages = (gender_counts / len(df) * 100).round(2)

sns.countplot(data=df, x='Gender', hue='Gender', palette='pastel', legend=False, ax=ax2)
plt.title('Proporção de Gênero')

for i in range(len(gender_counts)):
    plt.text(i, gender_counts.iloc[i], f'{gender_percentages.iloc[i]}%',
             ha='center', va='bottom')
st.pyplot(fig2)

# 3. Nível de Renda vs. Valor Gasto
st.header("3. Nível de Renda vs. Valor Gasto")
fig3, ax3 = plt.subplots(figsize=(12, 6))
sns.boxplot(data=df, x='Income_Level', y='Purchase_Amount', ax=ax3)
plt.title('Valor Gasto por Nível de Renda')
plt.xlabel('Nível de Renda')
plt.ylabel('Valor Gasto ($)')
st.pyplot(fig3)

# 4. Satisfação do Cliente por Gênero
st.header("4. Satisfação do Cliente por Gênero")
fig4, ax4 = plt.subplots(figsize=(10, 6))
sns.histplot(data=df, x='Customer_Satisfaction', hue='Gender', multiple="layer", alpha=0.6, ax=ax4)
plt.title('Distribuição da Satisfação do Cliente por Gênero')
plt.xlabel('Nível de Satisfação (1-10)')
plt.ylabel('Contagem')
st.pyplot(fig4)

# 5. Tempo de Pesquisa vs. Avaliação do Produto
st.header("5. Tempo de Pesquisa vs. Avaliação do Produto")
fig5, ax5 = plt.subplots(figsize=(12, 8))
sns.scatterplot(data=df, 
                x='Time_Spent_on_Product_Research(hours)', 
                y='Product_Rating',
                hue='Purchase_Category',
                alpha=0.6,
                ax=ax5)
plt.title('Relação entre Tempo de Pesquisa e Avaliação do Produto')
plt.xlabel('Tempo de Pesquisa (horas)')
plt.ylabel('Avaliação do Produto')
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
st.pyplot(fig5)