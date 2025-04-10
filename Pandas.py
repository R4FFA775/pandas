import pandas as pd

# Importar o DataFrame
df = pd.read_csv('Ecommerce_Consumer_Behavior_Analysis_Data.csv')

def limpar_e_converter_valor(valor):
    if isinstance(valor, str):
        valor = valor.replace('$', '').replace(',', '')
    try:
        return float(valor)
    except ValueError:
        return None

# Aplicar a limpeza e conversão à coluna 'Purchase_Amount'
df['Purchase_Amount'] = df['Purchase_Amount'].apply(limpar_e_converter_valor)

def analise_publico_alvo():
    print("\n=== ANÁLISE DEMOGRÁFICA DO PÚBLICO ALVO ===")

    # Dicionário de mapeamento para tradução
    traducao_genero = {'Female': 'Feminino', 'Male': 'Masculino'}
    traducao_estado_civil = {'Single': 'Solteiro', 'Married': 'Casado', 'Divorced': 'Divorciado', 'Widowed': 'Viúvo'}
    traducao_nivel_renda = {'High': 'Alto', 'Middle': 'Médio', 'Low': 'Baixo'}

    # 1. Análise de gênero
    print("\n--- Análise de Gênero ---")
    print("\nQuantidade por gênero:")
    print(df['Gender'].map(traducao_genero).value_counts())
    print("\nPorcentagem por gênero:")
    print((df['Gender'].map(traducao_genero).value_counts(normalize=True) * 100).round(2), "%")

    # 2. Análise de estado civil
    print("\n--- Análise de Estado Civil ---")
    qtd_solteiros = df['Marital_Status'].map(traducao_estado_civil).value_counts().get('Solteiro', 0)
    print(f"\nQuantidade de clientes solteiros: {qtd_solteiros}")

    # 3. Análise de idade
    print("\n--- Análise de Idade ---")
    idade_media = df['Age'].mean()
    print(f"\nIdade média dos clientes: {idade_media:.2f} anos")

    # 4. Idade média por nível de renda
    print("\n--- Idade Média por Nível de Renda ---")
    print(df.groupby('Income_Level')['Age'].mean().rename(index=traducao_nivel_renda).round(2))

    # 5. Idade média por gênero
    print("\n--- Idade Média por Gênero ---")
    print(df.groupby(df['Gender'].map(traducao_genero))['Age'].mean().round(2))

    # 6. Proporção de clientes por nível de renda
    print("\n--- Proporção de Clientes por Nível de Renda ---")
    prop_renda = df['Income_Level'].map(traducao_nivel_renda).value_counts(normalize=True) * 100
    print(prop_renda.round(2), "%")

    # 7. Categoria de produto mais comprada
    print("\n--- Categoria de Produto Mais Comprada ---")
    categoria_mais_comprada = df['Purchase_Category'].value_counts().idxmax()
    print(f"\nCategoria de produto mais comprada: {categoria_mais_comprada}")

    # 8. Valor médio gasto por compra
    print("\n--- Valor Médio Gasto por Compra ---")
    valor_medio_compra = df['Purchase_Amount'].mean()
    print(f"\nValor médio gasto por compra: ${valor_medio_compra:.2f}")

    # 9. Método de pagamento mais usado
    print("\n--- Método de Pagamento Mais Usado ---")
    metodo_pagamento_mais_usado = df['Payment_Method'].value_counts().idxmax()
    print(f"\nMétodo de pagamento mais usado: {metodo_pagamento_mais_usado}")

    # 10. Compras online vs. loja física
    print("\n--- Compras Online vs. Loja Física ---")
    compras_por_canal = df['Purchase_Channel'].value_counts()
    print(compras_por_canal)

    # 11. Avaliação média dos produtos
    print("\n--- Avaliação Média dos Produtos ---")
    avaliacao_media = df['Product_Rating'].mean()
    print(f"\nAvaliação média dos produtos: {avaliacao_media:.2f}")

    # 12. Valor médio de compra por gênero
    print("\n--- Valor Médio de Compra por Gênero ---")
    valor_medio_por_genero = df.groupby(df['Gender'].map(traducao_genero))['Purchase_Amount'].mean()
    print(valor_medio_por_genero.round(2))

    # 13. Valor médio de compra por estado civil
    print("\n--- Valor Médio de Compra por Estado Civil ---")
    valor_medio_por_estado_civil = df.groupby(df['Marital_Status'].map(traducao_estado_civil))['Purchase_Amount'].mean()
    print(valor_medio_por_estado_civil.round(2))

if __name__ == "__main__":
    analise_publico_alvo()