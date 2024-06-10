from datetime import datetime
import streamlit as st
import plotly.express as px
import pandas as pd
import pydeck as pdk
import json

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
    

def getSidebar(secetbox:bool=True) -> int:
    selected_style = 0
    if secetbox:
        selected_style = st.selectbox("Select Map Style", list(map_styles.keys()), index=7)
    st.markdown("""
                > Team
                1. Nur Fatiq (09040622071)
                2. Raden Roro Dalilati Nabilah Karamina (09040622074)
                3. Moch Hilu Maulidy (09020622034)
            """, unsafe_allow_html=True)
    st.markdown("***")
    st.markdown("""
        <P>Tugas Uas Matakuliah Visualisasi Data 2024</P>
        """, unsafe_allow_html=True)
    return selected_style

def getData(filename:str)-> pd.DataFrame:
    with open(filename, 'r') as json_file:
        data = json.load(json_file)
    df = pd.DataFrame(data)
    df[['latitude', 'longitude']] = df['Coordinates'].str.split(',', expand=True)
    df['Kedalaman'] = df['Kedalaman'].apply(lambda x: ' '.join(x.split()[:1]))
    df['DateTime'] = pd.to_datetime(df['DateTime'])
    for label in ['latitude', 'longitude', 'Magnitude', 'Kedalaman']:
        df[label] = df[label].astype(float)
    return df


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

def assign_color(magnitude):
    if magnitude < 3.0:
        return [72, 72, 72]  
    elif magnitude < 4.0:
        return [0, 0, 225]  
    elif magnitude < 5.0:
        return [0, 255, 255]  
    elif magnitude < 6.0:
        return [0, 255, 0]  
    elif magnitude < 7.0:
        return [255, 255, 0]  
    elif magnitude < 8.0:
        return [255, 165, 0]  
    else:
        return [255, 0, 0] 

def getLayer(dataframe:pd.DataFrame, radius:int) -> pdk.Layer:
    dataframe['radius'] = dataframe['Magnitude'] * radius
    dataframe['color'] = dataframe['Magnitude'].apply(lambda x: assign_color(x))

    layer = pdk.Layer(
        "ScatterplotLayer",
        data=dataframe,
        pickable=True,
        opacity=1.0,
        stroked=True,
        filled=True,
        radius_scale=1,  
        radius_min_pixels=5,
        radius_max_pixels=60,
        line_width_min_pixels=1,
        get_position=["longitude", "latitude"],
        get_radius=["radius"],
        get_fill_color="color",
        get_line_color=[225,225,225],
        tooltip={"text": "{Magnitude} magnitude earthquake at {Wilayah}"},
    )
    return layer

def getMapChart(dataframe:pd.DataFrame, style) -> pdk.Deck:
    return (
        pdk.Deck(
            layers=[getLayer(dataframe,1)],
            initial_view_state=pdk.ViewState(latitude=-2.5, longitude=118.0, zoom=4),
            tooltip={"text": "Magnitude: {Magnitude} \nTanggal: {Tanggal} \nJam: {Jam} \n{Wilayah}"},
            map_style=map_styles[style]
        )
    )

month_mapping = {
    'Jan': '01', 'Feb': '02', 'Mar': '03', 'Apr': '04',
    'Mei': '05', 'Jun': '06', 'Juli': '07', 'Agu': '08',
    'Sep': '09', 'Okt': '10', 'Nov': '11', 'Des': '12'
}

def parse_indonesian_date(date_str):
    day, month, year = date_str.split()
    month = month_mapping[month]
    return datetime.strptime(f'{day} {month} {year}', '%d %m %Y')

def getBarChart(df:pd.DataFrame):
    counts = df.groupby('Tanggal').size().reset_index(name='Count')
    counts['Tanggal'] = counts['Tanggal'].apply(parse_indonesian_date)
    counts['Tanggal'] = counts['Tanggal'].dt.strftime('%y/%m/%d')
    st.write("""<p style="text-align: center; font-weight: bold;">Banyak Gempa</p>""", unsafe_allow_html=True)
    st.bar_chart(counts.set_index('Tanggal'))