from config import map_styles, markdown, getData, getMapChart, lineChart, scatterPlot, donutChart
import streamlit as st
import plotly.express as px
import pandas as pd
import pydeck as pdk


st.set_page_config(
    page_title="Dashboard - Earthquake",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="collapsed")

st.set_option("deprecation.showPyplotGlobalUse", False)

url = 'https://data.bmkg.go.id/DataMKG/TEWS/gempaterkini.json'


df = getData(url)

with st.sidebar:
    selected_style = st.selectbox("Select Map Style", list(map_styles.keys()), index=7)
    st.markdown(markdown, unsafe_allow_html=True)

st.write("""<h3 style="text-align: center; margin-top:0;">Visualisasi Data Gempa Bumi dengan M 5.0+</h3>""", unsafe_allow_html=True)
st.markdown("***")

col1, col2 = st.columns([8, 2], gap="medium")
col3, col4 = st.columns([5, 5], gap="medium")

with col2:
    min_value_kedalaman = df['Kedalaman'].min() if len(df) > 0 else 0
    max_value_kedalaman = df['Kedalaman'].max() if len(df) > 0 else 1
    min_kedalaman, max_kedalaman = st.slider(label = "Kedalaman (km):",
                                min_value = min_value_kedalaman,
                                max_value = max_value_kedalaman,
                                value = (min_value_kedalaman,max_value_kedalaman))
    df = df[df['Kedalaman'].between(min_kedalaman, max_kedalaman)]

    min_value_magnitude = df['Magnitude'].min() if len(df) > 0 else 0
    max_value_magnitude = df['Magnitude'].max() if len(df) > 0 else 1
    min_magnitude, max_magnitude = st.slider(label = "Magnitude:",
                                min_value = min_value_magnitude,
                                max_value = max_value_magnitude,
                                value = (min_value_magnitude,max_value_magnitude))
    df = df[df['Magnitude'].between(min_magnitude, max_magnitude)]
    
    df['Potensi Stunami'] = df['Potensi'].apply(lambda x: ' '.join(x.split()[:1]))
    st.plotly_chart(donutChart(df, groupby='Potensi Stunami', title="Berpotensi Stunami"), use_container_width=True)

with col1:
    st.write("""<p style="text-align: center; font-weight: bold;">15 Titik Gempa Bumi dengan M 5.0+ di Indonesia</p>""", unsafe_allow_html=True)
    st.pydeck_chart(getMapChart(df,style=selected_style))

col3.plotly_chart(scatterPlot(df))
col4.plotly_chart(lineChart(df))
