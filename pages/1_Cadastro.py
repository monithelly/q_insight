import streamlit as st
import pandas as pd
from database import inserir_ocorrencia, listar_ocorrencias

st.title("📝 Cadastro de Ocorrências")

if st.button("📥 Carregar dados de exemplo"):
    df_exemplo = pd.read_csv("dados_exemplo.csv")

    for _, row in df_exemplo.iterrows():
        inserir_ocorrencia(
            row["data_ocorrencia"],
            row["setor"],
            row["responsavel"],
            row["tipo_erro"],
            row["gravidade"],
            row["status"],
            int(row["tempo_resolucao"]),
            row["descricao"]
        )

    st.success("Dados de exemplo carregados com sucesso!")

with st.form("form_ocorrencia"):
    data = st.date_input("Data da ocorrência")
    setor = st.selectbox("Setor", ["Operações", "TI", "Financeiro", "Logística", "Atendimento"])
    responsavel = st.text_input("Responsável")
    tipo = st.selectbox("Tipo de erro", ["Erro sistema", "Atraso", "Falha processo", "Erro humano", "Retrabalho"])
    gravidade = st.selectbox("Gravidade", ["Baixa", "Média", "Alta"])
    status = st.selectbox("Status", ["Aberto", "Em andamento", "Resolvido"])
    tempo = st.number_input("Tempo de resolução (h)", min_value=0)
    descricao = st.text_area("Descrição")

    botao = st.form_submit_button("Salvar")

    if botao:
        inserir_ocorrencia(
            str(data),
            setor,
            responsavel,
            tipo,
            gravidade,
            status,
            int(tempo),
            descricao
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
    st.dataframe(df, width="stretch")
else:
    st.info("Nenhuma ocorrência ainda.")