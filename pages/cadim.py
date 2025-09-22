# =============================== Importação das bibliotecas =================================
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
import calendar

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
    NÚMEROS DO CADASTRO IMOBILIÁRIO
    </h2>
    """,
    unsafe_allow_html=True
)
st.divider()


# 1 ============================== Lendo a base de dados excel do cadastro e memorando ===================================

df_cadastro = pd.read_excel(
    r"assets\NOVA_ PROCESSOS EM ANDAMENTO 2025  - CADASTRO.xlsx",
    sheet_name=['PROTOCOLO 2025', 'QUANTITATIVO', 'ANALISTAS', 'MEMORANDO 2025']
)

df_prot_ctc = df_cadastro['PROTOCOLO 2025']
df_memo_ctc = df_cadastro['MEMORANDO 2025']


# Função para converter datas em string (dd/mm/yyyy) ou número serial Excel
def converter_data(valor):
    try:
        # Se for número (serial Excel)
        if str(valor).isdigit():
            return pd.to_datetime("1899-12-30") + pd.to_timedelta(int(valor), unit="D")
        # Se for string no formato dia/mês/ano
        else:
            return pd.to_datetime(valor, dayfirst=True, errors="coerce")
    except:
        return pd.NaT  # caso não consiga converter

# ============================== Formatando os dados de datas ===================================

# Conversão dos registros dos datasets - Protocolos do C.I.
df_prot_ctc['DATA DE ENTRADA']   = df_prot_ctc['DATA DE ENTRADA'].apply(converter_data)
df_prot_ctc['DATA DE APROVAÇÃO'] = df_prot_ctc['DATA DE APROVAÇÃO'].apply(converter_data)

# Conversão dos registros dos datasets - Memorandos do C.I.
df_memo_ctc['DATA DE ENTRADA']   = df_memo_ctc['DATA DE ENTRADA'].apply(converter_data)
df_memo_ctc['DATA DE APROVAÇÃO'] = df_memo_ctc['DATA DE APROVAÇÃO'].apply(converter_data)

# 1.2. ============================== Cálculos do total, aprovados, média e mediana ===================================

# ---------------------- 1.2.1 Números dos protocolos ----------------------
# número total de protocolos do cadastro imobiliário
total_prot_ctc = len(df_prot_ctc)

# Cálculo do número de dias para aprovação - Protocolos
df_num_dias_prot_ctc = df_prot_ctc['DATA DE APROVAÇÃO'] - df_prot_ctc['DATA DE ENTRADA']
df_num_dias_prot_ctc.dropna(inplace=True)

# número total de protocolos aprovados e o percentual
df_prot_ctc_aprovados = df_prot_ctc[df_prot_ctc['STATUS'] == 'APROVADO']
qtde_aprov_prot_ctc = df_prot_ctc_aprovados.shape[0]
percentual_aprovados_prot_ctc = qtde_aprov_prot_ctc / total_prot_ctc * 100

# Cálculo média e mediana na aba protocolos
media_dias_prot_cad =df_num_dias_prot_ctc.mean()
mediana_dias_prot_cad = df_num_dias_prot_ctc.median()

# ---------------------- 1.2.2 Números dos memorandos ----------------------
# número total de memorandos do cadastro imobiliário
total_memo_ctc = len(df_memo_ctc)

# Cálculo do número de dias para aprovação - Memorandos
df_num_dias_memo_ctc = df_memo_ctc['DATA DE APROVAÇÃO'] - df_memo_ctc['DATA DE ENTRADA']
df_num_dias_memo_ctc.dropna(inplace=True)

# numero total de memorandos aprovados e o percentual
df_memo_ctc_aprovados = df_memo_ctc[df_memo_ctc['STATUS'] == 'APROVADO']
qtde_aprov_memo_ctc = df_memo_ctc_aprovados.shape[0]
percentual_aprovados_memo_ctc = qtde_aprov_memo_ctc / total_memo_ctc * 100

# Cálculo média e mediana na aba memorandos
media_dias_memo_cad =df_num_dias_memo_ctc.mean()
mediana_dias_memo_cad = df_num_dias_memo_ctc.median()


# 2. ============================== Gráficos e visuais dos Protocolos ===================================

# ---------------------- 2.1. Cartões com dados ----------------------

st.subheader("1. Números gerais de protocolos do Cadastro Imobiliário - Ano 2025")

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total de Protocolos", total_prot_ctc)
col2.metric("Total de Aprovados", qtde_aprov_prot_ctc, delta=f"{percentual_aprovados_prot_ctc:.2f}%")
col3.metric("Média de dias/ aprovação", media_dias_prot_cad.days)
col4.metric("Mediana de dias/ aprovação", mediana_dias_prot_cad.days)

st.divider()

# ---------------------- 2.2. Gráfico da quantidade por tipo de processos ----------------------

# Contagem por tipo de processo
st.markdown(
    "<h3 style='text-align: left;'>2. Quantidade de protocolos por tipo de processo</h3>",
    unsafe_allow_html=True
)

contagem_tipos = df_prot_ctc['ASSUNTO/TIPOLOGIA'].value_counts().sort_values()

# Criar gráfico de barras horizontais
fig = go.Figure(go.Bar(
    x=contagem_tipos.values,
    y=contagem_tipos.index,
    orientation='h',
    text=contagem_tipos.values,
    textposition="outside",
    textfont=dict(size=18),
    marker=dict(color="brown", line=dict(color="black", width=1))
))

# Layout
fig.update_layout(
    template="plotly_white",
    height=len(contagem_tipos) * 40,  # altura automática (30 px por categoria)
    margin=dict(l=250),  # margem esquerda maior p/ textos longos
    xaxis=dict(
        tickfont=dict(size=16)
    ),
    yaxis=dict(
        tickfont=dict(size=16)
    )

)

fig

st.markdown(
    "<p style='font-size: 12px;'><b>Nota: </b> Os dados apresentados foram coletados a partir da planilha de controle do cadastro imobiliário, desenvolvida pela equipe da Gerência de Controle de processos.</p>",
    unsafe_allow_html=True
)

st.divider()

# ---------------------- 2.2. Gráfico da quantidade por tipo de processos ----------------------

# Gráfico da distribuição de protocolos por mês no ano 2025

st.markdown(
    "<h3 style='text-align: left;'>3. Distribuição de Protocolos do Cadastro Imobiliário por Mês - 2025</h3>",
    unsafe_allow_html=True
)

# Garantir que a coluna seja datetime
df_prot_ctc["DATA DE ENTRADA"] = pd.to_datetime(
    df_prot_ctc["DATA DE ENTRADA"],
    errors="coerce",
    dayfirst=True
)

# Criar a coluna 'mes'
df_prot_ctc["mes"] = df_prot_ctc["DATA DE ENTRADA"].dt.month


# Contar a quantidade por mês e ordenar
contagem_meses_ctc = df_prot_ctc["mes"].value_counts().sort_index()

# Calcular média e mediana
media_prot_ctc = contagem_meses_ctc.mean()
mediana_prot_ctc = contagem_meses_ctc.median()

# Converter meses para abreviação (Jan, Feb, ...)
meses = [calendar.month_abbr[int(m)] for m in contagem_meses_ctc.index]

# Criar gráfico
fig = go.Figure()

# Barras
fig.add_trace(go.Bar(
    x=meses,
    y=contagem_meses_ctc.values,
    text=contagem_meses_ctc.values,
    textposition="outside",
    textfont=dict(size=18),
    marker=dict(color="brown", line=dict(color="black", width=1)),
    name="Protocolos"
))

# Linha da média
fig.add_hline(
    y=media_prot_ctc,
    line_dash="dash",
    line_color="grey",
    annotation_text=f"Média ({media_prot_ctc:.0f})",
    annotation_position="bottom left",
    annotation_font_size=16  # <- aumenta o tamanho do texto
)

# Linha da mediana
fig.add_hline(
    y=mediana_prot_ctc,
    line_dash="dot",
    line_color="orange",
    annotation_text=f"Mediana ({mediana_prot_ctc:.0f})",
    annotation_position="top left",
    annotation_font_size=16  # <- aumenta o tamanho do texto
)

# Layout
fig.update_layout(
    template="plotly_white",
    bargap=0.3,
    xaxis=dict(
        tickfont=dict(size=16)
    ),
    yaxis=dict(
        tickfont=dict(size=16),
        range=[0, contagem_meses_ctc.values.max() * 1.5]  # aumenta o limite em 20%
    )
)

fig

st.markdown(
    "<p style='font-size: 12px;'><b>Nota: </b> Os dados apresentados foram coletados a partir da planilha de controle do cadastro imobiliário, desenvolvida pela equipe da Gerência de Controle de processos.</p>",
    unsafe_allow_html=True
)


# ---------------------- 2.3. Gráfico da quantidade de protocolos por analista ----------------------

# Contagem por tipo de processo
st.markdown(
    "<h3 style='text-align: left;'>4. Quantidade de protocolos por analista</h3>",
    unsafe_allow_html=True
)

# Normalizar para maiúsculas
df_prot_ctc['ANALISTA'] = df_prot_ctc['ANALISTA'].str.strip().str.upper()

contagem_analista = df_prot_ctc['ANALISTA'].value_counts().sort_values()

# Criar gráfico de barras horizontais
fig = go.Figure(go.Bar(
    x=contagem_analista.values,
    y=contagem_analista.index,
    orientation='h',
    text=contagem_analista.values,
    textposition="outside",
    textfont=dict(size=18),
    marker=dict(color="brown", line=dict(color="black", width=1))
))

# Layout
fig.update_layout(
    template="plotly_white",
    height=len(contagem_analista) * 40,  # altura automática (30 px por categoria)
    margin=dict(l=250),  # margem esquerda maior p/ textos longos
    xaxis=dict(
        tickfont=dict(size=16)
    ),
    yaxis=dict(
        tickfont=dict(size=16)
    )

)

fig

st.markdown(
    "<p style='font-size: 12px;'><b>Nota: </b> Os dados apresentados foram coletados a partir da planilha de controle do cadastro imobiliário, desenvolvida pela equipe da Gerência de Controle de processos.</p>",
    unsafe_allow_html=True
)

st.divider()

# ---------------------- 2.4. Tabela protocolos do C.I. ----------------------
st.subheader("5. Tabela com os protocolos do Cadastro Imobiliario")

# Selecionar colunas que vão aparecer
colunas_para_exibir = ["PROTOCOLO", "ASSUNTO/TIPOLOGIA","DATA DE ENTRADA", "DATA DE APROVAÇÃO", "STATUS", "ANALISTA"]
df_filt_prot_ctc = df_prot_ctc[colunas_para_exibir]

# Remover linhas totalmente em branco
df_filt_prot_ctc = df_filt_prot_ctc.dropna(how="all")


# Formatar as datas no formato dd/mm/aaaa
df_filt_prot_ctc["DATA DE ENTRADA"] = df_filt_prot_ctc["DATA DE ENTRADA"].dt.strftime("%d/%m/%Y")
df_filt_prot_ctc["DATA DE APROVAÇÃO"] = df_filt_prot_ctc["DATA DE APROVAÇÃO"].dt.strftime("%d/%m/%Y")

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
st.dataframe(df_filt_prot_ctc, use_container_width=True, hide_index=True)

st.markdown(
    "<p style='font-size: 12px;'><b>Nota: </b> Os dados apresentados foram coletados a partir da planilha de controle do cadastro imobiliário, desenvolvida pela equipe da Gerência de Controle de processos.</p>",
    unsafe_allow_html=True
)

st.divider()

#  ==============================3.  Gráficos e visuais dos Memorandos ===================================

# ---------------------- 3.1. Cartões com dados ----------------------

st.subheader("6. Números gerais de memorandos do Cadastro Imobiliário - Ano 2025")

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total de Memorandos", total_memo_ctc)
col2.metric("Total finalizados", qtde_aprov_memo_ctc, delta=f"{percentual_aprovados_memo_ctc:.2f}%")
col3.metric("Média de dias/ finalização", media_dias_memo_cad.days)
col4.metric("Mediana de dias/ finalização", mediana_dias_memo_cad.days)

st.divider()

# ---------------------- 3.2. Gráfico da quantidade por tipo de processos ----------------------

# Contagem por tipo de processo
st.markdown(
    "<h3 style='text-align: left;'>7. Quantidade de memorandos por tipo de processo</h3>",
    unsafe_allow_html=True
)

contagem_tipos_memo = df_memo_ctc['ASSUNTO/TIPOLOGIA'].value_counts().sort_values()

# Criar gráfico de barras horizontais
fig = go.Figure(go.Bar(
    x=contagem_tipos_memo.values,
    y=contagem_tipos_memo.index,
    orientation='h',
    text=contagem_tipos_memo.values,
    textposition="outside",
    textfont=dict(size=18),
    marker=dict(color="brown", line=dict(color="black", width=1))
))

# Layout
fig.update_layout(
    template="plotly_white",
    height=len(contagem_tipos_memo) * 40,  # altura automática (30 px por categoria)
    margin=dict(l=250),  # margem esquerda maior p/ textos longos
    xaxis=dict(
        tickfont=dict(size=16)
    ),
    yaxis=dict(
        tickfont=dict(size=16)
    )
)

fig

st.markdown(
    "<p style='font-size: 12px;'><b>Nota: </b> Os dados apresentados foram coletados a partir da planilha de controle do cadastro imobiliário, desenvolvida pela equipe da Gerência de Controle de processos.</p>",
    unsafe_allow_html=True
)

st.divider()

# ---------------------- 3.3. Gráfico da quantidade por tipo de processos ----------------------

# Gráfico da distribuição de memorandos por mês no ano 2025

st.markdown(
    "<h3 style='text-align: left;'>8. Distribuição dos Memorandos do Cadastro Imobiliário por Mês - 2025</h3>",
    unsafe_allow_html=True
)

# Garantir que a coluna seja datetime
df_memo_ctc["DATA DE ENTRADA"] = pd.to_datetime(
    df_memo_ctc["DATA DE ENTRADA"],
    errors="coerce",
    dayfirst=True
)

# Criar a coluna 'mes'
df_memo_ctc["mes"] = df_memo_ctc["DATA DE ENTRADA"].dt.month

# Contar a quantidade por mês e ordenar
contagem_meses_ctc_memo = df_memo_ctc["mes"].value_counts().sort_index()

# Calcular média e mediana
media_memo_ctc = contagem_meses_ctc_memo.mean()
mediana_memo_ctc = contagem_meses_ctc_memo.median()

# Converter meses para abreviação (Jan, Feb, ...)
meses = [calendar.month_abbr[int(m)] for m in contagem_meses_ctc_memo.index]

# Criar gráfico
fig = go.Figure()

# Barras
fig.add_trace(go.Bar(
    x=meses,
    y=contagem_meses_ctc_memo.values,
    text=contagem_meses_ctc_memo.values,
    textposition="outside",
    textfont=dict(size=18),
    marker=dict(color="brown", line=dict(color="black", width=1)),
    name="Protocolos"
))

# Linha da média
fig.add_hline(
    y=media_memo_ctc,
    line_dash="dash",
    line_color="grey",
    annotation_text=f"Média ({media_memo_ctc:.0f})",
    annotation_position="top right",
    annotation_font_size=16  # <- aumenta o tamanho do texto
)

# Linha da mediana
fig.add_hline(
    y=mediana_memo_ctc,
    line_dash="dot",
    line_color="orange",
    annotation_text=f"Mediana ({mediana_memo_ctc:.0f})",
    annotation_position="bottom right",
    annotation_font_size=16  # <- aumenta o tamanho do texto
)

# Layout
fig.update_layout(
    template="plotly_white",
    bargap=0.3,
    xaxis=dict(
        tickfont=dict(size=16)
    ),
    yaxis=dict(
        tickfont=dict(size=16),
        range=[0, 60]
    )
)

fig

st.markdown(
    "<p style='font-size: 12px;'><b>Nota: </b> Os dados apresentados foram coletados a partir da planilha de controle do cadastro imobiliário, desenvolvida pela equipe da Gerência de Controle de processos.</p>",
    unsafe_allow_html=True
)

st.divider()

# ---------------------- 3.4. Gráfico da quantidade de memorandos por analista ----------------------

# Contagem por tipo de processo
st.markdown(
    "<h3 style='text-align: left;'>9. Quantidade de memorandos por analista</h3>",
    unsafe_allow_html=True
)

# Normalizar para maiúsculas
df_memo_ctc['ANALISTA'] = df_memo_ctc['ANALISTA'].str.strip().str.upper()

cont_memo_analista = df_memo_ctc['ANALISTA'].value_counts().sort_values()

# Criar gráfico de barras horizontais
fig = go.Figure(go.Bar(
    x=cont_memo_analista.values,
    y=cont_memo_analista.index,
    orientation='h',
    text=cont_memo_analista.values,
    textposition="outside",
    textfont=dict(size=18),
    marker=dict(color="brown", line=dict(color="black", width=1))
))

# Layout
fig.update_layout(
    template="plotly_white",
    height=len(cont_memo_analista) * 40,  # altura automática (30 px por categoria)
    margin=dict(l=250),  # margem esquerda maior p/ textos longos
    xaxis=dict(
        tickfont=dict(size=16)
    ),
    yaxis=dict(
        tickfont=dict(size=16)
    )

)

fig

st.markdown(
    "<p style='font-size: 12px;'><b>Nota: </b> Os dados apresentados foram coletados a partir da planilha de controle do cadastro imobiliário, desenvolvida pela equipe da Gerência de Controle de processos.</p>",
    unsafe_allow_html=True
)

st.divider()

# ---------------------- 3.5. Tabela protocolos do C.I. ----------------------
st.subheader("10. Tabela com os memorandos do Cadastro Imobiliario")

# Selecionar colunas que vão aparecer
col_memo_exibir = ["PROTOCOLO", "ASSUNTO/TIPOLOGIA","DATA DE ENTRADA", "DATA DE APROVAÇÃO", "STATUS", "ANALISTA"]
df_filt_memo_ctc = df_memo_ctc[col_memo_exibir]

# Remover linhas totalmente em branco
df_filt_memo_ctc = df_filt_memo_ctc.dropna(how="all")

# Renomear a coluna PROTOCOLO para MEMORANDO
df_filt_memo_ctc = df_filt_memo_ctc.rename(columns={"PROTOCOLO": "MEMORANDO"})

# Formatar as datas no formato dd/mm/aaaa
df_filt_memo_ctc["DATA DE ENTRADA"] = df_filt_memo_ctc["DATA DE ENTRADA"].dt.strftime("%d/%m/%Y")
df_filt_memo_ctc["DATA DE APROVAÇÃO"] = df_filt_memo_ctc["DATA DE APROVAÇÃO"].dt.strftime("%d/%m/%Y")

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
st.dataframe(df_filt_memo_ctc, use_container_width=True, hide_index=True)

st.markdown(
    "<p style='font-size: 12px;'><b>Nota: </b> Os dados apresentados foram coletados a partir da planilha de controle do cadastro imobiliário, desenvolvida pela equipe da Gerência de Controle de processos.</p>",
    unsafe_allow_html=True
)