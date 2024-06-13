import streamlit as st
import requests, json, time, schedule, os
from dateutil import parser
from data import gempa_dirasakan, gempa_m5
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def _sort_by_datetime(item):
    return parser.parse(item['DateTime'])

def _check_json(filepath):
    try:
        with open(filepath, 'r') as json_file:
            data = json.load(json_file)
        return data
    except FileNotFoundError:
        return None

def _hit_api(url, filepath):
    headers = {
        "Content-Type": "application/json",
        "Accept": "*/*",
        "User-Agent":"Anoamali99",
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        new_data = response.json()['Infogempa']['gempa']
    except requests.RequestException as e:
        logging.error(f"Failed to fetch data from {url}: {e}")
        return

    existing_data = _check_json(filepath)
    if existing_data is not None:
        combined_data = {f"{item['DateTime']}_{item['Coordinates']}": item for item in existing_data}
        for item in new_data:
            key = f"{item['DateTime']}_{item['Coordinates']}"
            combined_data[key] = item
        combined_data = list(combined_data.values())
    else:
        combined_data = new_data

    combined_data = sorted(combined_data, key=_sort_by_datetime, reverse=True)

    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'w') as json_file:
        json.dump(combined_data, json_file, indent=4)

def _fetch_and_store_data():
    _hit_api(url="https://data.bmkg.go.id/DataMKG/TEWS/gempadirasakan.json", filepath=gempa_dirasakan)
    _hit_api(url="https://data.bmkg.go.id/DataMKG/TEWS/gempaterkini.json", filepath=gempa_m5)
    logging.info("Data fetched and stored")

def run_scheduler():
    schedule.every(12).hours.do(_fetch_and_store_data)
    _fetch_and_store_data()
    while True:
        schedule.run_pending()
        time.sleep(1)