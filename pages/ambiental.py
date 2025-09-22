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
    NÚMEROS DO LICENCIAMENTO AMBIENTAL
    </h2>
    """,
    unsafe_allow_html=True
)
st.divider()

# 1 ============================== Lendo a base de dados excel do Licenciamento Ambiental ===================================

df_cta = pd.read_excel(
    r"assets/NOVO PROCESSOS EM ANDAMENTO 2025  - CTA.xlsx",
    sheet_name=['CTA 2025', 'ANALISTAS']
)

df_cta_2025 = df_cta['CTA 2025']
df_cta_ana = df_cta['ANALISTAS']


df_lic_amb_2025 = pd.read_excel(
    r"assets/LICENÇAS EMITIDAS AMBIENTAIS.xlsx",
    sheet_name="Saída",
    header=1
)


#  Normalizar os nomes das colunas (remove espaços e padroniza maiúsculas)
df_lic_amb_2025.columns = df_lic_amb_2025.columns.str.strip().str.upper()


# 1.1 ============================== Formatando os dados de datas ===================================

# Converter a coluna DATA para formato dd/mm/aa e as demais para formatos númericos:
df_cta_2025['DATA DE ENTRADA'] = pd.to_datetime(df_cta_2025['DATA DE ENTRADA'], format='%d/%m/%Y')
df_cta_2025['DATA DE APROVAÇÃO'] = pd.to_datetime(df_cta_2025['DATA DE APROVAÇÃO'], format='%d/%m/%Y')

for col in ['DATA A', 'DATA B']:
    if col in df_lic_amb_2025.columns:
        df_lic_amb_2025[col] = pd.to_datetime(df_lic_amb_2025[col], errors='coerce', dayfirst=True)



# 1.2. ============================== Cálculos do total, aprovados, média e mediana ===================================

# Número total de processo ambientais
total_linhas_amb = len(df_cta_2025)

# Quantidade de processos aprovados e percentual
df_cta_2025_aprovados = df_cta_2025[df_cta_2025['STATUS'] == 'APROVADO']
qtde_aprov_amb = df_cta_2025_aprovados.shape[0]
perc_aprov_amb = qtde_aprov_amb / total_linhas_amb * 100

# Cálculo da média e da mediana de dias para aprovação projetos ambientais
df_num_dias_amb = df_cta_2025['DATA DE APROVAÇÃO'] - df_cta_2025['DATA DE ENTRADA']
df_num_dias_amb.dropna(inplace=True)
media_dias_amb = df_num_dias_amb.mean()
median_dias_amb = df_num_dias_amb.median()

# Quantidade geral de licenças emitidas:
qtde_lic_amb_2025 = df_lic_amb_2025.shape[0]

# 2. ============================== Gráficos e visuais do L.A. ===================================

# ---------------------- 2.1. Cartões com dados ----------------------

st.subheader("1. Números gerais do Licenciamento Ambiental - Ano 2025")

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total de Protocolos", total_linhas_amb)
col2.metric("Total de Aprovados", qtde_aprov_amb, delta=f"{perc_aprov_amb:.2f}%")
col3.metric("Média de dias/ aprovação", media_dias_amb.days)
col4.metric("Mediana de dias/ aprovação", median_dias_amb.days)

st.divider()

# ---------------------- 2.2. Gráfico da quantidade por tipo de processos ----------------------

# Contagem por tipo de processo
st.markdown(
    "<h3 style='text-align: left;'>2. Quantidade de protocolos por tipo de processo</h3>",
    unsafe_allow_html=True
)

# Gráfico de processos ambientais na horizontal por tipo com plotly express

cont_proc_amb = df_cta_2025['ASSUNTO/TIPOLOGIA'].value_counts().sort_values()

# Criar gráfico de barras horizontais
fig = go.Figure(go.Bar(
    x=cont_proc_amb.values,
    y=cont_proc_amb.index,
    orientation='h',
    text=cont_proc_amb.values,
    textposition="outside",
    textfont=dict(size=16),
    marker=dict(color="darkgreen", line=dict(color="black", width=1))
))

# Layout
fig.update_layout(
    template="plotly_white",
    height=len(cont_proc_amb) * 50,  # altura automática (30 px por categoria)
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
    "<p style='font-size: 12px;'><b>Nota: </b> Os dados apresentados foram coletados a partir da planilha de controle do licenciamento ambiental, desenvolvida pela equipe da Gerência de Controle de processos.</p>",
    unsafe_allow_html=True
)

st.divider()


# ======================== 3. Gráfico da quantidade por tipo de processos ========================

# ---------------------- 3.1. Gráfico da distribuição de protocolos por mês no ano 2025 ----------------------

st.markdown(
    "<h3 style='text-align: left;'>3. Distribuição dos Protocolos de Licencimento Ambiental por Mês - 2025</h3>",
    unsafe_allow_html=True
)

# Garantir que a coluna seja datetime
df_cta_2025["DATA DE ENTRADA"] = pd.to_datetime(
    df_cta_2025["DATA DE ENTRADA"],
    errors="coerce",
    dayfirst=True
)

# Criar a coluna 'mes'
df_cta_2025["mes"] = df_cta_2025["DATA DE ENTRADA"].dt.month

# Contar a quantidade por mês e ordenar
cont_meses_cta_2025 = df_cta_2025["mes"].value_counts().sort_index()

# Calcular média e mediana (quantidade de protocolos por mês)
media_dias_amb = cont_meses_cta_2025.mean()
median_dias_amb = cont_meses_cta_2025.median()

# Criar gráfico
fig = go.Figure()

# Barras
fig.add_trace(go.Bar(
    x=cont_meses_cta_2025.index,       # Corrigido: pega os meses
    y=cont_meses_cta_2025.values,
    text=cont_meses_cta_2025.values,
    textposition="outside",
    textfont=dict(size=18),
    marker=dict(color="darkgreen", line=dict(color="black", width=1)),
    name="Protocolos"
))

# Linha da média
fig.add_hline(
    y=media_dias_amb,
    line_dash="dash",
    line_color="grey",
    annotation_text=f"Média ({media_dias_amb:.0f})",
    annotation_position="top right",
    annotation_font=dict(size=16, color="grey")
)

# Linha da mediana
fig.add_hline(
    y=median_dias_amb,
    line_dash="dot",
    line_color="orange",
    annotation_text=f"Mediana ({median_dias_amb:.0f})",
    annotation_position="bottom right",
    annotation_font=dict(size=16, color="grey")
)

# Layout
fig.update_layout(
    template="plotly_white",
    bargap=0.3,
    xaxis=dict(
        tickmode="array",
        tickvals=list(range(1, 13)),
        ticktext=["Jan", "Fev", "Mar", "Abr", "Mai", "Jun",
                  "Jul", "Ago", "Set", "Out", "Nov", "Dez"],
        tickfont=dict(size=16)   # tamanho dos ticks do eixo X
    ),
    yaxis=dict(
        range=[0, 160],           # define o intervalo do eixo Y de 0 a 150
        tickfont=dict(size=16)    # tamanho dos ticks do eixo Y
    )
)

st.plotly_chart(fig, use_container_width=True)

st.markdown(
    "<p style='font-size: 12px;'><b>Nota: </b> Os dados apresentados foram coletados a partir da planilha de controle do licenciamento ambiental, desenvolvida pela equipe da Gerência de Controle de processos.</p>",
    unsafe_allow_html=True
)

st.divider()


#  ---------------------- 3.2. Quantidade de processos por analista ----------------------

# Contagem por tipo de processo
st.markdown(
    "<h3 style='text-align: left;'>4. Quantidade de protocolos por analista </h3>",
    unsafe_allow_html=True
)

# Gráfico de processos ambientais na horizontal por tipo com plotly express

cont_proc_amb_ana = df_cta_2025['ANALISTA'].value_counts().sort_values()

# Criar gráfico de barras horizontais
fig = go.Figure(go.Bar(
    x=cont_proc_amb_ana.values,
    y=cont_proc_amb_ana.index,
    orientation='h',
    text=cont_proc_amb_ana.values,
    textposition="outside",
    textfont=dict(size=16),
    marker=dict(color="darkgreen", line=dict(color="black", width=1))
))

# Layout
fig.update_layout(
    template="plotly_white",
    height=len(cont_proc_amb_ana) * 50,  # altura automática (30 px por categoria)
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
    "<p style='font-size: 12px;'><b>Nota: </b> Os dados apresentados foram coletados a partir da planilha de controle do licenciamento ambiental, desenvolvida pela equipe da Gerência de Controle de processos.</p>",
    unsafe_allow_html=True
)

st.divider()
#  ---------------------- 3.3. Cartões com valores gerais das licenças emitidas ----------------------

st.markdown(
    "<h3 style='text-align: left;'>5. Resultados parciais da emissão de licenças ambientais</h3>",
    unsafe_allow_html=True
)

# Função para categorizar cada licença
def categorizar_licenca(x):
    x = str(x).upper().strip()
    if "DISPENSA" in x:
        return "Dispensa"
    elif "REGULARIZAÇÃO" in x:
        return "Regularizações"
    elif x.startswith("R"):
        return "Renovações"
    elif any(l in x for l in ["LO", "LI", "LP", "LS", "PLI", "PLP"]):
        return "Licenças"
    else:
        return "Outras"

# Aplicar categorização na coluna do DataFrame
df_lic_amb_2025['Categoria'] = df_lic_amb_2025['LICENÇA'].apply(categorizar_licenca)

# Contar quantidade por categoria
contagem = df_lic_amb_2025['Categoria'].value_counts().reset_index()
contagem.columns = ['Categoria', 'Quantidade']

def get_quantidade(cat):
    return int(contagem.loc[contagem['Categoria'] == cat, 'Quantidade'].sum() or 0)

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric(label="Dispensa", value=get_quantidade("Dispensa"))
with col2:
    st.metric(label="Licenças", value=get_quantidade("Licenças"))
with col3:
    st.metric(label="Regularizações", value=get_quantidade("Regularizações"))
with col4:
    st.metric(label="Renovações", value=get_quantidade("Renovações"))
with col5:
    st.metric(label="Outras", value=get_quantidade("Outras"))

st.divider()


# ---------------------- 3.4. Gráfico da quantidade de LICENÇAS por tipo ----------------------

col1, col2 = st.columns([1,1])

with col1:
    # Contagem por tipo de processo
    st.markdown(
        "<h3 style='text-align: center;'>6. Quantidade de licenças por tipo de processo</h3>",
        unsafe_allow_html=True
    )

    cont_lic_amb = df_lic_amb_2025['LICENÇA'].value_counts().sort_values()

    # Criar gráfico de barras horizontais
    fig = go.Figure(go.Bar(
        x=cont_lic_amb.values,
        y=cont_lic_amb.index,
        orientation='h',
        text=cont_lic_amb.values,
        textposition="outside",
        textfont=dict(size=20),
        marker=dict(color="darkgreen", line=dict(color="black", width=1))
    ))

    # Layout
    fig.update_layout(
        template="plotly_white",
        height=len(cont_lic_amb) * 50,  # altura automática (30 px por categoria)
        margin=dict(l=250),  # margem esquerda maior p/ textos longos
        yaxis=dict(
            tickfont=dict(size=18)       # <- aumenta a fonte dos tipos de processo
        ),
        xaxis=dict(
            tickfont=dict(size=14)       # opcional: aumenta a fonte dos valores no eixo X
        )
    )

    fig

# ---------------------- 3.5. Gráfico da quantidade de LICENÇAS por natureza da atividade ----------------------

with col2:
    # Contagem por tipo de processo
    st.markdown(
        "<h3 style='text-align: center;'>7. Quantidade de licenças por natureza de atividade</h3>",
        unsafe_allow_html=True
    )

    cont_nat_amb = df_lic_amb_2025['NATUREZA'].value_counts().sort_values()

    fig = go.Figure(go.Bar(
        x=cont_nat_amb.values,
        y=cont_nat_amb.index,
        orientation='h',
        text=cont_nat_amb.values,          # <- mostrar os próprios valores da contagem
        textposition="outside",
        textfont=dict(size=16),
        marker=dict(color="darkgreen", line=dict(color="black", width=1))
    ))

    # Layout com eixo x padronizado
    fig.update_layout(
        template="plotly_white",
        height=len(cont_nat_amb) * 50,       # altura dinâmica
        margin=dict(l=250),
        yaxis=dict(
            tickfont=dict(size=18)
        ),
        xaxis=dict(
            tickfont=dict(size=14),
            range=[0, max(cont_nat_amb.values) * 1.1],  # escala do eixo x proporcional
            dtick=20  # intervalo entre os ticks
        )
    )

    fig

st.markdown(
    "<p style='font-size: 12px;'><b>Nota: </b> Os dados apresentados foram coletados a partir da planilha de controle do licenciamento ambiental, desenvolvida pela equipe da Gerência de Controle de processos.</p>",
    unsafe_allow_html=True
)

st.divider()

# ---------------------- 3.6. Gráfico de velocímetro e variação mensal ----------------------

col1, col2 = st.columns([1,2])

with col1:
    st.markdown(
    "<h3 style='text-align: center;'>8. Meta-1: Aprovação de licenças no máximo até 30 dias</h3>",
    unsafe_allow_html=True
)

# Converter para número de dias
    df_num_dias_amb = df_num_dias_amb.dt.days  # importante!

# Calcular média e mediana em dias
    media_dias_amb = df_num_dias_amb.mean()
    median_dias_amb = df_num_dias_amb.median()

    valor_gauge = round(media_dias_amb,0)

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
        text=f"Mediana: {median_dias_amb:.0f} dias",
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
        "<h3 style='text-align: center;'>9. Variação Mensal da Média e Mediana de Dias para Aprovação</h3>",
        unsafe_allow_html=True
    )
    
    # Calcular diferença de dias
    df_num_dias_amb = (df_cta_2025['DATA DE APROVAÇÃO'] - df_cta_2025['DATA DE ENTRADA']).dt.days
    df_cta_2025['dias'] = df_num_dias_amb

    # Extrair mês
    df_cta_2025['mes'] = df_cta_2025['DATA DE ENTRADA'].dt.month

    # Calcular média e mediana por mês
    df_variacao_mensal = df_cta_2025.groupby('mes')['dias'].agg(['mean', 'median']).reset_index()

    fig = go.Figure()

    # Linha da média
    fig.add_trace(go.Scatter(
        x=df_variacao_mensal['mes'],
        y=df_variacao_mensal['mean'],
        mode='lines+markers',
        name='Média',
        line=dict(color='green', width=2),
        marker=dict(size=8)
    ))

    # Linha da mediana
    fig.add_trace(go.Scatter(
        x=df_variacao_mensal['mes'],
        y=df_variacao_mensal['median'],
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
        annotation_font=dict(size=14, color="red")
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
    "<p style='font-size: 12px;'><b>Nota: </b> Os dados apresentados foram coletados a partir da planilha de controle do licenciamento ambiental, desenvolvida pela equipe da Gerência de Controle de processos.</p>",
    unsafe_allow_html=True
)

# ---------------------- 3.7. Tabela dos processos de licenciamento ambiental ----------------------

st.subheader("10. Tabela de processos de Licenciamento Ambiental")

# Colunas desejadas
col_amb_exibir = ["PROTOCOLO ", "ASSUNTO/TIPOLOGIA", "DATA DE ENTRADA", "DATA DE APROVAÇÃO", "STATUS", "ANALISTA"]

# Selecionar apenas colunas que existem no DataFrame
colunas_existentes = [c for c in col_amb_exibir if c in df_cta_2025.columns]
df_filt_amb = df_cta_2025[colunas_existentes]

# Remover linhas totalmente em branco
df_filt_amb = df_filt_amb.dropna(how="all")

# Formatar datas no padrão dd/mm/aaaa, somente se existirem
if "DATA DE ENTRADA" in df_filt_amb.columns:
    df_filt_amb["DATA DE ENTRADA"] = pd.to_datetime(df_filt_amb["DATA DE ENTRADA"], errors="coerce").dt.strftime("%d/%m/%Y")
if "DATA DE APROVAÇÃO" in df_filt_amb.columns:
    df_filt_amb["DATA DE APROVAÇÃO"] = pd.to_datetime(df_filt_amb["DATA DE APROVAÇÃO"], errors="coerce").dt.strftime("%d/%m/%Y")

# Função de estilo
def estilo(df_filtrado):
    return (
        df_filtrado.style
        .set_properties(**{'text-align': 'center'})  # centraliza o conteúdo
        .set_table_styles([                           # estiliza cabeçalho
            {'selector': 'th', 'props': [('font-weight', 'bold'), ('text-align', 'center')]}
        ])
    )

# Exibir tabela
st.dataframe(df_filt_amb, use_container_width=True, hide_index=True)

# Nota explicativa
st.markdown(
    "<p style='font-size: 12px;'><b>Nota: </b> Os dados apresentados foram coletados a partir da planilha de controle do cadastro imobiliário, desenvolvida pela equipe da Gerência de Controle de processos.</p>",
    unsafe_allow_html=True
)