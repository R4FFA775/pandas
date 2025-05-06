import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

caminho_arquivo = os.path.join(os.path.dirname(__file__), 'Ecommerce_Consumer_Behavior_Analysis_Data (1).csv')

df = pd.read_csv(caminho_arquivo)
print("Dados carregados com sucesso!")

# 1. Distribuição de Idade
plt.figure(figsize=(10, 6))
sns.histplot(data=df, x='Age', kde=True)
plt.title('Distribuição de Idade dos Clientes')
plt.xlabel('Idade')
plt.ylabel('Contagem')
plt.savefig('grafico_idade.png')
plt.close()

# 2. Proporção de Gênero
plt.figure(figsize=(8, 6))
gender_counts = df['Gender'].value_counts()
gender_percentages = (gender_counts / len(df) * 100).round(2)

sns.countplot(data=df, x='Gender', hue='Gender', palette='pastel', legend=False)
plt.title('Proporção de Gênero')

for i in range(len(gender_counts)):
    plt.text(i, gender_counts.iloc[i], f'{gender_percentages.iloc[i]}%',
             ha='center', va='bottom')
plt.savefig('grafico_genero.png')
plt.close()

# 3. Nível de Renda vs. Valor Gasto
plt.figure(figsize=(12, 6))
sns.boxplot(data=df, x='Income_Level', y='Purchase_Amount')
plt.title('Valor Gasto por Nível de Renda')
plt.xlabel('Nível de Renda')
plt.ylabel('Valor Gasto ($)')
plt.savefig('grafico_renda.png')
plt.close()

# 4. Satisfação do Cliente por Gênero
plt.figure(figsize=(10, 6))
sns.histplot(data=df, x='Customer_Satisfaction', hue='Gender', multiple="layer", alpha=0.6)
plt.title('Distribuição da Satisfação do Cliente por Gênero')
plt.xlabel('Nível de Satisfação (1-10)')
plt.ylabel('Contagem')
plt.savefig('grafico_satisfacao.png')
plt.close()

# 5. Tempo de Pesquisa vs. Avaliação do Produto
plt.figure(figsize=(12, 8))
sns.scatterplot(data=df, 
                x='Time_Spent_on_Product_Research(hours)', 
                y='Product_Rating',
                hue='Purchase_Category',
                alpha=0.6)
plt.title('Relação entre Tempo de Pesquisa e Avaliação do Produto')
plt.xlabel('Tempo de Pesquisa (horas)')
plt.ylabel('Avaliação do Produto')
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.savefig('grafico_pesquisa_avaliacao.png')
plt.close()

# 6. Lealdade à Marca por Canal de Compra
plt.figure(figsize=(12, 6))
sns.violinplot(data=df, 
               x='Purchase_Channel', 
               y='Brand_Loyalty',
               hue='Discount_Used',
               split=True)
plt.title('Lealdade à Marca por Canal de Compra')
plt.xlabel('Canal de Compra')
plt.ylabel('Lealdade à Marca')
plt.savefig('grafico_lealdade_canal.png')
plt.close()

# 7. Impacto do Programa de Fidelidade
plt.figure(figsize=(10, 6))
sns.barplot(data=df, 
            x='Customer_Loyalty_Program_Member', 
            y='Frequency_of_Purchase',
            hue='Gender')
plt.title('Frequência de Compra por Participação no Programa de Fidelidade')
plt.xlabel('Membro do Programa de Fidelidade')
plt.ylabel('Frequência de Compra')
plt.savefig('grafico_programa_fidelidade.png')
plt.close()

# 8. Método de Pagamento vs. Dispositivo
plt.figure(figsize=(10, 8))
crosstab = pd.crosstab(df['Payment_Method'], df['Device_Used_for_Shopping'])
sns.heatmap(crosstab, annot=True, fmt='d', cmap='YlGnBu')
plt.title('Relação entre Método de Pagamento e Dispositivo')
plt.xlabel('Dispositivo Utilizado')
plt.ylabel('Método de Pagamento')
plt.tight_layout()
plt.savefig('grafico_pagamento_dispositivo.png')
plt.close()

# 9. Segmentação por Localização
plt.figure(figsize=(15, 10))
g = sns.FacetGrid(df, col="Location", col_wrap=3, height=4, aspect=1.5)
g.map_dataframe(sns.scatterplot, x="Age", y="Purchase_Amount")
g.fig.suptitle("Valor de Compra vs Idade por Localização", y=1.02)
plt.tight_layout()
g.savefig('grafico_segmentacao_localizacao.png', bbox_inches='tight', dpi=300)
plt.close()

# 10. Tendências Temporais
# Convertendo para datetime e tratando possíveis erros
df['Time_of_Purchase'] = pd.to_datetime(df['Time_of_Purchase'], errors='coerce')
# Removendo valores nulos se houver
df_temp = df.dropna(subset=['Time_of_Purchase'])
# Calculando média mensal
monthly_avg = df_temp.groupby(df_temp['Time_of_Purchase'].dt.to_period('M'))['Purchase_Amount'].mean().reset_index()
monthly_avg['Time_of_Purchase'] = monthly_avg['Time_of_Purchase'].astype(str)

plt.figure(figsize=(12, 6))
sns.lineplot(data=monthly_avg, x='Time_of_Purchase', y='Purchase_Amount')
plt.title('Média Mensal de Valor de Compra')
plt.xlabel('Mês')
plt.ylabel('Valor Médio de Compra ($)')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('grafico_tendencias_temporais.png', bbox_inches='tight', dpi=300)
plt.close()

# 11. Clusterização com Pairplot
# Selecionando apenas variáveis numéricas e limitando o dataset se necessário
numeric_cols = ['Age', 'Purchase_Amount', 'Customer_Satisfaction', 
                'Time_Spent_on_Product_Research(hours)', 'Product_Rating']
plot_data = df[numeric_cols + ['Shipping_Preference']].copy()

# Criando o pairplot
pairplot = sns.pairplot(plot_data, 
                        vars=numeric_cols, 
                        hue='Shipping_Preference', 
                        diag_kind='kde',
                        plot_kws={'alpha': 0.6})
pairplot.fig.suptitle('Análise de Correlação entre Variáveis', y=1.02)
pairplot.savefig('grafico_pairplot.png', bbox_inches='tight', dpi=300)
plt.close()
