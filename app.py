import streamlit as st
import pandas as pd
import pymysql
import plotly.express as px
import os
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="Radar Político", page_icon="📊", layout="wide")

@st.cache_resource
def connect_db():
    return pymysql.connect(
        host=os.getenv("DB_HOST"),
        port=int(os.getenv("DB_PORT", 4000)),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
        cursorclass=pymysql.cursors.DictCursor
    )

def load_data():
    conn = connect_db()
    query = """
        SELECT sm.*, p.name, p.role, p.commune, p.political_leaning, p.instagram_handle
        FROM social_metrics sm
        JOIN politicians p ON sm.politician_id = p.id
        WHERE sm.platform = 'Instagram'
        ORDER BY sm.metric_date ASC
    """
    df = pd.read_sql(query, conn)
    conn.close()
    return df

df = load_data()

st.title("📊 Radar de Seguimiento Político")
st.markdown("Monitoreo automatizado de redes sociales para gestión estratégica.")

st.sidebar.header("Filtros de Búsqueda")
roles = ["Todos"] + sorted(df['role'].unique().tolist())
selected_role = st.sidebar.selectbox("Rol", roles)

communes = ["Todas"] + sorted(df['commune'].unique().tolist())
selected_commune = st.sidebar.selectbox("Comuna", communes)

leanings = ["Todas"] + sorted(df['political_leaning'].unique().tolist())
selected_leaning = st.sidebar.selectbox("Tendencia", leanings)

filtered_df = df.copy()
if selected_role != "Todos":
    filtered_df = filtered_df[filtered_df['role'] == selected_role]
if selected_commune != "Todas":
    filtered_df = filtered_df[filtered_df['commune'] == selected_commune]
if selected_leaning != "Todas":
    filtered_df = filtered_df[filtered_df['political_leaning'] == selected_leaning]

col1, col2, col3 = st.columns(3)
with col1:
    latest_followers = filtered_df.groupby('name')['followers_count'].last().sum()
    st.metric("Seguidores Totales (Filtrados)", f"{latest_followers:,}")
with col2:
    avg_engagement = filtered_df['engagement_rate'].mean()
    st.metric("Engagement Promedio", f"{avg_engagement:.2f}%")
with col3:
    total_spikes = filtered_df['is_activity_spike'].sum()
    st.metric("Picos de Actividad Detectados", f"{int(total_spikes)} 🚨")

st.markdown("---")

st.subheader("📈 Crecimiento de Seguidores (Histórico)")
fig_followers = px.line(
    filtered_df, x='metric_date', y='followers_count', color='name',
    markers=True, title="Evolución Semanal de Seguidores"
)
fig_followers.update_layout(xaxis_title="Fecha", yaxis_title="Seguidores", height=400)
st.plotly_chart(fig_followers, use_container_width=True)

st.subheader("💡 Comparativa de Engagement Rate")
fig_engagement = px.bar(
    filtered_df, x='name', y='engagement_rate', color='is_activity_spike',
    color_discrete_map={0: '#1f77b4', 1: '#d62728'},
    title="Engagement por Político (Rojo = Pico de Actividad / Viral)",
    barmode='group'
)
fig_engagement.update_layout(xaxis_title="Político", yaxis_title="Engagement %", height=350)
st.plotly_chart(fig_engagement, use_container_width=True)

st.subheader("🔍 Detalle de Métricas Semanales")
display_cols = ['metric_date', 'name', 'role', 'commune', 'followers_count', 'engagement_rate', 'is_activity_spike']
st.dataframe(
    filtered_df[display_cols].sort_values(by=['metric_date', 'followers_count'], ascending=[False, False]),
    use_container_width=True,
    hide_index=True
)