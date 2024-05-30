import streamlit as st
import plotly.express as px
import pandas as pd
import pydeck as pdk
import requests

map_styles = {
    "Streets": "mapbox://styles/mapbox/streets-v11",
    "Outdoors": "mapbox://styles/mapbox/outdoors-v11",
    "Satellite": "mapbox://styles/mapbox/satellite-v9",
    "Satellite Streets": "mapbox://styles/mapbox/satellite-streets-v11",
    "Navigation Day": "mapbox://styles/mapbox/navigation-day-v1",
    "Navigation Night": "mapbox://styles/mapbox/navigation-night-v1",
    "Light": "mapbox://styles/mapbox/light-v10",
    "Dark": "mapbox://styles/mapbox/dark-v10",
}

markdown =  ("""
                > Team
                1. Nur Fatiq (09040622071)
                2. Raden Roro Dalilati Nabilah Karamina (09040622074)
                3. Moch Hilu Maulidy (09020622034)
            """)

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
        df[['latitude', 'longitude']] = df['Coordinates'].str.split(',', expand=True)
        df['Kedalaman'] = df['Kedalaman'].apply(lambda x: ' '.join(x.split()[:1]))
        df['DateTime'] = pd.to_datetime(df['DateTime'])
        for label in ['latitude', 'longitude', 'Magnitude', 'Kedalaman']:
            df[label] = df[label].astype(float)
        return df
    else:
        return None


def scatterPlot(dataframe:pd.DataFrame):
    fig = px.scatter(dataframe, x='Magnitude', y='Kedalaman',title='Magnitude dan Kedalaman Gempa Bumi', hover_data=['Wilayah'], labels={"Kedalaman": "Kedalaman (km)"})
    fig.update_layout(title={'x':0.35})
    return fig


def lineChart(dataframe:pd.DataFrame):
    fig = px.line(dataframe, x='DateTime', y='Magnitude', title='Timeline Magnitudes Gempa', markers=True, hover_data=['Wilayah'])
    fig.update_layout(title={'x':0.35})
    return fig

def donutChart(dataframe:pd.DataFrame, groupby:str, title:str):
    counts = dataframe.groupby(groupby).size().reset_index(name='Count')
    fig = px.pie(counts, values=counts['Count'], names=counts[groupby], hole=.4, title=title)
    fig.update_layout(title={'x':0.2})
    return fig

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

def getMapChart(dataframe:pd.DataFrame, style) -> pdk.Deck:
    return (
        pdk.Deck(
            layers=[getLayer(dataframe,100000,[0, 225,0]), getLayer(dataframe,50000,[225,255,0]), getLayer(dataframe,1,[255,0,0])],
            initial_view_state=pdk.ViewState(latitude=-2.5, longitude=118.0, zoom=4),
            map_style=map_styles[style]
        )
    )