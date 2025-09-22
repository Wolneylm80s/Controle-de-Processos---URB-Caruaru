# =============================== Importação das bibliotecas =================================
import streamlit as st

pg = st.navigation([
    st.Page("pages/home.py", title= "Página Inicial"),
    st.Page("pages/atend.py", title= "Atendimento Presencial"),
    st.Page("pages/cadim.py", title= "Cadastro Imobiliário"),
    st.Page("pages/ambiental.py", title= "Licenciamento Ambiental"),
    st.Page("pages/urbano.py", title= "Licenciamento Urbano"),
])

pg.run()