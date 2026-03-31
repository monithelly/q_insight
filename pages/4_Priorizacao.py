import streamlit as st
import pandas as pd
from database import listar_ocorrencias

st.set_page_config(page_title="Priorização", page_icon="🚨", layout="wide")

st.title("🚨 Priorização de Problemas")
st.caption("Identificação dos problemas mais críticos para ação imediata.")

dados = listar_ocorrencias()

if not dados:
    st.warning("Cadastre ocorrências para gerar prioridades.")
    st.stop()

df = pd.DataFrame(dados, columns=[
    "ID", "Data", "Setor", "Responsável",
    "Tipo", "Gravidade", "Status",
    "Tempo", "Descrição"
])

pesos = {"Baixa": 1, "Média": 2, "Alta": 3}
df["Peso_Gravidade"] = df["Gravidade"].map(pesos)

prioridade = df.groupby("Tipo").agg(
    frequencia=("ID", "count"),
    gravidade_media=("Peso_Gravidade", "mean"),
    tempo_medio=("Tempo", "mean")
).reset_index()

prioridade["Indice_Prioridade"] = (
    prioridade["frequencia"] * 2 +
    prioridade["gravidade_media"] * 3 +
    prioridade["tempo_medio"] * 0.5
)

prioridade["Indice_Prioridade"] = prioridade["Indice_Prioridade"].round(1)


def classificar(indice):
    if indice >= 12:
        return "Alta prioridade"
    elif indice >= 8:
        return "Média prioridade"
    return "Baixa prioridade"


def sugerir_acao(indice):
    if indice >= 12:
        return "Ação imediata: revisar processo, tratar causa raiz e acompanhar diariamente."
    elif indice >= 8:
        return "Ação recomendada: monitorar, ajustar fluxo e alinhar responsáveis."
    return "Ação preventiva: acompanhar indicador e revisar se houver recorrência."


def cor_prioridade(indice):
    if indice >= 12:
        return "red"
    elif indice >= 8:
        return "orange"
    return "green"


prioridade["Classificação"] = prioridade["Indice_Prioridade"].apply(classificar)
prioridade["Ação Sugerida"] = prioridade["Indice_Prioridade"].apply(sugerir_acao)
prioridade["Cor"] = prioridade["Indice_Prioridade"].apply(cor_prioridade)

prioridade = prioridade.sort_values(by="Indice_Prioridade", ascending=False).reset_index(drop=True)

top1 = prioridade.iloc[0]

st.subheader("Problema mais crítico do momento")

col1, col2 = st.columns([3, 1])

with col1:
    st.metric("Problema prioritário", top1["Tipo"])
    st.write(f"**Índice de prioridade:** {top1['Indice_Prioridade']}")
    st.progress(min(int(top1["Indice_Prioridade"] * 5), 100))

with col2:
    if top1["Classificação"] == "Alta prioridade":
        st.error(top1["Classificação"])
    elif top1["Classificação"] == "Média prioridade":
        st.warning(top1["Classificação"])
    else:
        st.success(top1["Classificação"])

st.info(f"**Ação sugerida:** {top1['Ação Sugerida']}")

st.markdown("---")
st.subheader("Ranking de prioridades")

for posicao, row in prioridade.iterrows():
    with st.container(border=True):
        col_a, col_b = st.columns([4, 1])

        with col_a:
            st.markdown(f"### #{posicao + 1} - {row['Tipo']}")
            st.write(
                f"**Frequência:** {row['frequencia']} | "
                f"**Gravidade média:** {row['gravidade_media']:.1f} | "
                f"**Tempo médio de resolução:** {row['tempo_medio']:.1f} h"
            )
            st.write(f"**Ação sugerida:** {row['Ação Sugerida']}")
            st.progress(min(int(row["Indice_Prioridade"] * 5), 100))

        with col_b:
            st.metric("Prioridade", row["Indice_Prioridade"])

            if row["Classificação"] == "Alta prioridade":
                st.error(row["Classificação"])
            elif row["Classificação"] == "Média prioridade":
                st.warning(row["Classificação"])
            else:
                st.success(row["Classificação"])