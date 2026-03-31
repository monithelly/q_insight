import pandas as pd
from database import inserir_ocorrencia

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
            row["tempo_resolucao"],
            row["descricao"]
        )

    st.success("Dados de exemplo carregados com sucesso!")