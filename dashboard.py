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
st.markdown(f"<html style='scroll-behavior: smooth;'></html>", unsafe_allow_html=True)

url = 'https://data.bmkg.go.id/DataMKG/TEWS/gempadirasakan.json'


def getData()-> pd.DataFrame:
    headers = {
        "Content-Type": "application/json",
        "Accept": "*/*",
        "User-Agent":"Anoamali99",
        }
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        gempa = response.json()['Infogempa']['gempa']
        df = pd.DataFrame(gempa)
        df[['latitude', 'longitude']] = df['Coordinates'].str.split(',', expand=True)
        df['latitude'] = df['latitude'].astype(float)
        df['longitude'] = df['longitude'].astype(float)
        df['Magnitude'] = df['Magnitude'].astype(float)
        df['DateTime'] = pd.to_datetime(df['DateTime'])
        df['Kedalaman'] = df['Kedalaman'].apply(lambda x: ' '.join(x.split()[:1]))
        df['Kedalaman'] = df['Kedalaman'].astype(float)
        df['Wilayah_Unique'] = df['Wilayah'].apply(lambda x: 
            'di darat' if 'di darat' in x.lower() or 'didarat' in x.lower() 
            else 'di laut' if 'di laut' in x.lower() or 'dilaut' in x.lower() 
            else None
            )
        return df
    else:
        return None

def getLayer(dataframe:pd.DataFrame, radius:int, color=[0, 0, 0]) -> pdk.Layer:
    dataframe['radius'] = dataframe['Magnitude'] * radius

    layer = pdk.Layer(
        "ScatterplotLayer",
        data=dataframe,
        pickable=False,
        opacity=0.1,
        stroked=True,
        filled=True,
        radius_scale=1,  
        radius_min_pixels=5,
        radius_max_pixels=60,
        line_width_min_pixels=1,
        get_position=["longitude", "latitude"],
        get_radius=["radius"],
        get_fill_color=color,
        get_line_color=color,
        tooltip={"text": "{Magnitude} magnitude earthquake at {Wilayah}"},
    )
    return layer

def scatterPlot(dataframe:pd.DataFrame):
    fig = px.scatter(dataframe, x='Magnitude', y='Kedalaman',title='Magnitude dan Kedalaman Gempa Bumi', hover_data=['Wilayah'], labels={"Kedalaman": "Kedalaman (km)"})
    fig.update_layout(title={'x':0.35})
    return fig


def lineChart(dataframe:pd.DataFrame):
    fig = px.line(dataframe, x='DateTime', y='Magnitude', title='Timeline Magnitudes Gempa', markers=True, hover_data=['Wilayah'])
    fig.update_layout(title={'x':0.35})
    return fig

def donutChart(dataframe:pd.DataFrame):
    dataframe['Depth'] = dataframe['Kedalaman'].apply(lambda x: 'D < 10' if x < 10 else '10 ≤ D < 20' if 10 <= x < 20 else 'D ≥ 20')
    counts = dataframe.groupby('Depth').size().reset_index(name='Count')
    fig = px.pie(counts, values=counts['Count'], names=counts['Depth'], hole=.4, title="Berdasarkan Kedalaman")
    fig.update_layout(title={'x':0.2})
    return fig


df = getData()

st.write("""<h3 style="text-align: center; margin-top:0;">Visualisasi Data Gemap Bumi</h3>""", unsafe_allow_html=True)
st.markdown("***")

col1, col2 = st.columns([8, 2], gap="medium")
col3, col4 = st.columns([5, 5], gap="medium")

with col2:
    unique_wilayah = df['Wilayah_Unique'].unique()
    selected_wilayah = st.multiselect('Pusat Gempa:', unique_wilayah, default=unique_wilayah)
    df = df[df['Wilayah_Unique'].isin(selected_wilayah)]

    min_value = df['Magnitude'].min()
    max_value = df['Magnitude'].max()
    min, max = st.slider(label = "Magnitude:",
                                min_value = min_value,
                                max_value = max_value,
                                value = (min_value,max_value))
    df = df[df['Magnitude'].between(min, max)]
    
    st.plotly_chart(donutChart(df), use_container_width=True)



with col1:
    st.write("""<p style="text-align: center; font-weight: bold;">15 Titik Gempa Bumi Terbaru di Indonesia</p>""", unsafe_allow_html=True)
    st.pydeck_chart(
        pdk.Deck(
            layers=[getLayer(df,100000,[0, 225,0]), getLayer(df,50000,[225,255,0]), getLayer(df,1,[255,0,0])],
            initial_view_state=pdk.ViewState(latitude=-2.5, longitude=118.0, zoom=4),
            map_style="mapbox://styles/mapbox/dark-v10"
        )
    )

    

col3.plotly_chart(scatterPlot(df))
col4.plotly_chart(lineChart(df))
