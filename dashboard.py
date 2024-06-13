from function.config import getData, configuration
from data import gempa_dirasakan
from function.rest_api import run_scheduler
from function.chart import getSidebar, getMapChart, donutChart, scatterPlot, getBarChart
import streamlit as st, threading

scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
scheduler_thread.start()

configuration()

df = getData(gempa_dirasakan)

with st.sidebar:
    selected_style =  getSidebar()

st.write("""<h3 style="text-align: center; margin-top:0;">Visualisasi Data Gempa Bumi</h3>""", unsafe_allow_html=True)
st.markdown("***")

col1, col2 = st.columns([8, 2], gap="medium")
col3, col4 = st.columns([5, 5], gap="medium")

with col2:
    df['Wilayah_Unique'] = df['Wilayah'].apply(lambda x: 
            'di darat' if 'di darat' in x.lower() or 'didarat' in x.lower() 
            else 'di laut' if 'di laut' in x.lower() or 'dilaut' in x.lower() 
            else None
            )
    unique_wilayah = df['Wilayah_Unique'].unique()
    selected_wilayah = st.multiselect('Pusat Gempa:', unique_wilayah, default=unique_wilayah)
    df = df[df['Wilayah_Unique'].isin(selected_wilayah)]

    min_value = df['Magnitude'].min() if len(df) > 0 else 0
    max_value = df['Magnitude'].max() if len(df) > 0 else 1
    min, max = st.slider(label = "Magnitude:",
                                min_value = min_value,
                                max_value = max_value,
                                value = (min_value, max_value))
    df = df[df['Magnitude'].between(min, max)]
    
    df['Depth'] = df['Kedalaman'].apply(lambda x: 'D < 10' if x < 10 else '10 ≤ D < 20' if 10 <= x < 20 else 'D ≥ 20')
    st.plotly_chart(donutChart(df, groupby='Depth', title="Berdasarkan Kedalaman"), use_container_width=True)

with col1:
    st.write("""<p style="text-align: center; font-weight: bold;">Gempa Bumi Terbaru di Indonesia</p>""", unsafe_allow_html=True)
    st.pydeck_chart(getMapChart(df,style=selected_style))

col3.plotly_chart(scatterPlot(df))

with col4:
    getBarChart(df)
