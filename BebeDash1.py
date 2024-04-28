import pandas as pd
import streamlit as st 
import plotly.express as px


# Função para carregar e preparar os dados
 # Usando o novo decorador de cache

@st.cache_data  # Corrigindo o decorador para o cache correto
def load_data():
    data = pd.read_excel("Bebe")
    data['Day'] = pd.to_datetime(data['Day'], errors='coerce')
    return data

data = load_data()

# Verifica se há datas inválidas
if data['Day'].isnull().any():
    st.error('Alguns valores de data estão faltando ou foram convertidos incorretamente.')

# Título do Dashboard
st.title('Dashboard de Análise de Campanha de Vendas')

# Filtro de datas
if 'Day' in data:
    start_date, end_date = st.sidebar.date_input("Selecionar intervalo de datas", [data['Day'].min(), data['Day'].max()])
    if start_date and end_date:
        # Convertendo start_date e end_date para datetime para compatibilidade
        start_date = pd.to_datetime(start_date)
        end_date = pd.to_datetime(end_date)

        filtered_data = data[(data['Day'] >= start_date) & (data['Day'] <= end_date)]

        # Exibindo estatísticas básicas dos dados filtrados
        st.header('Estatísticas Básicas')
        st.write(filtered_data.describe())

        # Gráfico de Linhas para Alcance por Dia
        st.header('Alcance por Dia')
        fig = px.line(filtered_data, x='Day', y='Reach', title='Alcance por Dia')
        st.plotly_chart(fig)

        # Gráfico de Linhas para Gasto por Dia
        st.header('Gasto por Dia')
        fig2 = px.line(filtered_data, x='Day', y='Amount Spent', title='Gasto por Dia')
        st.plotly_chart(fig2)

          # Gráfico de Barras para Link Clicks
        st.header('Distribuição de Cliques por Link')
        fig3 = px.bar(filtered_data, x='Day', y='Link Clicks', title='Cliques por Link', labels={'Day': 'Dia', 'Link Clicks': 'Cliques nos Links'})
        st.plotly_chart(fig3)


        # Opção para download dos dados filtrados
        st.sidebar.header('Baixar Dados Filtrados')
        st.sidebar.download_button(label="Baixar dados como CSV", data=filtered_data.to_csv(index=False), file_name='dados_filtrados.csv', mime='text/csv')
