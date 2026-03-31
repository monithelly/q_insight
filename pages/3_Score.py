import streamlit as st
import pandas as pd
from database import listar_ocorrencias

st.set_page_config(page_title="Score de Qualidade", page_icon="🏆", layout="wide")

st.title("🏆 Score de Qualidade")
st.caption("Visão consolidada da performance por setor.")

dados = listar_ocorrencias()

if not dados:
    st.warning("Cadastre ocorrências para calcular o score.")
    st.stop()

df = pd.DataFrame(dados, columns=[
    "ID", "Data", "Setor", "Responsável",
    "Tipo", "Gravidade", "Status",
    "Tempo", "Descrição"
])

pesos = {
    "Baixa": 1,
    "Média": 2,
    "Alta": 3
}

df["Peso_Gravidade"] = df["Gravidade"].map(pesos)

score_df = df.groupby("Setor").agg(
    ocorrencias_registradas=("ID", "count"),
    impacto_ocorrencias=("Peso_Gravidade", "sum"),
    tempo_total_resolucao=("Tempo", "sum")
).reset_index()

score_df["Score"] = 100 - (
    score_df["ocorrencias_registradas"] * 2 +
    score_df["impacto_ocorrencias"] * 3 +
    score_df["tempo_total_resolucao"] * 0.5
)

score_df["Score"] = score_df["Score"].apply(lambda x: round(max(x, 0), 1))


def classificar_score(score):
    if score >= 90:
        return "Excelente"
    elif score >= 75:
        return "Bom"
    elif score >= 60:
        return "Atenção"
    return "Crítico"


def cor_score(score):
    if score >= 90:
        return "green"
    elif score >= 75:
        return "orange"
    elif score >= 60:
        return "orange"
    return "red"


score_df["Classificação"] = score_df["Score"].apply(classificar_score)
score_df["Cor"] = score_df["Score"].apply(cor_score)

score_df = score_df.sort_values(by="Score", ascending=False).reset_index(drop=True)

score_geral = round(score_df["Score"].mean(), 1)
classificacao_geral = classificar_score(score_geral)

st.subheader("Score geral da operação")

col_a, col_b = st.columns([3, 1])

with col_a:
    st.metric("Score médio consolidado", score_geral)
    st.progress(int(score_geral / 100 * 100))

with col_b:
    if classificacao_geral == "Excelente":
        st.success(classificacao_geral)
    elif classificacao_geral == "Bom":
        st.warning(classificacao_geral)
    elif classificacao_geral == "Atenção":
        st.warning(classificacao_geral)
    else:
        st.error(classificacao_geral)

st.markdown("---")

media_ocorrencias = round(score_df["ocorrencias_registradas"].mean(), 1)
tempo_medio_resolucao = round(df["Tempo"].mean(), 1)
total_setores = score_df["Setor"].nunique()

col1, col2, col3 = st.columns(3)
col1.metric("Setores avaliados", total_setores)
col2.metric("Média de ocorrências por setor", media_ocorrencias)
col3.metric("Tempo médio de resolução", f"{tempo_medio_resolucao} h")

st.markdown("---")
st.subheader("Ranking de performance por setor")

for posicao, row in score_df.iterrows():
    with st.container(border=True):
        col1, col2 = st.columns([4, 1])

        with col1:
            st.markdown(f"### #{posicao + 1} - {row['Setor']}")
            st.write(
                f"Ocorrências registradas: {row['ocorrencias_registradas']} | "
                f"Impacto das ocorrências: {row['impacto_ocorrencias']} | "
                f"Tempo total de resolução: {row['tempo_total_resolucao']} h"
            )
            st.progress(int(row["Score"]))

        with col2:
            st.metric("Score", row["Score"])

            if row["Classificação"] == "Excelente":
                st.success(row["Classificação"])
            elif row["Classificação"] == "Bom":
                st.warning(row["Classificação"])
            elif row["Classificação"] == "Atenção":
                st.warning(row["Classificação"])
            else:
                st.error(row["Classificação"])