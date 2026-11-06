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

SHEET_URL = "https://docs.google.com/spreadsheets/d/1MK9DkoRh3LJdf2iLcBEF61I2W_FGnPtCqbMdaYmkjTQ/export?format=csv"

# Barra lateral para opções de importação
st.sidebar.header("📁 Fonte de Dados")
modo_dados = st.sidebar.radio(
    "Escolha como carregar os dados:",
    ["Google Sheets (Automático)", "Enviar arquivo CSV local"],
)

uploaded_file = None
if modo_dados == "Enviar arquivo CSV local":
  uploaded_file = st.sidebar.file_uploader(
      "Envie sua planilha em CSV", type=["csv"]
  )


@st.cache_data(ttl=10)
def carregar_dados_web():
  try:
    df = pd.read_csv(SHEET_URL)
    return df
  except Exception as e:
    st.error(f"Erro ao carregar dados da planilha online: {e}")
    return pd.DataFrame()


# Lógica para definir de onde os dados vêm
if uploaded_file is not None:
  try:
    df = pd.read_csv(uploaded_file)
    st.sidebar.success("Arquivo CSV carregado com sucesso!")
  except Exception as e:
    st.error(f"Erro ao ler o arquivo CSV enviado: {e}")
    df = pd.DataFrame()
else:
  df = carregar_dados_web()

# Tratamento e limpeza dos dados
if not df.empty:
  colunas_uteis = ["Aluno", "Nota", "Frequencia_Pct", "Observacoes"]
  df = df[[c for c in colunas_uteis if c in df.columns]].dropna(subset=["Aluno"])

  if "Nota" in df.columns:
    df["Nota"] = pd.to_numeric(
        df["Nota"].astype(str).str.replace(",", "."), errors="coerce"
    )
  if "Frequencia_Pct" in df.columns:
    df["Frequencia_Pct"] = (
        df["Frequencia_Pct"]
        .astype(str)
        .str.replace("%", "", regex=True)
        .str.replace(",", ".", regex=True)
    )
    df["Frequencia_Pct"] = pd.to_numeric(df["Frequencia_Pct"], errors="coerce")

# Classificação automática de Risco
if not df.empty:
  df["Status_Risco"] = df.apply(
      lambda r: (
          "⚠️ Alto Risco (Alerta)"
          if (r["Nota"] < 6.0 or r["Frequencia_Pct"] < 75)
          else "✅ Adequado"
      ),
      axis=1,
  )

CORES_RISCO = {
    "✅ Adequado": "#2980b9",
    "⚠️ Alto Risco (Alerta)": "#e74c3c",
}

# Métricas Principais (KPIs)
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total de Alunos", len(df) if not df.empty else 0)
col2.metric(
    "Média Geral de Notas",
    f"{df['Nota'].mean():.2f}" if not df.empty and "Nota" in df else "0.00",
)
col3.metric(
    "Frequência Média",
    f"{df['Frequencia_Pct'].mean():.1f}%"
    if not df.empty and "Frequencia_Pct" in df
    else "0%",
)
col4.metric(
    "Alunos em Risco",
    len(df[df["Status_Risco"].str.contains("Alto Risco", na=False)])
    if not df.empty and "Status_Risco" in df
    else 0,
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
        color_discrete_map=CORES_RISCO,
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
        color_discrete_map=CORES_RISCO,
        hover_name="Aluno",
        hover_data=["Observacoes"],
    )
    fig_scatter.update_traces(marker=dict(size=14))
    st.plotly_chart(fig_scatter, use_container_width=True)

st.divider()

# Tabela Sincronizada e Opção de Download
st.subheader("📝 Registros Oficiais Sincronizados")
# Tabela interativa editável para alteração direta de dados
df_editado = st.data_editor(
    df,
    num_rows="dynamic",
    use_container_width=True
)

if not df.empty:
  csv_data = df.to_csv(index=False).encode("utf-8")
  st.download_button(
      label="📥 Baixar dados consolidados em CSV",
      data=csv_data,
      file_name="relatorio_apoio_escolar.csv",
      mime="text/csv",
  )
