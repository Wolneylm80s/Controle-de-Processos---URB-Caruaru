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
    NÚMEROS DA URB CARUARU ANO 2025
    </h2>
    """,
    unsafe_allow_html=True
)

st.divider()

# ============================== Descritivo da pagina ===================================

st.write("👈 Use o **menu lateral** para navegar entre as páginas.")

st.subheader("Apresentação")

st.write("O presente Dashboard traz os números referentes a quantidade de processos e " \
        "protocolos solicitados à Autarquia de Meio Ambiente de Caruaru.")

st.write("Neste conjunto de dados temos informações de setores como:")
st.write("""
- Números do Atendimento Presencial
- Cadastro Imobiliário
- Licenciamento Ambiental
- Licenciamento Urbano
""")




