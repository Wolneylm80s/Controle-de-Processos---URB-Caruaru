# =============================== Importação das bibliotecas =================================
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(
    layout="wide",  # 🔹 aqui define o layout wide
    initial_sidebar_state="expanded"  # opcional: abre o menu lateral
)

# ============================== Logos ===================================
fig1 = 'assets/logo_prefeitura.png'
fig2 = 'assets/logo_urb_Caruaru.jpg'

col1, col2, col3 = st.columns([1,1,1])

with col1:
    st.image(fig2, width=50)

with col2:
    st.image(fig1, use_container_width=True)

st.divider()
# ============================== Título inicial ===================================
st.markdown(
    """
    <h2 style='font-size: 50px; text-align: center;'>
    NÚMEROS DO ATENDIMENTO PRESENCIAL
    </h2>
    """,
    unsafe_allow_html=True
)
st.divider()

# 1 ============================== Lendo o base de dados excel ===================================

df_atend = pd.read_excel("assets\ATENDIMENTO - CALENDARIO.xlsx", sheet_name="QTDE_GERAL")

# Converter a coluna DATA para formato dd/mm/aa e as demais para formatos númericos:
df_atend["Data"] = pd.to_datetime(df_atend["Data"]).dt.strftime("%d/%m/%y")
df_atend['Normal'] = pd.to_numeric(df_atend['Normal'], errors='coerce')
df_atend['Prioridade'] = pd.to_numeric(df_atend['Prioridade'], errors='coerce')
df_atend['Total'] = pd.to_numeric(df_atend['Total'], errors='coerce')

# X =============================== Resultados parciais e gerais ==================================

# Somatório de valores totais de atendimento
normal_total = df_atend['Normal'].sum()
prioridade_total = df_atend['Prioridade'].sum()
total_atend = df_atend['Total'].sum()
media_atend = int(df_atend['Total'].mean())
median_atend = int(df_atend['Total'].median())

# X =============================== Gráfico de Pizza Número de atendimentos ==================================
col1, col2 = st.columns([3,1])

with col1:
    st.subheader("1. Número Total de Atendimentos x Perfil de Usuário")

    # Gráfico de pizza composição total de atendimentos:
    labels = ['Normal', 'Prioridade',]
    values = [normal_total, prioridade_total,]

    fig = go.Figure(data=[
        go.Pie(
            labels=labels, 
            values=values, 
            hole=0.5,
            textfont=dict(size=16)
            )
    ])

    # Ajustar legenda
    fig.update_layout(
        legend=dict(
            font=dict(size=16)  # aumenta fonte da legenda
        )
    )

    fig

with col2:
    st.metric("Total de Atendimentos", total_atend, border=True)
    st.metric("Atendimentos normais", normal_total, border=True)
    st.metric("Atendimentos Prioritários", prioridade_total, border=True)
    st.metric("Média Mensal", media_atend, border=True)
    st.metric("Mediana Mensal", median_atend, border=True)

st.markdown(
    "<p style='font-size: 12px;'><b>Nota: </b> Os dados apresentados foram coletados a partir da contagem do número de senhas entregues no atendimento presencial, realizado pela recepção da URB.</p>",
    unsafe_allow_html=True
)

st.markdown(
    """
    <div style="text-align: left; font-size: 12px; margin-top: 1px 0 0 ;">
        <b>Fonte:</b> 
        <a href="https://docs.google.com/spreadsheets/d/1NcembmrohbXdUUU01mjWGH5pVJs91hO6a1wyfiqCjW8/edit?gid=0#gid=0" target="_blank">
            Planilha de controle de atendimentos
        </a>
    </div>
    """,
    unsafe_allow_html=True
)

st.divider()


# X =============================== Gráfico de Barras quantidadde de atendimentos no ano de 2025 ==================================

st.subheader("2. Distribuição do número de atendimentos por perfil de usuário no ano de 2025")

