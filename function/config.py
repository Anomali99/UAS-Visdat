import streamlit as st
import pandas as pd
import json

def configuration():
    st.set_page_config(
        page_title="Dashboard - Earthquake",
        page_icon="https://www.bmkg.go.id//asset/img/favicon.ico",
        layout="wide",
        initial_sidebar_state="collapsed")

    st.set_option("deprecation.showPyplotGlobalUse", False)

    st.markdown("""
        <style>
            [data-testid="stSidebarNav"] {
                background-image: url(https://www.bmkg.go.id/asset/img/logo/logo-bmkg.png);
                background-position: center 20px;
                background-repeat: no-repeat;
                padding-top: 130px;
            }
        </style>
        """, unsafe_allow_html=True)
    

def getData(filename: str) -> pd.DataFrame:
    try:
        with open(filename, 'r') as json_file:
            data = json.load(json_file)
    except FileNotFoundError:
        print(f"File {filename} not found.")
        return pd.DataFrame()
    except json.JSONDecodeError:
        print(f"Error decoding JSON from the file {filename}.")
        return pd.DataFrame()

    df = pd.DataFrame(data)

    if 'Coordinates' in df.columns:
        df[['latitude', 'longitude']] = df['Coordinates'].str.split(',', expand=True)
    else:
        print(f"Coordinates column not found in the data.")
        return pd.DataFrame()

    if 'Kedalaman' in df.columns:
        df['Kedalaman'] = df['Kedalaman'].apply(lambda x: x.split()[0])
    else:
        print(f"Kedalaman column not found in the data.")
        return pd.DataFrame()

    if 'DateTime' in df.columns:
        df['DateTime'] = pd.to_datetime(df['DateTime'])
    else:
        print(f"DateTime column not found in the data.")
        return pd.DataFrame()

    for label in ['latitude', 'longitude', 'Magnitude', 'Kedalaman']:
        if label in df.columns:
            df[label] = df[label].astype(float)
        else:
            print(f"{label} column not found in the data.")
            return pd.DataFrame()

    return df
