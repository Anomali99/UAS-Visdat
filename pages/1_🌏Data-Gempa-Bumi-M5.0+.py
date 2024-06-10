from config import  getSidebar, getMapChart, donutChart, scatterPlot, getData, configuration, getBarChart
import streamlit as st

configuration()

df = getData('data-gempa-M5.0+.json')

with st.sidebar:
    selected_style = getSidebar()

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
    st.write("""<p style="text-align: center; font-weight: bold;">Gempa Bumi dengan M 5.0+ di Indonesia</p>""", unsafe_allow_html=True)
    st.pydeck_chart(getMapChart(df,style=selected_style))

col3.plotly_chart(scatterPlot(df))
with col4:
    getBarChart(df)