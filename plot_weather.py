#!/usr/bin/env python3
"""
Weather Data Plotter
Reads CSV files produced by weather_scraper.py and generates plots.
"""

import csv
import sys
from datetime import datetime

import matplotlib.pyplot as plt
import matplotlib.dates as mdates


def read_csv(filename):
    with open(filename, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    return rows


def plot_weather(rows, output_file):
    dates = [datetime.strptime(r['Date'], '%Y-%m-%d') for r in rows]

    fig, axes = plt.subplots(6, 1, figsize=(12, 20), sharex=True)

    # Temperature
    ax = axes[0]
    ax.fill_between(dates,
                    [float(r['Temp Low (°C)']) for r in rows],
                    [float(r['Temp High (°C)']) for r in rows],
                    alpha=0.3, color='tab:red')
    ax.plot(dates, [float(r['Temp Avg (°C)']) for r in rows],
            color='tab:red', label='Avg')
    ax.set_ylabel('Temperature (°C)')
    ax.legend()
    ax.grid(True, alpha=0.3)

    # Dew Point
    ax = axes[1]
    ax.fill_between(dates,
                    [float(r['Dew Point Low (°C)']) for r in rows],
                    [float(r['Dew Point High (°C)']) for r in rows],
                    alpha=0.3, color='tab:purple')
    ax.plot(dates, [float(r['Dew Point Avg (°C)']) for r in rows],
            color='tab:purple', label='Avg')
    ax.set_ylabel('Dew Point (°C)')
    ax.legend()
    ax.grid(True, alpha=0.3)

    # Humidity
    ax = axes[2]
    ax.fill_between(dates,
                    [float(r['Humidity Low (%)']) for r in rows],
                    [float(r['Humidity High (%)']) for r in rows],
                    alpha=0.3, color='tab:blue')
    ax.plot(dates, [float(r['Humidity Avg (%)']) for r in rows],
            color='tab:blue', label='Avg')
    ax.set_ylabel('Humidity (%)')
    ax.legend()
    ax.grid(True, alpha=0.3)

    # Wind Speed
    ax = axes[3]
    ax.plot(dates, [float(r['Wind Speed High (km/h)']) for r in rows],
            color='tab:green', alpha=0.6, label='High')
    ax.plot(dates, [float(r['Wind Speed Avg (km/h)']) for r in rows],
            color='tab:green', label='Avg')
    ax.set_ylabel('Wind Speed (km/h)')
    ax.legend()
    ax.grid(True, alpha=0.3)

    # Pressure
    ax = axes[4]
    ax.fill_between(dates,
                    [float(r['Pressure Min (mb)']) for r in rows],
                    [float(r['Pressure Max (mb)']) for r in rows],
                    alpha=0.3, color='tab:orange')
    ax.plot(dates,
            [(float(r['Pressure Max (mb)']) + float(r['Pressure Min (mb)'])) / 2
             for r in rows],
            color='tab:orange', label='Mid')
    ax.set_ylabel('Pressure (mb)')
    ax.legend()
    ax.grid(True, alpha=0.3)

    # Precipitation
    ax = axes[5]
    ax.bar(dates, [float(r['Precipitation (mm)']) for r in rows],
           color='tab:cyan', width=0.8)
    ax.set_ylabel('Precipitation (mm)')
    ax.grid(True, alpha=0.3)

    axes[5].xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    axes[5].xaxis.set_major_locator(mdates.WeekdayLocator())
    fig.autofmt_xdate(rotation=45)

    fig.suptitle('Weather Data', fontsize=14)
    fig.tight_layout()
    fig.savefig(output_file, dpi=150)
    print(f"Plot saved to {output_file}")


def main():
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <csv_file> [output.png]", file=sys.stderr)
        sys.exit(1)

    csv_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else csv_file.rsplit('.', 1)[0] + '.png'

    rows = read_csv(csv_file)
    plot_weather(rows, output_file)


if __name__ == "__main__":
    main()
