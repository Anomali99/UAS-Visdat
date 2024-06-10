from config import configuration, getSidebar, getData
import streamlit as st, pandas as pd, requests, json

configuration()

with st.sidebar:
    getSidebar(secetbox=False)

st.write("""<h3 style="text-align: center; margin-top:0;">Table Data Gempa Bumi</h3>""", unsafe_allow_html=True)
st.markdown("***")
st.write("""<p style="text-align: center; font-weight: bold;">15 Gempa Bumi Terbaru di Indonesia</p>""", unsafe_allow_html=True)
st.dataframe(getData("data-gempa-terbaru.json"))
st.markdown("***")
st.write("""<p style="text-align: center; font-weight: bold;">15 Gempa Bumi dengan M 5.0+ di Indonesia</p>""", unsafe_allow_html=True)
st.dataframe(getData("data-gempa-M5.0+.json"))
