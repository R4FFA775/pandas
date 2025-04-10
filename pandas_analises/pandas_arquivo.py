import pandas as pd
df = pd.read_csv('Ecommerce_Consumer_Behavior_Analysis_Data.csv')

def limpar_e_converter_valor(valor):
    if isinstance(valor, str):
        valor = valor.replace('$', '').replace(',', '')
    try:
        return float(valor)
    except ValueError:
        return None
# Aplicar a limpeza e conversão à coluna 
df['Purchase_Amount'] = df['Purchase_Amount'].apply(limpar_e_converter_valor)

def analise_publico_alvo():
    print("\n=== ANÁLISE DEMOGRÁFICA DO PÚBLICO ALVO ===")

    print("\n--- Análise de Gênero ---")
    print("\nQuantidade por gênero:")
    print(df['Gender'].value_counts())
    print("\nPorcentagem por gênero:")
    print((df['Gender'].value_counts(normalize=True) * 100).round(2), "%")

    print("\n--- Análise de Estado Civil ---")
    qtd_solteiros = df['Marital_Status'].value_counts().get('Single', 0)
    print(f"\nQuantidade de clientes solteiros: {qtd_solteiros}")

    print("\n--- Análise de Idade ---")
    idade_media = df['Age'].mean()
    print(f"\nIdade média dos clientes: {idade_media:.2f} anos")

    print("\n--- Idade Média por Nível de Renda ---")
    print(df.groupby('Income_Level')['Age'].mean().round(2))

    print("\n--- Idade Média por Gênero ---")
    print(df.groupby('Gender')['Age'].mean().round(2))

    print("\n--- Proporção de Clientes por Nível de Renda ---")
    prop_renda = df['Income_Level'].value_counts(normalize=True) * 100
    print(prop_renda.round(2), "%")

    print("\n--- Categoria de Produto Mais Comprada ---")
    categoria_mais_comprada = df['Purchase_Category'].value_counts().idxmax()
    print(f"\nCategoria de produto mais comprada: {categoria_mais_comprada}")

    print("\n--- Valor Médio Gasto por Compra ---")
    valor_medio_compra = df['Purchase_Amount'].mean()
    print(f"\nValor médio gasto por compra: ${valor_medio_compra:.2f}")

    print("\n--- Método de Pagamento Mais Usado ---")
    metodo_pagamento_mais_usado = df['Payment_Method'].value_counts().idxmax()
    print(f"\nMétodo de pagamento mais usado: {metodo_pagamento_mais_usado}")

    print("\n--- Compras Online vs. Loja Física ---")
    compras_por_canal = df['Purchase_Channel'].value_counts()
    print(compras_por_canal)

    print("\n--- Avaliação Média dos Produtos ---")
    avaliacao_media = df['Product_Rating'].mean()
    print(f"\nAvaliação média dos produtos: {avaliacao_media:.2f}")

    print("\n--- Valor Médio de Compra por Gênero ---")
    valor_medio_por_genero = df.groupby('Gender')['Purchase_Amount'].mean()
    print(valor_medio_por_genero.round(2))

    print("\n--- Valor Médio de Compra por Estado Civil ---")
    valor_medio_por_estado_civil = df.groupby('Marital_Status')['Purchase_Amount'].mean()
    print(valor_medio_por_estado_civil.round(2))

if __name__ == "__main__":
    analise_publico_alvo()