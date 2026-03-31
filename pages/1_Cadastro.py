import streamlit as st
from database import inserir_ocorrencia, listar_ocorrencias
import pandas as pd

st.title("📝 Cadastro de Ocorrências")

with st.form("form_ocorrencia"):
    data = st.date_input("Data da ocorrência")
    setor = st.selectbox("Setor", ["Operações", "TI", "Financeiro", "Logística"])
    responsavel = st.text_input("Responsável")
    tipo = st.selectbox("Tipo de erro", ["Erro sistema", "Atraso", "Falha processo"])
    gravidade = st.selectbox("Gravidade", ["Baixa", "Média", "Alta"])
    status = st.selectbox("Status", ["Aberto", "Resolvido"])
    tempo = st.number_input("Tempo de resolução (h)", min_value=0)
    descricao = st.text_area("Descrição")

    botao = st.form_submit_button("Salvar")

    if botao:
        inserir_ocorrencia(
            str(data), setor, responsavel, tipo,
            gravidade, status, int(tempo), descricao
        )
        st.success("Ocorrência salva!")

st.divider()

st.subheader("📋 Ocorrências cadastradas")

dados = listar_ocorrencias()

if dados:
    df = pd.DataFrame(dados, columns=[
        "ID", "Data", "Setor", "Responsável",
        "Tipo", "Gravidade", "Status",
        "Tempo", "Descrição"
    ])
    st.dataframe(df)
else:
    st.info("Nenhuma ocorrência ainda")