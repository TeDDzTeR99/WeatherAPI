import json
import requests
import pandas as pd

# 1. Define the live API endpoint with coordinates
url = "https://api.met.no/weatherapi/locationforecast/2.0/compact"

# 2. Move coordinates into a clean parameters dictionary
params = {
    "lat": 60.10,
    "lon": 24.75
}

# 3. Add Accept (file type) and User-Agent identifiers to your headers
headers = {
    "User-Agent": "WeatherAnalyticsDataApp/2.0 (research_analytics@domain.com)",
    "Accept": "application/geo+json"  # Tells the server you expect JSON back
}

try:
    # 3. Make the API request
    print("Fetching live data from Met.no API...")
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status() 
    #print(response.headers)
    #print(response.json())
    #with open("data.json", "w", encoding="utf-8") as file:
    # Option A: Save the raw Python dictionary/list directly
        #json.dump(response.json(), file, indent=4)
    
    # 4. Load the API text response directly into a JSON dictionary
    raw_payload = response.json()
    timeseries = raw_payload["properties"]["timeseries"]

    # 5. Extract and flatten the weather records safely
    flattened_records = []
    for entry in timeseries:
        details = entry.get("data", {}).get("instant", {}).get("details", {})
        record = {
            "Timestamp": entry.get("time"),
            "Temperature (°C)": details.get("air_temperature"),
            "Humidity (%)": details.get("relative_humidity"),
            "Wind Speed (m/s)": details.get("wind_speed"),
            "Pressure (hPa)": details.get("air_pressure_at_sea_level")
        }
        flattened_records.append(record)

    # 6. Convert into a structured table frame
    df = pd.DataFrame(flattened_records)
    
    # 7. Format the raw UTC timestamps into an easily readable format
    # Convert string to datetime object
    df["Timestamp"] = pd.to_datetime(df["Timestamp"])
    
    # Optional: Convert from UTC to your system's local timezone
    df["Timestamp"] = df["Timestamp"].dt.tz_convert(None) # Removes 'Z' and leaves a clean local runtime index
    
    # Format into a clean, standard layout: YYYY-MM-DD HH:MM
    df["Timestamp"] = df["Timestamp"].dt.strftime("%Y-%m-%d %H:%M")
    
    # View the top records
    print("\nSuccessfully processed data frame:")
    print(df.head())

except requests.exceptions.HTTPError as http_err:
    print(f"HTTP error occurred: {http_err}")
except Exception as err:
    print(f"An unexpected error occurred: {err}")
