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
    NÚMEROS DO LICENCIAMENTO URBANO
    </h2>
    """,
    unsafe_allow_html=True
)
st.divider()

#  ============================== 1. Lendo a base de dados excel do Licenciamento Urbano ===================================

df_ctu = pd.read_excel(
    r"assets/NOVA_ PROCESSOS EM ANDAMENTO 2025  - CTU.xlsx",
    sheet_name=['GERAL 2025', 'SIMPLIFICADA 2025', 'COLEGIADO 2025', 'QUANTITATIVO', 'ANALISTAS']
)

df_ctu_geral = df_ctu['GERAL 2025']
df_ctu_simp = df_ctu['SIMPLIFICADA 2025']
df_ctu_col = df_ctu['COLEGIADO 2025']

#  ============================== 1.1. Formatando os dados de datas ===================================

# Converter a coluna DATA para formato dd/mm/aa e as demais para formatos númericos:
df_ctu_geral['DATA DE ENTRADA'] = pd.to_datetime(df_ctu_geral['DATA DE ENTRADA'], format='%d/%m/%Y')
df_ctu_geral['DATA DE APROVAÇÃO'] = pd.to_datetime(df_ctu_geral['DATA DE APROVAÇÃO'], format='%d/%m/%Y')

df_ctu_simp['DATA DE ENTRADA'] = pd.to_datetime(df_ctu_simp['DATA DE ENTRADA'], format='%d/%m/%Y')
df_ctu_simp['DATA DE APROVAÇÃO'] = pd.to_datetime(df_ctu_simp['DATA DE APROVAÇÃO'], format='%d/%m/%Y')

df_ctu_col['DATA DE ENTRADA'] = pd.to_datetime(df_ctu_col['DATA DE ENTRADA'], format='%d/%m/%Y')
df_ctu_col['DATA DE APROVAÇÃO'] = pd.to_datetime(df_ctu_col['DATA DE APROVAÇÃO'], format='%d/%m/%Y')

#  ============================== 1.2. Cálculos do total, aprovados, média e mediana ===================================

# Garantir linhas únicas
df_ctu_geral = df_ctu_geral.drop_duplicates()
df_ctu_simp = df_ctu_simp.drop_duplicates()
df_ctu_col = df_ctu_col.drop_duplicates()

# Cálculo do número total de linhas no CTU Geral/ Simplificado/ Colegiado:
total_linhas_geral = df_ctu_geral.shape[0]
total_linhas_simp = len(df_ctu_simp)
total_linhas_col = df_ctu_col.shape[0]

# Quantidade de processos aprovados e percentual tramitação geral
df_ctu_geral_aprov = df_ctu_geral[df_ctu_geral['STATUS'] == 'APROVADO']
qtde_aprov_ctu_geral = df_ctu_geral_aprov.shape[0]
perc_aprov_geral = qtde_aprov_ctu_geral / total_linhas_geral * 100

# Quantidade de processos aprovados e percentual tramitação simplificada
df_ctu_simp_aprov = df_ctu_simp[df_ctu_simp['STATUS'] == 'APROVADO']
qtde_aprov_ctu_simp = df_ctu_simp_aprov.shape[0]
perc_aprov_simp = qtde_aprov_ctu_simp / total_linhas_simp * 100

# Quantidade de processos aprovados e percentual tramitação colegiado
df_ctu_col_aprov = df_ctu_col[df_ctu_col['STATUS'] == 'APROVADO']
qtde_aprov_ctu_col = df_ctu_col_aprov.shape[0]
perc_aprov_col = qtde_aprov_ctu_col / total_linhas_col * 100

# Quantidade total de processos, aprovados e percentual tramitação colegiado
qtde_total_pu = total_linhas_geral + total_linhas_simp + total_linhas_col
qtde_aprov_pu = qtde_aprov_ctu_geral + qtde_aprov_ctu_simp + qtde_aprov_ctu_col
perc_aprov_pu = qtde_aprov_pu / qtde_total_pu * 100


# Cálculo da média e da mediana de dias para aprovação - tramitação geral
df_num_dias_geral = df_ctu_geral['DATA DE ENTRADA'] - df_ctu_geral['DATA DE APROVAÇÃO']
df_num_dias_geral.dropna(inplace=True)
media_dias_geral = df_num_dias_geral.mean()
median_dias_geral = df_num_dias_geral.median()

# Cálculo da média e da mediana de dias para aprovação - tramitação simplificada
df_num_dias_simp = df_ctu_simp['DATA DE ENTRADA'] - df_ctu_simp['DATA DE APROVAÇÃO']
df_num_dias_simp.dropna(inplace=True)
media_dias_simp = df_num_dias_simp.mean()
median_dias_simp = df_num_dias_simp.median()

# Cálculo da média e da mediana de dias para aprovação - tramitação colegiada
df_num_dias_col = df_ctu_col['DATA DE ENTRADA'] - df_ctu_col['DATA DE APROVAÇÃO']
df_num_dias_col.dropna(inplace=True)
media_dias_col = df_num_dias_col.mean()
median_dias_col = df_num_dias_col.median()

#  ============================== 2. Gráficos e visuais do L.U. ===================================

# ---------------------------------------- 2.1. Cartões com dados ----------------------------------------
st.subheader("1. Números gerais do Licenciamento Urbano - Ano 2025")

col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Total Geral", qtde_total_pu)
col2.metric("Tramitação geral", total_linhas_geral)
col3.metric("Tramitação simplificada", total_linhas_simp)
col4.metric("Tramitação colegiada", total_linhas_col)
col5.metric("Total Geral de Aprovados", qtde_aprov_pu, delta=f"{perc_aprov_pu:.2f}%")

st.divider()

# ---------------------------------------- 2.2. Quantidade de processos por tipo ----------------------------------------

st.subheader("2. Quantidade de processos urbanos de tramitação geral por tipo - Ano 2025")



# Geração de gráfico de quantidade por tipo de processos com plotly express (sem título)
fig = px.histogram(
    df_ctu_geral,
    x='ASSUNTO/TIPOLOGIA',
    color_discrete_sequence=['#1f77b4']  # azul mais suave
)

# Ordenar do maior para o menor
fig.update_xaxes(categoryorder='total descending')

# Adicionar rótulos
fig.update_traces(
    texttemplate='%{y}',
    textposition='outside',
    marker=dict(line=dict(color='black', width=1))  # contorno nas barras
)

# Melhorar layout (sem título + sem espaço extra em cima)
fig.update_layout(
    width=800,
    height=600,
    margin=dict(t=10),   # 🔹 reduz a margem superior (default ~100)
    xaxis_title='',
    yaxis_title='',
    uniformtext_minsize=16,
    uniformtext_mode='hide',
    bargap=0.3,
    plot_bgcolor='white',
    xaxis=dict(
        tickangle=45,
        tickfont=dict(size=14)
    ),
    yaxis=dict(
        range=[0, 500],
        tick0=0,
        dtick=100,
        gridcolor='lightgrey',
        zeroline=False
    )
)

st.plotly_chart(fig, use_container_width=True)  # 🔹 garante ajuste no Streamlit

st.markdown(
    "<p style='font-size: 12px;'><b>Nota: </b> Os dados apresentados foram coletados a partir da planilha de controle do licenciamento urbano, desenvolvida pela equipe da Gerência de Controle de processos.</p>",
    unsafe_allow_html=True
)

st.divider()

#  ============================== 3. Gráficos e visuais de Tramitação Geral ===================================

# ---------------------------------------- 3.1. Resultados parciais de tramitação geral ----------------------------------------

st.subheader("3. Resultados de processos de tramitação geral - Ano 2025")

col1, col2, col3, col4 = st.columns(4)
col1.metric("Tramitação geral", total_linhas_geral)
col2.metric("Total de aprovados", qtde_aprov_ctu_geral, delta=f"{perc_aprov_geral:.2f}%")
col3.metric("Média dias aprovação", abs(media_dias_geral).days)
col4.metric("Mediana dias aprovação", abs(median_dias_geral).days)

st.divider()


# ---------------------------------------- 3.2. Quantidade de processos de tramitação geral ----------------------------------------

st.subheader("3.1. Quantidade de processos urbanos de tramitação geral - Ano 2025")

import calendar

# Criar a coluna 'mes'
df_ctu_geral["mes"] = df_ctu_geral["DATA DE ENTRADA"].dt.month

# Contar a quantidade por mês e ordenar
contagem_meses = df_ctu_geral["mes"].value_counts().sort_index()

# Calcular média e mediana
media = contagem_meses.mean()
mediana = contagem_meses.median()

# Corrigir nomes dos meses (índices como int)
meses = [calendar.month_abbr[int(m)] for m in contagem_meses.index]

# Criar figura
fig = go.Figure()

# Barras
fig.add_trace(go.Bar(
    x=meses,
    y=contagem_meses.values,
    text=contagem_meses.values,
    textposition="outside",
    marker=dict(
        color = "#0B4C7A",
        line=dict(color="black", width=1)
    ),
    name="Quantidade"
))

# Linha da média
fig.add_hline(
    y=media,
    line_dash="dash",
    line_color="blue",
    annotation_text=f"Média ({media:.0f})",
    annotation_position="top left",
    annotation_font_size=16
)

# Linha da mediana
fig.add_hline(
    y=mediana,
    line_dash="dot",
    line_color="red",
    annotation_text=f"Mediana ({mediana:.0f})",
    annotation_position="top left",
    annotation_font_size=16
)

# Layout
fig.update_layout(
    xaxis_title="",
    yaxis_title="",
    template="plotly_white",
    bargap=0.3,  # espaçamento entre barras
    yaxis=dict(
        range=[0, max(contagem_meses.values) * 1.2]  # 20% acima do maior valor
    )
)

fig

st.markdown(
    "<p style='font-size: 12px;'><b>Nota: </b> Os dados apresentados foram coletados a partir da planilha de controle do licenciamento urbano, desenvolvida pela equipe da Gerência de Controle de processos.</p>",
    unsafe_allow_html=True
)

st.divider()

# ---------------------------------------- 3.3. Quantidade de processo tramitação geral por analista ----------------------------------------

# Contagem por tipo de processo
st.markdown(
    "<h3 style='text-align: left;'>3.2. Quantidade de protocolos de tramitação geral por analista </h3>",
    unsafe_allow_html=True
)

# Gráfico de processos ambientais na horizontal por tipo com plotly express

cont_proc_urb_ana = df_ctu_geral['ANALISTA'].value_counts().sort_values()

# Criar gráfico de barras horizontais
fig = go.Figure(go.Bar(
    x=cont_proc_urb_ana.values,
    y=cont_proc_urb_ana.index,
    orientation='h',
    text=cont_proc_urb_ana.values,
    textposition="outside",
    textfont=dict(size=16),
    marker=dict(color = "#0B4C7A", line=dict(color="black", width=1))
))

# Layout
fig.update_layout(
    template="plotly_white",
    height=len(cont_proc_urb_ana) * 50,  # altura automática (30 px por categoria)
    margin=dict(l=250),  # margem esquerda maior p/ textos longos
    yaxis=dict(
        tickfont=dict(size=16)       # <- aumenta a fonte dos tipos de processo
    ),
    xaxis=dict(
        tickfont=dict(size=14)       # opcional: aumenta a fonte dos valores no eixo X
    )
)

fig

st.markdown(
    "<p style='font-size: 12px;'><b>Nota: </b> Os dados apresentados foram coletados a partir da planilha de controle do licenciamento urbano, desenvolvida pela equipe da Gerência de Controle de processos.</p>",
    unsafe_allow_html=True
)

st.divider()

# ---------------------- 3.4. Gráfico de velocímetro e variação mensal ----------------------

col1, col2 = st.columns([1,2])

with col1:
    st.markdown(
    "<h3 style='text-align: center;'>3.3. Meta-1: Aprovação de licenças no máximo até 30 dias</h3>",
    unsafe_allow_html=True
)

# Converter para número de dias
    df_num_dias_geral = (df_ctu_geral['DATA DE APROVAÇÃO'] - df_ctu_geral['DATA DE ENTRADA']).dt.days.abs()

# Calcular média e mediana em dias
    media_dias_geral = df_num_dias_geral.mean()
    median_dias_geral = df_num_dias_geral.median()

    valor_gauge = round(media_dias_geral,0)

    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=valor_gauge,
        title={'text':""},
        delta={'reference': 30, 'increasing': {'color': "red"}, 'decreasing': {'color': "green"}},
        gauge={
            'axis': {'range': [0, 50]}, 
            'bar': {'color': "darkgreen"},
            'steps': [
                {'range': [0, 30], 'color': 'lightgreen'},
                {'range': [30, 50], 'color': 'lightcoral'}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 30
            }
        }
    ))

    # Adicionar mediana como anotação
    fig.add_annotation(
        x=0.5,
        y=0.20,
        text=f"Mediana: {median_dias_geral:.0f} dias",
        showarrow=False,
        font=dict(size=16, color="blue")
    )

    fig.update_layout(
        width=500,   # largura do gráfico
        height=400   # altura do gráfico
    )

    st.plotly_chart(fig, use_container_width=True)

# Gráfico de linhas da variação da média e da mediana:
with col2:
    st.markdown(
        "<h3 style='text-align: center;'>3.4. Variação Mensal da Média e Mediana de Dias para Aprovação</h3>",
        unsafe_allow_html=True
    )
    
    # Calcular diferença de dias
    df_num_dias_geral = (df_ctu_geral['DATA DE APROVAÇÃO'] - df_ctu_geral['DATA DE ENTRADA']).dt.days
    df_ctu_geral['dias'] = df_num_dias_geral

    # Extrair mês
    df_ctu_geral['mes'] = df_ctu_geral['DATA DE ENTRADA'].dt.month

    # Calcular média e mediana por mês
    df_variacao_mensal_geral = df_ctu_geral.groupby('mes')['dias'].agg(['mean', 'median']).reset_index()

    fig = go.Figure()

    # Linha da média
    fig.add_trace(go.Scatter(
        x=df_variacao_mensal_geral['mes'],
        y=df_variacao_mensal_geral['mean'],
        mode='lines+markers',
        name='Média',
        line=dict(color='green', width=2),
        marker=dict(size=8)
    ))

    # Linha da mediana
    fig.add_trace(go.Scatter(
        x=df_variacao_mensal_geral['mes'],
        y=df_variacao_mensal_geral['median'],
        mode='lines+markers',
        name='Mediana',
        line=dict(color='blue', width=2, dash='dot'),
        marker=dict(size=8)
    ))

     # Linha de meta de 30 dias
    fig.add_hline(
        y=30,
        line_dash="dash",             # linha pontilhada
        line_color="red",
        annotation_text="Meta 30 dias",
        annotation_position="top right",
        annotation_font=dict(size=16, color="red")
    )

    # Layout
    fig.update_layout(
        xaxis_title="Mês",
        yaxis_title="Dias",
        template="plotly_white",
        xaxis=dict(tickmode='linear'),
        height=450,
        legend=dict(
        font=dict(size=18)  # <- aumenta o tamanho da legenda
        )
    )

    # Exibir o gráfico **dentro da coluna**
    st.plotly_chart(fig, use_container_width=True)

st.markdown(
    "<p style='font-size: 12px;'><b>Nota: </b> Os dados apresentados foram coletados a partir da planilha de controle do licenciamento urbano, desenvolvida pela equipe da Gerência de Controle de processos.</p>",
    unsafe_allow_html=True
)

st.divider()

# ---------------------- 3.5. Tabela com processos tramitação geral ----------------------
st.subheader("3.5. Tabela com os processos de Licenciamento Urbano de tramitação geral")

# Selecionar colunas que vão aparecer
col_urb_geral_exibir = ["PROTOCOLO ", "ASSUNTO/TIPOLOGIA","DATA DE ENTRADA", "DATA DE APROVAÇÃO", "STATUS", "ANALISTA"]
df_filt_ctu_geral= df_ctu_geral[col_urb_geral_exibir]

# Remover linhas totalmente em branco
df_filt_ctu_geral = df_filt_ctu_geral.dropna(how="all")

# Formatar as datas no formato dd/mm/aaaa
df_filt_ctu_geral["DATA DE ENTRADA"] = df_filt_ctu_geral["DATA DE ENTRADA"].dt.strftime("%d/%m/%Y")
df_filt_ctu_geral["DATA DE APROVAÇÃO"] = df_filt_ctu_geral["DATA DE APROVAÇÃO"].dt.strftime("%d/%m/%Y")

# Função de estilo
def estilo(df_filtrado):
    return (
        df_filtrado.style
        .set_properties(**{'text-align': 'center'})  # centraliza o conteúdo
        .set_table_styles([                           # estiliza cabeçalho
            {'selector': 'th', 'props': [('font-weight', 'bold'), ('text-align', 'center')]}
        ])
    )

# Exibir
st.dataframe(df_filt_ctu_geral, use_container_width=True, hide_index=True)

st.markdown(
    "<p style='font-size: 12px;'><b>Nota: </b> Os dados apresentados foram coletados a partir da planilha de controle do cadastro imobiliário, desenvolvida pela equipe da Gerência de Controle de processos.</p>",
    unsafe_allow_html=True
)

st.divider()

# =================================================== Licença Simplificada ===================================================

# ---------------------------------------- 4.1. Resultados parciais de tramitação simplificada ----------------------------------------

st.subheader("4. Resultados de processos de tramitação simplificada - Ano 2025")

col1, col2, col3, col4 = st.columns(4)
col1.metric("Tramitação simplificada", total_linhas_simp)
col2.metric("Total de aprovados", qtde_aprov_ctu_simp, delta=f"{perc_aprov_simp:.2f}%")
col3.metric("Média dias aprovação", abs(media_dias_simp).days)
col4.metric("Mediana dias aprovação", abs(median_dias_simp).days)

st.divider()

# ---------------------------------------- 4.2. Quantidade de processos de tramitação simplificada ----------------------------------------

st.subheader("4.1. Quantidade de processos urbanos de tramitação simplificada - Ano 2025")

import calendar

# Criar a coluna 'mes'
df_ctu_simp["mes"] = df_ctu_simp["DATA DE ENTRADA"].dt.month

# Contar a quantidade por mês e ordenar
contagem_meses_simp = df_ctu_simp["mes"].value_counts().sort_index()

# Calcular média e mediana
media = contagem_meses_simp.mean()
mediana = contagem_meses_simp.median()

# Corrigir nomes dos meses (índices como int)
meses = [calendar.month_abbr[int(m)] for m in contagem_meses_simp.index]

# Criar figura
fig = go.Figure()

# Barras
fig.add_trace(go.Bar(
    x=meses,
    y=contagem_meses_simp.values,
    text=contagem_meses_simp.values,
    textposition="outside",
    marker=dict(
        color = "#0B4C7A",
        line=dict(color="black", width=1)
    ),
    name="Quantidade"
))

# Linha da média
fig.add_hline(
    y=media,
    line_dash="dash",
    line_color="blue",
    annotation_text=f"Média ({media:.0f})",
    annotation_position="top left",
    annotation_font_size=16
)

# Linha da mediana
fig.add_hline(
    y=mediana,
    line_dash="dot",
    line_color="red",
    annotation_text=f"Mediana ({mediana:.0f})",
    annotation_position="top left",
    annotation_font_size=16
)

# Layout
fig.update_layout(
    xaxis_title="",
    yaxis_title="",
    template="plotly_white",
    bargap=0.3,  # espaçamento entre barras
    yaxis=dict(
        range=[0, max(contagem_meses_simp.values) * 1.2]  # 20% acima do maior valor
    )
)

fig

st.markdown(
    "<p style='font-size: 12px;'><b>Nota: </b> Os dados apresentados foram coletados a partir da planilha de controle do licenciamento urbano, desenvolvida pela equipe da Gerência de Controle de processos.</p>",
    unsafe_allow_html=True
)

st.divider()

# ---------------------------------------- 4.3. Quantidade de processo tramitação geral por analista ----------------------------------------

# Contagem por tipo de processo
st.markdown(
    "<h3 style='text-align: left;'>4.2. Quantidade de protocolos de tramitação simplificada por analista </h3>",
    unsafe_allow_html=True
)

# Gráfico de processos ambientais na horizontal por tipo com plotly express

cont_proc_urb_simp_ana = df_ctu_simp['ANALISTA'].value_counts().sort_values()

# Criar gráfico de barras horizontais
fig = go.Figure(go.Bar(
    x=cont_proc_urb_simp_ana.values,
    y=cont_proc_urb_simp_ana.index,
    orientation='h',
    text=cont_proc_urb_simp_ana.values,
    textposition="outside",
    textfont=dict(size=16),
    marker=dict(color = "#0B4C7A", line=dict(color="black", width=1))
))

# Layout
fig.update_layout(
    template="plotly_white",
    height=len(cont_proc_urb_simp_ana) * 50,  # altura automática (30 px por categoria)
    margin=dict(l=250),  # margem esquerda maior p/ textos longos
    yaxis=dict(
        tickfont=dict(size=16)       # <- aumenta a fonte dos tipos de processo
    ),
    xaxis=dict(
        tickfont=dict(size=14)       # opcional: aumenta a fonte dos valores no eixo X
    )
)

fig

st.markdown(
    "<p style='font-size: 12px;'><b>Nota: </b> Os dados apresentados foram coletados a partir da planilha de controle do licenciamento urbano, desenvolvida pela equipe da Gerência de Controle de processos.</p>",
    unsafe_allow_html=True
)

st.divider()

# ---------------------- 4.4. Gráfico de velocímetro e variação mensal ----------------------

col1, col2 = st.columns([1,2])

with col1:
    st.markdown(
    "<h3 style='text-align: center;'>4.3. Meta-2: Aprovação de licenças simplificadas até 10 dias</h3>",
    unsafe_allow_html=True
)

# Converter para número de dias
    df_num_dias_simp = (df_ctu_simp['DATA DE APROVAÇÃO'] - df_ctu_simp['DATA DE ENTRADA']).dt.days.abs()

# Calcular média e mediana em dias
    media_dias_simp = df_num_dias_simp.mean()
    median_dias_simp = df_num_dias_simp.median()

    valor_gauge = round(media_dias_simp,0)

    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=valor_gauge,
        title={'text':""},
        delta={'reference': 10, 'increasing': {'color': "red"}, 'decreasing': {'color': "green"}},
        gauge={
            'axis': {'range': [0, 30]}, 
            'bar': {'color': "darkgreen"},
            'steps': [
                {'range': [0, 10], 'color': 'lightgreen'},
                {'range': [10, 30], 'color': 'lightcoral'}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 10
            }
        }
    ))

    # Adicionar mediana como anotação
    fig.add_annotation(
        x=0.5,
        y=0.20,
        text=f"Mediana: {median_dias_simp:.0f} dias",
        showarrow=False,
        font=dict(size=16, color="blue")
    )

    fig.update_layout(
        width=500,   # largura do gráfico
        height=400   # altura do gráfico
    )

    st.plotly_chart(fig, use_container_width=True)

# Gráfico de linhas da variação da média e da mediana:
with col2:
    st.markdown(
        "<h3 style='text-align: center;'>4.4. Variação Mensal da Média e Mediana de Dias para Aprovação</h3>",
        unsafe_allow_html=True
    )
    
    # Calcular diferença de dias
    df_num_dias_simp = (df_ctu_simp['DATA DE APROVAÇÃO'] - df_ctu_simp['DATA DE ENTRADA']).dt.days
    df_ctu_simp['dias'] = df_num_dias_simp

    # Extrair mês
    df_ctu_simp['mes'] = df_ctu_simp['DATA DE ENTRADA'].dt.month

    # Calcular média e mediana por mês
    df_variacao_mensal_simp = df_ctu_simp.groupby('mes')['dias'].agg(['mean', 'median']).reset_index()

    fig = go.Figure()

    # Linha da média
    fig.add_trace(go.Scatter(
        x=df_variacao_mensal_simp['mes'],
        y=df_variacao_mensal_simp['mean'],
        mode='lines+markers',
        name='Média',
        line=dict(color='green', width=2),
        marker=dict(size=8)
    ))

    # Linha da mediana
    fig.add_trace(go.Scatter(
        x=df_variacao_mensal_simp['mes'],
        y=df_variacao_mensal_simp['median'],
        mode='lines+markers',
        name='Mediana',
        line=dict(color='blue', width=2, dash='dot'),
        marker=dict(size=8)
    ))

     # Linha de meta de 10 dias
    fig.add_hline(
        y=10,
        line_dash="dash",             # linha pontilhada
        line_color="red",
        annotation_text="Meta 10 dias",
        annotation_position="top right",
        annotation_font=dict(size=16, color="red")
    )

    # Layout
    fig.update_layout(
        xaxis_title="Mês",
        yaxis_title="Dias",
        template="plotly_white",
        xaxis=dict(tickmode='linear'),
        height=450,
        legend=dict(
        font=dict(size=18)  # <- aumenta o tamanho da legenda
        )
    )

    # Exibir o gráfico **dentro da coluna**
    st.plotly_chart(fig, use_container_width=True)

st.markdown(
    "<p style='font-size: 12px;'><b>Nota: </b> Os dados apresentados foram coletados a partir da planilha de controle do licenciamento urbano, desenvolvida pela equipe da Gerência de Controle de processos.</p>",
    unsafe_allow_html=True
)


st.divider()


# ---------------------- 4.5. Tabela com processos tramitação simplificada ----------------------
st.subheader("4.5. Tabela com os processos de Licenciamento Urbano de tramitação simplificada")

# Selecionar colunas que vão aparecer
col_urb_simp_exibir = ["PROTOCOLO ", "ASSUNTO/TIPOLOGIA","DATA DE ENTRADA", "DATA DE APROVAÇÃO", "STATUS", "ANALISTA"]
df_filt_ctu_simp= df_ctu_simp[col_urb_simp_exibir]

# Remover linhas totalmente em branco
df_filt_ctu_simp = df_filt_ctu_simp.dropna(how="all")

# Formatar as datas no formato dd/mm/aaaa
df_filt_ctu_simp["DATA DE ENTRADA"] = df_filt_ctu_simp["DATA DE ENTRADA"].dt.strftime("%d/%m/%Y")
df_filt_ctu_simp["DATA DE APROVAÇÃO"] = df_filt_ctu_simp["DATA DE APROVAÇÃO"].dt.strftime("%d/%m/%Y")

# Função de estilo
def estilo(df_filtrado):
    return (
        df_filtrado.style
        .set_properties(**{'text-align': 'center'})  # centraliza o conteúdo
        .set_table_styles([                           # estiliza cabeçalho
            {'selector': 'th', 'props': [('font-weight', 'bold'), ('text-align', 'center')]}
        ])
    )

# Exibir
st.dataframe(df_filt_ctu_simp, use_container_width=True, hide_index=True)

st.markdown(
    "<p style='font-size: 12px;'><b>Nota: </b> Os dados apresentados foram coletados a partir da planilha de controle do cadastro imobiliário, desenvolvida pela equipe da Gerência de Controle de processos.</p>",
    unsafe_allow_html=True
)

st.divider()

# ======================================= 5. Resultados parciais de tramitação colegiada  =======================================

st.subheader("5. Resultados de processos de tramitação colegiada - Ano 2025")

col1, col2, col3, col4 = st.columns(4)
col1.metric("Tramitação colegiada", total_linhas_col)
col2.metric("Total de aprovados", qtde_aprov_ctu_col, delta=f"{perc_aprov_col:.2f}%")
col3.metric("Média dias aprovação", abs(media_dias_col).days)
col4.metric("Mediana dias aprovação", abs(median_dias_col).days)

st.divider()

# ---------------------------------------- 5.1. Quantidade de processos de tramitação colegiada ----------------------------------------

st.subheader("5.1. Quantidade de processos urbanos de tramitação colegiada - Ano 2025")

import calendar

# Criar a coluna 'mes'
df_ctu_col["mes"] = df_ctu_col["DATA DE ENTRADA"].dt.month

# Contar a quantidade por mês e ordenar
contagem_meses_col = df_ctu_col["mes"].value_counts().sort_index()

# Calcular média e mediana
media = contagem_meses_col.mean()
mediana = contagem_meses_col.median()

# Corrigir nomes dos meses (índices como int)
meses = [calendar.month_abbr[int(m)] for m in contagem_meses_col.index]

# Criar figura
fig = go.Figure()

# Barras
fig.add_trace(go.Bar(
    x=meses,
    y=contagem_meses_col.values,
    text=contagem_meses_col.values,
    textposition="outside",
    marker=dict(
        color = "#0B4C7A",
        line=dict(color="black", width=1)
    ),
    name="Quantidade"
))

# Linha da média
fig.add_hline(
    y=media,
    line_dash="dash",
    line_color="blue",
    annotation_text=f"Média ({media:.0f})",
    annotation_position="top left",
    annotation_font_size=16
)

# Linha da mediana
fig.add_hline(
    y=mediana,
    line_dash="dot",
    line_color="red",
    annotation_text=f"Mediana ({mediana:.0f})",
    annotation_position="top left",
    annotation_font_size=16
)

# Layout
fig.update_layout(
    xaxis_title="",
    yaxis_title="",
    template="plotly_white",
    bargap=0.3,  # espaçamento entre barras
    yaxis=dict(
        range=[0, max(contagem_meses_col.values) * 1.2]  # 20% acima do maior valor
    )
)

fig

st.markdown(
    "<p style='font-size: 12px;'><b>Nota: </b> Os dados apresentados foram coletados a partir da planilha de controle do licenciamento urbano, desenvolvida pela equipe da Gerência de Controle de processos.</p>",
    unsafe_allow_html=True
)

st.divider()

# ---------------------- 5.2. Gráfico de velocímetro e variação mensal ----------------------

col1, col2 = st.columns([1,2])

with col1:
    st.markdown(
    "<h3 style='text-align: center;'>5.2. Meta-3: Aprovação de licenças colegiadas até 60 dias</h3>",
    unsafe_allow_html=True
)

# Converter para número de dias
    df_num_dias_col = (df_ctu_col['DATA DE APROVAÇÃO'] - df_ctu_col['DATA DE ENTRADA']).dt.days.abs()

# Calcular média e mediana em dias
    media_dias_col = df_num_dias_col.mean()
    median_dias_col = df_num_dias_col.median()

    valor_gauge = round(media_dias_col,0)

    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=valor_gauge,
        title={'text':""},
        delta={'reference': 60, 'increasing': {'color': "red"}, 'decreasing': {'color': "green"}},
        gauge={
            'axis': {'range': [0, 90]}, 
            'bar': {'color': "darkgreen"},
            'steps': [
                {'range': [0, 60], 'color': 'lightgreen'},
                {'range': [60, 90], 'color': 'lightcoral'}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 60
            }
        }
    ))

    # Adicionar mediana como anotação
    fig.add_annotation(
        x=0.5,
        y=0.20,
        text=f"Mediana: {median_dias_col:.0f} dias",
        showarrow=False,
        font=dict(size=16, color="blue")
    )

    fig.update_layout(
        width=500,   # largura do gráfico
        height=400   # altura do gráfico
    )

    st.plotly_chart(fig, use_container_width=True)

# Gráfico de linhas da variação da média e da mediana:
with col2:
    st.markdown(
        "<h3 style='text-align: center;'>5.3. Variação Mensal da Média e Mediana de Dias para Aprovação</h3>",
        unsafe_allow_html=True
    )
    
    # Calcular diferença de dias
    df_num_dias_col = (df_ctu_col['DATA DE APROVAÇÃO'] - df_ctu_col['DATA DE ENTRADA']).dt.days
    df_ctu_col['dias'] = df_num_dias_col

    # Extrair mês
    df_ctu_col['mes'] = df_ctu_col['DATA DE ENTRADA'].dt.month

    # Calcular média e mediana por mês
    df_variacao_mensal_col = df_ctu_col.groupby('mes')['dias'].agg(['mean', 'median']).reset_index()

    fig = go.Figure()

    # Linha da média
    fig.add_trace(go.Scatter(
        x=df_variacao_mensal_col['mes'],
        y=df_variacao_mensal_col['mean'],
        mode='lines+markers',
        name='Média',
        line=dict(color='green', width=2),
        marker=dict(size=8)
    ))

    # Linha da mediana
    fig.add_trace(go.Scatter(
        x=df_variacao_mensal_col['mes'],
        y=df_variacao_mensal_col['median'],
        mode='lines+markers',
        name='Mediana',
        line=dict(color='blue', width=2, dash='dot'),
        marker=dict(size=8)
    ))

     # Linha de meta de 30 dias
    fig.add_hline(
        y=60,
        line_dash="dash",             # linha pontilhada
        line_color="red",
        annotation_text="Meta 60 dias",
        annotation_position="top right",
        annotation_font=dict(size=16, color="red")
    )

    # Layout
    fig.update_layout(
        xaxis_title="Mês",
        yaxis_title="Dias",
        template="plotly_white",
        xaxis=dict(tickmode='linear'),
        height=450,
        legend=dict(
        font=dict(size=18)  # <- aumenta o tamanho da legenda
        )
    )

    # Exibir o gráfico **dentro da coluna**
    st.plotly_chart(fig, use_container_width=True)

st.markdown(
    "<p style='font-size: 12px;'><b>Nota: </b> Os dados apresentados foram coletados a partir da planilha de controle do licenciamento urbano, desenvolvida pela equipe da Gerência de Controle de processos.</p>",
    unsafe_allow_html=True
)


st.divider()

# ---------------------- 5.4. Tabela com processos tramitação geral ----------------------
st.subheader("5.4. Tabela com os processos de Licenciamento Urbano de tramitação colegiada")

# Selecionar colunas que vão aparecer
col_urb_col_exibir = ["PROTOCOLO ", "ASSUNTO/TIPOLOGIA","DATA DE ENTRADA", "DATA DE APROVAÇÃO", "STATUS", "ANALISTA"]
df_filt_ctu_col= df_ctu_col[col_urb_col_exibir]

# Remover linhas totalmente em branco
df_filt_ctu_col = df_filt_ctu_col.dropna(how="all")

# Formatar as datas no formato dd/mm/aaaa
df_filt_ctu_col["DATA DE ENTRADA"] = df_filt_ctu_col["DATA DE ENTRADA"].dt.strftime("%d/%m/%Y")
df_filt_ctu_col["DATA DE APROVAÇÃO"] = df_filt_ctu_col["DATA DE APROVAÇÃO"].dt.strftime("%d/%m/%Y")

# Função de estilo
def estilo(df_filtrado):
    return (
        df_filtrado.style
        .set_properties(**{'text-align': 'center'})  # centraliza o conteúdo
        .set_table_styles([                           # estiliza cabeçalho
            {'selector': 'th', 'props': [('font-weight', 'bold'), ('text-align', 'center')]}
        ])
    )

# Exibir
st.dataframe(df_filt_ctu_col, use_container_width=True, hide_index=True)

st.markdown(
    "<p style='font-size: 12px;'><b>Nota: </b> Os dados apresentados foram coletados a partir da planilha de controle do cadastro imobiliário, desenvolvida pela equipe da Gerência de Controle de processos.</p>",
    unsafe_allow_html=True
)

st.divider()