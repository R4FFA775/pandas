import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import sqlite3
from conexao import criar_banco

def adicionar_transacao(data, tipo, categoria, valor, descricao):
    conn = sqlite3.connect('financas.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO transacoes (data, tipo, categoria, valor, descricao)
        VALUES (?, ?, ?, ?, ?)
    ''', (data, tipo, categoria, valor, descricao))
    conn.commit()
    conn.close()

def carregar_transacoes():
    conn = sqlite3.connect('financas.db')
    return pd.read_sql_query("SELECT * FROM transacoes", conn)

def main():
    criar_banco()
    st.title("Gerenciador Financeiro")
    
    menu = st.sidebar.selectbox(
        "Selecione uma opção",
        ["Adicionar Transação", "Dashboard"]
    )
    
    if menu == "Adicionar Transação":
        st.subheader("Nova Transação")
        
        data = st.date_input("Data")
        tipo = st.selectbox("Tipo", ["Receita", "Despesa"])
        categoria = st.selectbox("Categoria", ["Salário", "Alimentação", "Transporte", "Lazer", "Outros"])
        valor = st.number_input("Valor", min_value=0.0)
        descricao = st.text_input("Descrição")
        
        if st.button("Adicionar"):
            adicionar_transacao(data, tipo, categoria, valor, descricao)
            st.success("Transação adicionada com sucesso!")
    
    else:  # Dashboard
        st.subheader("Dashboard Financeiro")
        
        df = carregar_transacoes()
        if not df.empty:
            # Métricas
            total_receitas = df[df['tipo'] == 'Receita']['valor'].sum()
            total_despesas = df[df['tipo'] == 'Despesa']['valor'].sum()
            saldo = total_receitas - total_despesas
            
            col1, col2, col3 = st.columns(3)
            col1.metric("Total Receitas", f"R$ {total_receitas:.2f}")
            col2.metric("Total Despesas", f"R$ {total_despesas:.2f}")
            col3.metric("Saldo", f"R$ {saldo:.2f}")
            
            # Gráficos
            df['data'] = pd.to_datetime(df['data'])
            
            # Gráfico de linha temporal
            fig_linha = px.line(df, x='data', y='valor', color='tipo',
                              title='Transações ao longo do tempo')
            st.plotly_chart(fig_linha)
            
            # Gráfico de pizza por categoria
            fig_pizza = px.pie(df, values='valor', names='categoria',
                             title='Distribuição por Categoria')
            st.plotly_chart(fig_pizza)

if __name__ == "__main__":
    main()