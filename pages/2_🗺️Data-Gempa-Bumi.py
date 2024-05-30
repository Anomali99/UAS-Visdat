import streamlit as st
import plotly.express as px
import pandas as pd
import pydeck as pdk
import requests


st.set_page_config(
    page_title="Dashboard - Earthquake",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="collapsed")

st.set_option("deprecation.showPyplotGlobalUse", False)


url_terbaru = 'https://data.bmkg.go.id/DataMKG/TEWS/gempadirasakan.json'
url_M5 = 'https://data.bmkg.go.id/DataMKG/TEWS/gempaterkini.json'

st.sidebar.markdown(
        """
            > Team
            1. Nur Fatiq (09040622071)
            2. Raden Roro Dalilati Nabilah Karamina (09040622074)
            3. Moch Hilu Maulidy (09020622034)
        """,
        unsafe_allow_html=True,
    )


def getData(url:str)-> pd.DataFrame:
    headers = {
        "Content-Type": "application/json",
        "Accept": "*/*",
        "User-Agent":"Anoamali99",
        }
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        gempa = response.json()['Infogempa']['gempa']
        df = pd.DataFrame(gempa)
        return df
    else:
        return None


st.write("""<h3 style="text-align: center; margin-top:0;">Table Data Gempa Bumi</h3>""", unsafe_allow_html=True)
st.markdown("***")
st.write("""<p style="text-align: center; font-weight: bold;">15 Gempa Bumi Terbaru di Indonesia</p>""", unsafe_allow_html=True)
st.dataframe(getData(url_terbaru))
st.markdown("***")
st.write("""<p style="text-align: center; font-weight: bold;">15 Gempa Bumi dengan M 5.0+ di Indonesia</p>""", unsafe_allow_html=True)
st.dataframe(getData(url_M5))
