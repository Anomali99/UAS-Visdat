from function.config import configuration
from function.chart import getSidebar
from data import gempa_m5, gempa_dirasakan
import streamlit as st
import pandas as pd
import json

# Panggil fungsi konfigurasi
configuration()

# Fungsi untuk mengambil data dari file JSON
def getData(filename: str) -> dict:
    try:
        with open(filename, 'r') as json_file:
            data = json.load(json_file)
        return data
    except FileNotFoundError:
        print(f"File {filename} not found.")
        return {}
    except json.JSONDecodeError:
        print(f"Error decoding JSON from the file {filename}.")
        return {}

# Sidebar menggunakan getSidebar dari fungsi chart
with st.sidebar:
    getSidebar(secretbox=False)

# Judul dan deskripsi tabel pertama
st.write("""<h3 style="text-align: center; margin-top:0;">Table Data Gempa Bumi</h3>""", unsafe_allow_html=True)
st.markdown("***")

# Tabel pertama: 15 Gempa Bumi Terbaru di Indonesia
st.write("""<p style="text-align: center; font-weight: bold;">15 Gempa Bumi Terbaru di Indonesia</p>""", unsafe_allow_html=True)
gempa_dirasakan_data = getData(gempa_dirasakan)
if gempa_dirasakan_data:
    st.dataframe(pd.DataFrame(gempa_dirasakan_data))
    st.download_button(
        label="Download JSON",
        data=json.dumps(gempa_dirasakan_data, indent=4),
        file_name='data-gempa-terbaru.json',
        mime='application/json'
    )
else:
    st.write("Data gempa bumi terbaru tidak tersedia.")

st.markdown("***")

# Tabel kedua: 15 Gempa Bumi dengan M 5.0+ di Indonesia
st.write("""<p style="text-align: center; font-weight: bold;">15 Gempa Bumi dengan M 5.0+ di Indonesia</p>""", unsafe_allow_html=True)
gempa_m5_data = getData(gempa_m5)
if gempa_m5_data:
    st.dataframe(pd.DataFrame(gempa_m5_data))
    st.download_button(
        label="Download JSON",
        data=json.dumps(gempa_m5_data, indent=4),
        file_name='data-gempa-M5.0+.json',
        mime='application/json'
    )
else:
    st.write("Data gempa bumi dengan magnitudo 5.0+ tidak tersedia.")
