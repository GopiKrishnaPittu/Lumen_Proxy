import streamlit as st
import sqlite3
import pandas as pd
from streamlit_echarts import st_echarts

# Set page configuration for a "Cyber-Dark" theme
st.set_page_config(page_title="Lumen Proxy SOC", layout="wide")

# Custom CSS for "Blinking" alerts and "Hover" responsiveness
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stMetric { background-color: #161b22; padding: 15px; border-radius: 10px; border: 1px solid #30363d; transition: 0.3s; }
    .stMetric:hover { border-color: #58a6ff; transform: translateY(-5px); background-color: #1c2128; }
    
    @keyframes blink { 0% { opacity: 1; } 50% { opacity: 0.3; } 100% { opacity: 1; } }
    .blink-red { color: #ff4b4b; font-weight: bold; animation: blink 1s infinite; }
    </style>
""", unsafe_allow_html=True)

def get_data():
    conn = sqlite3.connect("lumen_proxy.db")
    df = pd.read_sql_query("SELECT * FROM security_logs", conn)
    conn.close()
    return df

st.title("🛡️ LUMEN PROXY: WEBSCALE SOC")
st.markdown("---")

df = get_data()

# --- TOP ROW: DYNAMIC METRICS ---
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total Traffic", len(df))
with col2:
    red_count = len(df[df['decision'].str.contains('RED')])
    st.markdown(f"### <span class='blink-red'>Critical Threats: {red_count}</span>", unsafe_allow_html=True)
with col3:
    yellow_count = len(df[df['decision'] == 'YELLOW'])
    st.metric("Escalations", yellow_count)
with col4:
    st.metric("System Status", "ONLINE", delta="Active")

# --- MIDDLE ROW: DYNAMIC GRAPHICS ---
st.subheader("📊 Attack Vector Analysis")
c1, c2 = st.columns([2, 1])

with c1:
    # Interactive Pie Chart
    decision_counts = df['decision'].value_counts()
    options = {
        "tooltip": {"trigger": "item"},
        "legend": {"top": "5%", "left": "center", "textStyle": {"color": "#ccc"}},
        "series": [{
            "name": "Threat Levels",
            "type": "pie",
            "radius": ["40%", "70%"],
            "avoidLabelOverlap": False,
            "itemStyle": {"borderRadius": 10, "borderColor": "#0e1117", "borderWidth": 2},
            "label": {"show": False, "position": "center"},
            "emphasis": {"label": {"show": True, "fontSize": "20", "fontWeight": "bold"}},
            "data": [{"value": int(v), "name": k} for k, v in decision_counts.items()]
        }]
    }
    st_echarts(options=options, height="400px")

with c2:
    st.subheader("📜 Recent Events")
    st.dataframe(df[['timestamp', 'decision', 'score']].tail(10), use_container_width=True)

# --- REFRESH BUTTON ---
if st.button('🔄 Refresh Live Feed'):
    st.rerun()
