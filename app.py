import streamlit as st
import pandas as pd
import plotly.express as px

# Configuração da página
st.set_page_config(page_title="Apoio Escolar - Análise de Desempenho", layout="wide")

st.title("📊 Painel de Análise de Desempenho e Prevenção à Evasão Escolar")
st.markdown("Projeto de Extensão Universitária em Ciência de Dados — Apoio Escolar Digital")

# Dados simulados para execução imediata
data_default = {
    "Aluno": ["Ana Silva", "Bruno Santos", "Carla Lima", "Diego Costa", "Elena Souza", "Fernando Dias", "Gabriela Rocha"],
    "Disciplina": ["Matemática", "Português", "História", "Ciências", "Matemática", "Português", "História"],
    "Nota": [8.5, 4.2, 9.0, 5.5, 3.8, 7.0, 6.5],
    "Frequencia_Pct": [92, 65, 98, 80, 58, 88, 90]
}

# Interface para carregar arquivo ou usar dados demonstrativos
st.sidebar.header("Configurações do Projeto")
opcao_dados = st.sidebar.radio("Fonte de Dados:", ("Dados Demonstrativos do Projeto", "Carregar Planilha (CSV/XLSX)"))

if opcao_dados == "Carregar Planilha (CSV/XLSX)":
    uploaded_file = st.sidebar.file_uploader("Envie a planilha dos alunos", type=["csv", "xlsx"])
    if uploaded_file is not None:
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
    else:
        df = pd.DataFrame(data_default)
else:
    df = pd.DataFrame(data_default)

# Regra de Risco (Ciência de Dados aplicada à pedagogia)
df["Status_Risco"] = df.apply(
    lambda row: "⚠️ Alto Risco (Alerta)" if (row["Nota"] < 6.0 or row["Frequencia_Pct"] < 75) else "✅ Adequado", axis=1
)

# Métricas Principais
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total de Alunos Analisados", len(df["Aluno"].unique()))
col2.metric("Média Geral de Notas", f"{df['Nota'].mean():.2f}")
col3.metric("Frequência Média", f"{df['Frequencia_Pct'].mean():.1f}%")
col4.metric("Alunos em Situação de Risco", len(df[df["Status_Risco"] == "⚠️ Alto Risco (Alerta)"]))

st.divider()

# Gráficos
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("Distribuição do Desempenho por Nota")
    fig_bar = px.bar(
        df, 
        x="Aluno", 
        y="Nota", 
        color="Status_Risco",
        color_discrete_map={"✅ Adequado": "#2ecc71", "⚠️ Alto Risco (Alerta)": "#e74c3c"},
        title="Notas Individuais e Identificação de Risco"
    )
    st.plotly_chart(fig_bar, use_container_width=True)

with col_right:
    st.subheader("Relação Frequência vs Nota")
    fig_scatter = px.scatter(
        df, 
        x="Frequencia_Pct", 
        y="Nota", 
        color="Status_Risco",
        size="Nota",
        hover_name="Aluno",
        title="Dispersão: Assiduidade x Aprendizado"
    )
    st.plotly_chart(fig_scatter, use_container_width=True)

st.subheader("📋 Relatório Sintético de Intervenção Pedagógica")
st.dataframe(df, use_container_width=True)

