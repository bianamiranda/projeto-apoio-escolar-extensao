import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(
    page_title="Painel de Apoio Escolar", page_icon="📊", layout="wide"
)

st.title(
    "📊 Painel de Análise de Desempenho e Prevenção à Evasão Escolar"
)
st.caption("Projeto de Extensão Universitária em Ciência de Dados - Apoio Escolar Digital")

# Link oficial da planilha exportada em CSV do Google Drive
SHEET_URL = "https://docs.google.com/spreadsheets/d/1MK9DkoRh3LJdf2iLcBEF61I2W_FGnPtCqbMdaYmkjTQ/export?format=csv"


@st.cache_data(ttl=10)
def carregar_dados():
  try:
    return pd.read_csv(SHEET_URL)
  except Exception as e:
    st.error(f"Erro ao carregar dados da planilha: {e}")
    return pd.DataFrame(
        columns=["Aluno", "Nota", "Frequencia_Pct", "Observacoes"]
    )


# Carrega os dados da planilha
df = carregar_dados()

# Garantir colunas essenciais
if "Status_Risco" not in df.columns:
  df["Status_Risco"] = df.apply(
      lambda r: (
          "⚠️ Alto Risco (Alerta)"
          if (r["Nota"] < 6.0 or r["Frequencia_Pct"] < 75)
          else "✅ Adequado"
      ),
      axis=1,
  )

# Métricas Principais (KPIs)
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total de Alunos", len(df))
col2.metric(
    "Média Geral de Notas",
    f"{df['Nota'].mean():.2f}" if not df.empty else "0.00",
)
col3.metric(
    "Frequência Média",
    f"{df['Frequencia_Pct'].mean():.1f}%" if not df.empty else "0%",
)
col4.metric(
    "Alunos em Risco",
    len(df[df["Status_Risco"].str.contains("Alto Risco", na=False)]),
)

st.divider()

# Gráficos
c1, c2 = st.columns(2)

with c1:
  st.subheader("Distribuição do Desempenho por Nota")
  if not df.empty:
    fig_bar = px.bar(
        df,
        x="Aluno",
        y="Nota",
        color="Status_Risco",
        color_discrete_map={
            "✅ Adequado": "#2ecc71",
            "⚠️ Alto Risco (Alerta)": "#e74c3c",
        },
        text_auto=True,
    )
    st.plotly_chart(fig_bar, use_container_width=True)

with c2:
  st.subheader("Relação Frequência vs Nota")
  if not df.empty:
    fig_scatter = px.scatter(
        df,
        x="Frequencia_Pct",
        y="Nota",
        color="Status_Risco",
        color_discrete_map={
            "✅ Adequado": "#2ecc71",
            "⚠️ Alto Risco (Alerta)": "#e74c3c",
        },
        hover_name="Aluno",
        hover_data=["Observacoes"],
    )
    st.plotly_chart(fig_scatter, use_container_width=True)

st.divider()

# Exibição e Consulta dos Dados Oficiais do Google Sheets
st.subheader("📝 Registros Oficiais Sincronizados com o Google Sheets")
st.info(
    "Estes dados são carregados em tempo real da sua planilha oficial no"
    " Google Drive."
)
st.dataframe(df, use_container_width=True)

