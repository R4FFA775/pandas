import pandas as pd

df = pd.read_csv("vgsales.csv")

print("\n1. Dimensões do Dataset:")
print(f"Linhas: {df.shape[0]}")
print(f"Colunas: {df.shape[1]}")

print("\n2. Total de vendas Globais:")
print(f"{df['Global_Sales'].sum():.2f} milhões de cópias")


print("\n3. 10 primeiros jogos")
print(df.head(10))


print("\n4. Quantidade de jogos em 2006:")
print(len(df[df['Year'] == 2006]))

print("\n5. Jogos Nintendo com vendas EU > 10:")
print(df[(df['Publisher'] == 'Nintendo') & (df['EU_Sales'] > 10)])


print("\n6. Jogos do gênero Racing:")
print(df[df['Genre'] == 'Racing'])


print("\n7. Média de vendas na América do Norte:")
print(f"{df['NA_Sales'].mean():.2f} milhões")


print("\n8. Editora mais frequente:")
print(df['Publisher'].value_counts().head(1))


print("\n9. Quantidade de gêneros diferentes:")
print(len(df['Genre'].unique()))

# 10. Top 5 jogos JP
print("\n10. Top 5 jogos com maiores vendas no Japão:")
print(df.nlargest(5, 'JP_Sales')[['Name', 'JP_Sales']])

# 11. Ordenar por ano decrescente
df_sorted = df.sort_values('Year', ascending=False)
print("\n11. Dataset ordenado por ano:")
print(df_sorted.head())

# 12. Maior diferença NA-JP
df['NA_JP_Diff'] = df['NA_Sales'] - df['JP_Sales']
print("\n12. Jogo com maior diferença NA-JP:")
print(df.nlargest(1, 'NA_JP_Diff')[['Name', 'NA_Sales', 'JP_Sales', 'NA_JP_Diff']])

# 13. Gênero com mais vendas globais
genre_sales = df.groupby('Genre')['Global_Sales'].sum()
print("\n13. Gênero com mais vendas globais:")
print(genre_sales.nlargest(1))

# 14. Valores faltantes em Year
print("\n14. Valores faltantes em Year:")
print(df['Year'].isna().sum())

# 15. Jogos com vendas > 30M
print("\n15. Jogos com vendas globais > 30M:")
print(len(df[df['Global_Sales'] > 30]))

# 16. Ranking Mario Kart Wii
print("\n16. Posição de Mario Kart Wii:")
print(df[df['Name'] == 'Mario Kart Wii']['Rank'].values[0])

# 17. Dados do terceiro jogo
print("\n17. Dados do terceiro colocado:")
print(df[df['Rank'] == 3])

# 18. Nova coluna Total_Regional
df['Total_Regional'] = df['NA_Sales'] + df['EU_Sales'] + df['JP_Sales'] + df['Other_Sales']

# 19. Diferença percentual primeiro jogo
first_game = df.iloc[0]
diff_percent = ((first_game['Global_Sales'] - first_game['Total_Regional']) / first_game['Global_Sales']) * 100
print("\n19. Diferença percentual do primeiro jogo:")
print(f"{diff_percent:.2f}%")

# Desafios:

# 20. Jogo com Other_Sales mais próximo da média
mean_other = df['Other_Sales'].mean()
df['Other_Diff'] = abs(df['Other_Sales'] - mean_other)
print("\n20. Jogo com Other_Sales mais próximo da média:")
print(df.nsmallest(1, 'Other_Diff')[['Name', 'Other_Sales']])

# 21. Jogos com NA > EU+JP
df['EU_JP_Combined'] = df['EU_Sales'] + df['JP_Sales']
print("\n21. Jogos com NA > EU+JP combinados:")
print(df[df['NA_Sales'] > df['EU_JP_Combined']].head())

# 22. Publisher com maior média de vendas globais
publisher_avg = df.groupby('Publisher')['Global_Sales'].mean()
print("\n22. Publisher com maior média de vendas:")
print(publisher_avg.nlargest(1))

# 23. Jogo com maior % vendas JP
df['JP_Percent'] = (df['JP_Sales'] / df['Global_Sales']) * 100
print("\n23. Jogo com maior % de vendas no Japão:")
print(df.nlargest(1, 'JP_Percent')[['Name', 'JP_Percent']])

# 24. Jogos em 3+ plataformas
publisher_platforms = df.groupby('Publisher')['Platform'].nunique()
print("\n24. Publishers com jogos em 3+ plataformas:")
print(len(publisher_platforms[publisher_platforms >= 3]))

# 25. Jogo mais antigo com vendas > 20M
old_games = df[df['Global_Sales'] > 20].nsmallest(1, 'Year')
print("\n25. Jogo mais antigo com vendas > 20M:")
print(old_games[['Name', 'Year', 'Global_Sales']])
