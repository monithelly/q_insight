import streamlit as st
import pandas as pd
import plotly.express as px
from database import listar_ocorrencias

st.set_page_config(page_title="Dashboard", page_icon="📊", layout="wide")

st.title("📊 Dashboard")
st.caption("Visão geral das ocorrências de qualidade operacional.")

dados = listar_ocorrencias()

if not dados:
    st.warning("Cadastre pelo menos uma ocorrência para visualizar o dashboard.")
    st.stop()

df = pd.DataFrame(dados, columns=[
    "ID", "Data", "Setor", "Responsável",
    "Tipo", "Gravidade", "Status",
    "Tempo", "Descrição"
])

df["Data"] = pd.to_datetime(df["Data"])

# ---------------------------
# SIDEBAR - FILTROS
# ---------------------------
st.sidebar.header("Filtros")

setores = ["Todos"] + sorted(df["Setor"].dropna().unique().tolist())
gravidades = ["Todas"] + sorted(df["Gravidade"].dropna().unique().tolist())
status_lista = ["Todos"] + sorted(df["Status"].dropna().unique().tolist())

setor_sel = st.sidebar.selectbox("Setor", setores)
gravidade_sel = st.sidebar.selectbox("Gravidade", gravidades)
status_sel = st.sidebar.selectbox("Status", status_lista)

data_min = df["Data"].min().date()
data_max = df["Data"].max().date()

periodo = st.sidebar.date_input(
    "Período",
    value=(data_min, data_max),
    min_value=data_min,
    max_value=data_max
)

df_filtrado = df.copy()

if setor_sel != "Todos":
    df_filtrado = df_filtrado[df_filtrado["Setor"] == setor_sel]

if gravidade_sel != "Todas":
    df_filtrado = df_filtrado[df_filtrado["Gravidade"] == gravidade_sel]

if status_sel != "Todos":
    df_filtrado = df_filtrado[df_filtrado["Status"] == status_sel]

if isinstance(periodo, tuple) and len(periodo) == 2:
    data_inicio, data_fim = periodo
    df_filtrado = df_filtrado[
        (df_filtrado["Data"].dt.date >= data_inicio) &
        (df_filtrado["Data"].dt.date <= data_fim)
    ]

if df_filtrado.empty:
    st.warning("Nenhum dado encontrado com os filtros selecionados.")
    st.stop()

# ---------------------------
# KPIs
# ---------------------------
st.markdown("## Indicadores gerais")

total_ocorrencias = len(df_filtrado)
setores_unicos = df_filtrado["Setor"].nunique()
tempo_medio = round(df_filtrado["Tempo"].mean(), 1)
alta_gravidade = round(
    (df_filtrado[df_filtrado["Gravidade"] == "Alta"].shape[0] / len(df_filtrado)) * 100, 1
)

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total de ocorrências", total_ocorrencias)
col2.metric("Setores impactados", setores_unicos)
col3.metric("Tempo médio resolução", tempo_medio)
col4.metric("% alta gravidade", f"{alta_gravidade}%")

st.markdown("---")

# ---------------------------
# GRÁFICOS
# ---------------------------
col_graf1, col_graf2 = st.columns(2)

with col_graf1:
    st.subheader("Ocorrências por setor")
    grafico_setor = df_filtrado["Setor"].value_counts().reset_index()
    grafico_setor.columns = ["Setor", "Quantidade"]

    fig1 = px.bar(
        grafico_setor,
        x="Setor",
        y="Quantidade",
        text="Quantidade",
        color="Setor",
        color_discrete_sequence=["#1D4ED8", "#F97316", "#0F766E", "#7C3AED", "#DC2626"]
    )
    fig1.update_traces(textposition="outside")
    fig1.update_layout(
        height=350,
        showlegend=False,
        plot_bgcolor="white",
        paper_bgcolor="white"
    )
    st.plotly_chart(fig1, use_container_width=True)

with col_graf2:
    st.subheader("Ocorrências por gravidade")
    grafico_gravidade = df_filtrado["Gravidade"].value_counts().reset_index()
    grafico_gravidade.columns = ["Gravidade", "Quantidade"]

    fig2 = px.pie(
        grafico_gravidade,
        names="Gravidade",
        values="Quantidade",
        hole=0.55,
        color="Gravidade",
        color_discrete_map={
            "Baixa": "#FACC15",
            "Média": "#F97316",
            "Alta": "#DC2626"
        }
    )
    fig2.update_layout(
        height=350,
        paper_bgcolor="white"
    )
    st.plotly_chart(fig2, use_container_width=True)

# ---------------------------
# LINHA DE TEMPO
# ---------------------------
st.subheader("Evolução das ocorrências no tempo")

evolucao = df_filtrado.groupby(df_filtrado["Data"].dt.date).size().reset_index(name="Quantidade")
evolucao.columns = ["Data", "Quantidade"]

fig3 = px.line(
    evolucao,
    x="Data",
    y="Quantidade",
    markers=True
)
fig3.update_layout(
    height=320,
    plot_bgcolor="white",
    paper_bgcolor="white"
)
st.plotly_chart(fig3, use_container_width=True)

# ---------------------------
# TABELA RESUMIDA
# ---------------------------
st.subheader("Resumo das ocorrências filtradas")

st.dataframe(
    df_filtrado[["Data", "Setor", "Responsável", "Tipo", "Gravidade", "Status", "Tempo"]],
    use_container_width=True
)