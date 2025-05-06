import pandas as pd

df = pd.read_csv("vgsales.csv")

print("\n" + "="*50)
print("ANÁLISE DE VENDAS DE VIDEOGAMES")
print("="*50)

print("\nINFORMAÇÕES BÁSICAS DO DATASET")
print("-"*30)
print("1. Dimensões do Dataset")
print(f"Total de Linhas: {df.shape[0]}")
print(f"Total de Colunas: {df.shape[1]}")

print("\nVENDAS E ESTATÍSTICAS")
print("-"*30)
print("2. Total de Vendas Globais")
print(f"Total: {df['Global_Sales'].sum():.2f} milhões de cópias")

print("\n3. Ranking - Top 10 Jogos")
print("-"*30)
print(df.head(10))

print("\nFILTROS E BUSCAS")
print("-"*30)
print("4. Jogos lançados em 2006")
print(f"Total encontrado: {len(df[df['Year'] == 2006])} jogos")

print("\n5. Jogos Nintendo com vendas europeias > 10M")
print("-"*30)
print(df[(df['Publisher'] == 'Nintendo') & (df['EU_Sales'] > 10)])

print("\n6. Lista de Jogos de Corrida")
print("-"*30)
print(df[df['Genre'] == 'Racing'])

print("\nESTATÍSTICAS DE MERCADO")
print("-"*30)
print("7. Média de Vendas na América do Norte")
print(f"Média: {df['NA_Sales'].mean():.2f} milhões de cópias")

print("\n8. Publisher Mais Frequente")
print("-"*30)
print(df['Publisher'].value_counts().head(1))

print("\nANÁLISE DE CATEGORIAS")
print("-"*30)
print("9. Diversidade de Gêneros")
print(f"Total de gêneros diferentes: {len(df['Genre'].unique())}")



print("\nDESAFIOS ESPECIAIS")
print("="*50)
# ... incluir os desafios com o mesmo padrão de formatação ...