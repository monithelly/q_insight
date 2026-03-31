import streamlit as st
from database import init_db

st.set_page_config(
    page_title="Q-Insight",
    page_icon="📊",
    layout="wide"
)

init_db()

st.title("📊 Q-Insight")
st.subheader("Sistema Inteligente de Qualidade Operacional")

st.markdown("""
### Transformando ocorrências em decisão

O **Q-Insight** é um app desenvolvido para apoiar o controle da qualidade operacional, 
permitindo registrar ocorrências, acompanhar indicadores, calcular score de performance 
e priorizar problemas críticos com foco em tomada de decisão.
""")

st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    st.info("""
    **Objetivo do sistema**  
    Centralizar falhas operacionais e transformar dados em insights acionáveis 
    para liderança, acompanhamento e melhoria contínua.
    """)

with col2:
    st.success("""
    **O que você encontra aqui**  
    Cadastro de ocorrências, dashboard com indicadores, score de qualidade 
    e painel de priorização com ações sugeridas.
    """)

st.markdown("## Módulos do sistema")

col3, col4 = st.columns(2)

with col3:
    with st.container(border=True):
        st.markdown("### 📝 Cadastro")
        st.write("Registro estruturado das ocorrências operacionais, incluindo setor, gravidade, status, tempo e descrição.")

    with st.container(border=True):
        st.markdown("### 🏆 Score")
        st.write("Cálculo do score de qualidade por setor, com visão consolidada de performance e ranking visual.")

with col4:
    with st.container(border=True):
        st.markdown("### 📊 Dashboard")
        st.write("Indicadores gerais, filtros, gráficos e visualização rápida das ocorrências registradas.")

    with st.container(border=True):
        st.markdown("### 🚨 Priorização")
        st.write("Classificação dos problemas mais críticos, com ranking e ação sugerida para apoio à gestão.")

st.markdown("---")

st.markdown("## Como usar")
st.write("""
1. Acesse **Cadastro** para registrar ocorrências.  
2. Vá em **Dashboard** para acompanhar indicadores e gráficos.  
3. Consulte **Score** para avaliar a performance dos setores.  
4. Use **Priorização** para identificar o que deve ser tratado primeiro.
""")

st.markdown("---")

st.caption("Projeto de portfólio desenvolvido em Python com Streamlit, SQLite, Pandas e Plotly.")