# Criar gráfico de barras
fig = go.Figure(data=[
    go.Bar(name='Normal', x=df_atend['Mês'], y=df_atend['Normal'], marker_color="#557BCC"),
    go.Bar(name='Prioridade', x=df_atend['Mês'], y=df_atend['Prioridade'], marker_color="#71B5E6")
])

# Calcular média e mediana (somando as duas categorias para o total)
total_atend = df_atend['Normal'] + df_atend['Prioridade']
media = total_atend.mean()
mediana = total_atend.median()

# Adiciona linha de média
fig.add_trace(go.Scatter(
    x=df_atend['Mês'],
    y=[media]*len(df_atend),
    mode='lines',
    name='Média',
    line=dict(color='darkgreen', dash='dash')
))

# Adiciona linha de mediana
fig.add_trace(go.Scatter(
    x=df_atend['Mês'],
    y=[mediana]*len(df_atend),
    mode='lines',
    name='Mediana',
    line=dict(color='green', dash='dot')
))

# Anotação média - início do eixo X
fig.add_annotation(
    x=df_atend['Mês'].iloc[-1],  # último ponto no eixo x
    y=media,
    text=f"Média ({media:.0f})",
    showarrow=False,
    font=dict(color="darkgreen", size=16),
    align="left",
    xanchor="left",
    yanchor="bottom"
)

# Anotação mediana - início do eixo X
fig.add_annotation(
    x=df_atend['Mês'].iloc[-1],
    y=mediana,
    text=f"Mediana ({mediana:.0f})",
    showarrow=False,
    font=dict(color="green", size=16),
    align="left",
    xanchor="left",
    yanchor="bottom"
)

# Layout do gráfico
fig.update_layout(
    barmode='stack',
    template="plotly_white",
    legend=dict(
        font=dict(size=16)
    ),
    xaxis=dict(
        tickfont=dict(size=18)
    ),
    yaxis=dict(
        tickfont=dict(size=18)
    )
)

# Exibir no Streamlit
st.plotly_chart(fig, use_container_width=True)


st.markdown(
    """
    <div style="text-align: left; font-size: 12px; margin-top: 1px 0 0 ;">
        <b>Fonte:</b> 
        <a href="https://docs.google.com/spreadsheets/d/1NcembmrohbXdUUU01mjWGH5pVJs91hO6a1wyfiqCjW8/edit?gid=0#gid=0" target="_blank">
            Planilha de controle de atendimentos
        </a>
    </div>
    """,
    unsafe_allow_html=True
)

st.divider()


# X ============================== Exibição da tabela quantidade de atendimentos ===================================

st.subheader("3. Tabela com os números gerais do atendimento presencial")

# Selecionar colunas que vão aparecer
colunas_para_exibir = ["Mês", "Normal", "Prioridade", "Total"]
df_filtrado = df_atend[colunas_para_exibir].copy()

# Transformar todas as colunas de texto em maiúsculas
for col in df_filtrado.select_dtypes(include='object').columns:
    df_filtrado[col] = df_filtrado[col].str.upper()

# Função de estilo
def estilo(df_filtrado):
    return (
        df_filtrado.style
        .set_properties(**{'text-align': 'center', 'font-size': '16pt'})  # corpo da tabela
        .set_table_styles([
            {'selector': 'th', 'props': [('font-weight', 'bold'),
                                         ('text-align', 'center'),
                                         ('font-size', '18pt')]}  # cabeçalho
        ])
    )

# Exibir
st.dataframe(df_filtrado, use_container_width=True, hide_index=True)

st.markdown(
    """
    <div style="text-align: left; font-size: 12px; margin-top: 1px 0 0 ;">
        <b>Fonte:</b> 
        <a href="https://docs.google.com/spreadsheets/d/1NcembmrohbXdUUU01mjWGH5pVJs91hO6a1wyfiqCjW8/edit?gid=0#gid=0" target="_blank">
            Planilha de controle de atendimentos
        </a>
    </div>
    """,
    unsafe_allow_html=True
)