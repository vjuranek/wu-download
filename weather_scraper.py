#!/usr/bin/env python3
"""
Weather Underground Data Scraper (Simple API Version)
Downloads weather data from Weather Underground API and saves to CSV
"""

import csv
import os
import sys
import requests

from datetime import datetime


API_URL = "https://api.weather.com/v2/pws/history/daily"
API_KEY = os.getenv("WU_API_KEY")
STATION_ID = os.getenv("WU_STATION_ID")


def fetch_weather_data(station_id, start_date, end_date, api_key):
    """Fetch weather data from Weather Underground API"""
    params = {
        'stationId': station_id,
        'format': 'json',
        'units': 'm',  # Metric units (Celsius, millimeters, etc.)
        'startDate': start_date,
        'endDate': end_date,
        'numericPrecision': 'decimal',
        'apiKey': api_key,
    }

    try:
        response = requests.get(API_URL, params=params, timeout=30)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}", file=sys.stderr)
        sys.exit(1)


def parse_weather_data(json_data):
    """Parse JSON weather data into CSV format"""
    observations = json_data.get('observations', [])

    if not observations:
        print("Error: No observations found in response", file=sys.stderr)
        sys.exit(1)

    # Build headers from the first observation
    headers = ['Date']
    data_rows = []

    for obs in observations:
        date = obs.get('obsTimeLocal', '')[:10]  # Extract date part
        row = [date]

        # Temperature
        if 'metric' in obs:
            metric = obs['metric']

            # Temperature High/Avg/Low
            temp_high = metric.get('tempHigh', '')
            temp_avg = metric.get('tempAvg', '')
            temp_low = metric.get('tempLow', '')

            # Dew Point
            dewpt_high = metric.get('dewptHigh', '')
            dewpt_avg = metric.get('dewptAvg', '')
            dewpt_low = metric.get('dewptLow', '')

            # Pressure
            pressure_max = metric.get('pressureMax', '')
            pressure_min = metric.get('pressureMin', '')

            # Precipitation
            precip_total = metric.get('precipTotal', '')

            # Humidity
            humidity_high = obs.get('humidityHigh', '')
            humidity_avg = obs.get('humidityAvg', '')
            humidity_low = obs.get('humidityLow', '')

            # Wind Speed
            wind_speed_high = metric.get('windspeedHigh', '')
            wind_speed_avg = metric.get('windspeedAvg', '')
            wind_speed_low = metric.get('windspeedLow', '')

            # Build the row
            if not data_rows:  # First row, set headers
                headers = [
                    'Date',
                    'Temp High (°C)',
                    'Temp Avg (°C)',
                    'Temp Low (°C)',
                    'Dew Point High (°C)',
                    'Dew Point Avg (°C)',
                    'Dew Point Low (°C)',
                    'Humidity High (%)',
                    'Humidity Avg (%)',
                    'Humidity Low (%)',
                    'Wind Speed High (km/h)',
                    'Wind Speed Avg (km/h)',
                    'Wind Speed Low (km/h)',
                    'Pressure Max (mb)',
                    'Pressure Min (mb)',
                    'Precipitation (mm)'
                ]

            row = [
                date,
                temp_high,
                temp_avg,
                temp_low,
                dewpt_high,
                dewpt_avg,
                dewpt_low,
                humidity_high,
                humidity_avg,
                humidity_low,
                wind_speed_high,
                wind_speed_avg,
                wind_speed_low,
                pressure_max,
                pressure_min,
                precip_total,
            ]

        data_rows.append(row)

    return headers, data_rows


def save_to_csv(headers, data, filename):
    """Save the weather data to a CSV file"""
    try:
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(headers)
            writer.writerows(data)

        print(f"Data successfully saved to {filename}")
        print(f"Total rows: {len(data)}")
    except IOError as e:
        print(f"Error writing to file: {e}", file=sys.stderr)
        sys.exit(1)


def main():
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <start_date> <end_date>", file=sys.stderr)
        print("  Dates in YYYYMMDD format, e.g. 20260401 20260430", file=sys.stderr)
        sys.exit(1)

    start_date = sys.argv[1]
    end_date = sys.argv[2]

    print(f"Fetching weather data for station {STATION_ID} ...")
    print(f"Date range: {start_date} to {end_date}")

    json_data = fetch_weather_data(STATION_ID, start_date, end_date, API_KEY)

    print("Parsing weather data...")
    headers, data = parse_weather_data(json_data)

    output_filename = f"weather_data_{start_date}_{end_date}.csv"
    print(f"Saving data to {output_filename}...")
    save_to_csv(headers, data, output_filename)


if __name__ == "__main__":
    main()
