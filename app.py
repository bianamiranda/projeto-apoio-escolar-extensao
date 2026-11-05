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

# Inicialização dos dados na sessão do usuário
if "df_alunos" not in st.session_state:
  st.session_state.df_alunos = pd.DataFrame({
      "Aluno": [
          "Ana Silva",
          "Carla Lima",
          "Fernando Dias",
          "Gabriela Rocha",
          "Bruno Santos",
          "Diego Costa",
          "Elena Souza",
      ],
      "Nota": [8.5, 9.0, 7.0, 6.5, 4.2, 5.5, 3.8],
      "Frequencia_Pct": [85, 95, 92, 88, 62, 75, 58],
  })

# Classificação automática de Risco
df = st.session_state.df_alunos.copy()
df["Status_Risco"] = df.apply(
    lambda r: (
        "⚠️ Alto Risco (Alerta)"
        if (r["Nota"] < 6.0 or r["Frequencia_Pct"] < 75)
        else "✅ Adequado"
    ),
    axis=1,
)

# Métricas Principais
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total de Alunos", len(df))
col2.metric("Média Geral de Notas", f"{df['Nota'].mean():.2f}")
col3.metric("Frequência Média", f"{df['Frequencia_Pct'].mean():.1f}%")
col4.metric(
    "Alunos em Risco", len(df[df["Status_Risco"].str.contains("Alto Risco")])
)

st.divider()

# Gráficos
c1, c2 = st.columns(2)

with c1:
  st.subheader("Distribuição do Desempenho por Nota")
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
  )
  st.plotly_chart(fig_scatter, use_container_width=True)

st.divider()

# Tabela Interativa de Cadastro e Edição
st.subheader("📝 Cadastro e Edição de Alunos em Tempo Real")
st.info(
    "Qualquer usuário pode adicionar novas linhas ou alterar dados na tabela"
    " abaixo:"
)

df_editado = st.data_editor(
    st.session_state.df_alunos, num_rows="dynamic", use_container_width=True
)

if st.button("💾 Atualizar Indicadores e Gráficos"):
  st.session_state.df_alunos = df_editado
  st.success("Painel e indicadores atualizados com sucesso!")
  st.rerun()
