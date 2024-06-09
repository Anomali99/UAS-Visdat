import streamlit as st
import requests, json, time, schedule

def _check_json(title:str):
    try:
        with open(title, 'r') as json_file:
            data = json.load(json_file)
        return data
    except FileNotFoundError:
        return None

def _hit_api(url:str, title:str):
    headers = {
        "Content-Type": "application/json",
        "Accept": "*/*",
        "User-Agent":"Anoamali99",
    }
    response = requests.get(url, headers=headers)
    new_data = response.json()['Infogempa']['gempa']

    existing_data = _check_json(title=title)
    if existing_data is not None:
        combined_data = {f"{item['DateTime']}_{item['Coordinates']}": item for item in existing_data}
        for item in new_data:
            key = f"{item['DateTime']}_{item['Coordinates']}"
            combined_data[key] = item
        
        combined_data = list(combined_data.values())
    else:
        combined_data = new_data

    with open(title, 'w') as json_file:
        json.dump(combined_data, json_file)

def _fetch_and_store_data():
    _hit_api(url="https://data.bmkg.go.id/DataMKG/TEWS/gempadirasakan.json", title='data-gempa-terbaru.json')
    _hit_api(url="https://data.bmkg.go.id/DataMKG/TEWS/gempaterkini.json", title='data-gempa-M5.0+.json')
    print("Data fetched and stored at", time.strftime("%Y-%m-%d %H:%M:%S"))

def run_scheduler():
    schedule.every(12).hours.do(_fetch_and_store_data)
    _fetch_and_store_data()
    while True:
        schedule.run_pending()
        time.sleep(1)