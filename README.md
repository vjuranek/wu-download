# Weather Underground Data Scraper

A simple Python application to download weather data from Weather Underground PWS (Personal Weather Station) API and save it to CSV format.

## Features

- Downloads complete daily weather data directly from Weather Underground API
- Simple HTTP requests - no browser automation needed
- Clean numeric data without HTML parsing
- Saves all data to timestamped CSV files
- Includes data for: Temperature, Dew Point, Humidity, Wind Speed, Pressure, and Precipitation

## Requirements

- Python 3.7+
- `requests` library

## Installation

Install the required dependency:

```bash
pip install -r requirements.txt
```

Or simply:

```bash
pip install requests
```

## Usage

Run the scraper:

```bash
python3 weather_scraper.py
```

The script will:
1. Fetch data directly from the Weather Underground API
2. Parse the JSON response
3. Extract all 30 days of daily weather data for April 2026
4. Save the data to a CSV file named `weather_data_april_2026_<timestamp>.csv`

Takes only a few seconds to complete!

## Output

The CSV file contains:
- **Header row** with clear column names
- **30 data rows** - one for each day of April 2026
- All measurements as clean numeric values

Example output:
```
Date,Temp High (°F),Temp Avg (°F),Temp Low (°F),Dew Point High (°F),...
2026-04-01,56.3,43.0,33.6,35.4,...
2026-04-02,55.4,42.9,35.4,37.7,...
...
2026-04-30,64.0,44.1,26.2,28.0,...
```

Columns include:
- Date
- Temperature (High, Average, Low)
- Dew Point (High, Average, Low)
- Humidity (High, Average, Low)
- Wind Speed (High, Average, Low)
- Pressure (Max, Min)
- Precipitation (Total)

## Customization

To scrape data from a different station or date range, modify the variables in the `main()` function of `weather_scraper.py`:

```python
station_id = "IDALEI13"      # Change to your station ID
start_date = "20260401"      # YYYYMMDD format
end_date = "20260430"        # YYYYMMDD format
```

## How It Works

Instead of scraping HTML, this app uses the official Weather Underground API endpoint that the website itself uses. This is much faster, simpler, and more reliable than browser automation.
