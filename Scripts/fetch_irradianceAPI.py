import openmeteo_requests

import pandas as pd
import requests_cache
from retry_requests import retry


# Setup the Open-Meteo API client with cache and retry on error
cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
openmeteo = openmeteo_requests.Client(session = retry_session)

def get_weather():
    # Make sure all required weather variables are listed here
    # The order of variables in hourly or daily is important to assign them correctly below
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
    	"latitude": 40.7159,
    	"longitude": -73.9868,
    	"hourly": ["direct_normal_irradiance_instant", "direct_normal_irradiance"],
    	"minutely_15": ["direct_normal_irradiance_instant", "direct_normal_irradiance"],
    	"timezone": "America/New_York",
    	"past_days": 14,
    	"forecast_days": 14,
    	"wind_speed_unit": "ms",
    	"temperature_unit": "fahrenheit",
    	"precipitation_unit": "inch",
    }
    responses = openmeteo.weather_api(url, params = params)
    
    # Process first location. Add a for-loop for multiple locations or weather models
    response = responses[0]
    #print(f"Coordinates: {response.Latitude()}°N {response.Longitude()}°E")
    #print(f"Elevation: {response.Elevation()} m asl")
    #print(f"Timezone: {response.Timezone()}{response.TimezoneAbbreviation()}")
    #print(f"Timezone difference to GMT+0: {response.UtcOffsetSeconds()}s")
    
    # Process minutely_15 data. The order of variables needs to be the same as requested.
    minutely_15 = response.Minutely15()
    minutely_15_direct_normal_irradiance_instant = minutely_15.Variables(0).ValuesAsNumpy()
    minutely_15_direct_normal_irradiance = minutely_15.Variables(1).ValuesAsNumpy()
    
    minutely_15_data = {
    	"date": pd.date_range(
    		start = pd.to_datetime(minutely_15.Time(), unit = "s", utc = True),
    		end =  pd.to_datetime(minutely_15.TimeEnd(), unit = "s", utc = True),
    		freq = pd.Timedelta(seconds = minutely_15.Interval()),
    		inclusive = "left"
    	).tz_convert(response.Timezone().decode())
    }
    
    minutely_15_data["direct_normal_irradiance_instant"] = minutely_15_direct_normal_irradiance_instant
    minutely_15_data["direct_normal_irradiance"] = minutely_15_direct_normal_irradiance
    
    minutely_15_dataframe = pd.DataFrame(data = minutely_15_data)
    #print("\nMinutely15 data\n", minutely_15_dataframe)
    
    # Process hourly data. The order of variables needs to be the same as requested.
    hourly = response.Hourly()
    print("Hourly start:", pd.to_datetime(hourly.Time(), unit="s", utc=True))
    print("Hourly end:  ", pd.to_datetime(hourly.TimeEnd(), unit="s", utc=True))
    hourly_direct_normal_irradiance_instant = hourly.Variables(0).ValuesAsNumpy()
    hourly_direct_normal_irradiance = hourly.Variables(1).ValuesAsNumpy()
    
    hourly_data = {
    	"date": pd.date_range(
    		start = pd.to_datetime(hourly.Time(), unit = "s", utc = True),
    		end =  pd.to_datetime(hourly.TimeEnd(), unit = "s", utc = True),
    		freq = pd.Timedelta(seconds = hourly.Interval()),
    		inclusive = "left"
    	).tz_convert(response.Timezone().decode())
    }
    
    hourly_data["direct_normal_irradiance_instant"] = hourly_direct_normal_irradiance_instant
    hourly_data["direct_normal_irradiance"] = hourly_direct_normal_irradiance
    
    hourly_dataframe = pd.DataFrame(data = hourly_data)

    # 1. Capture the exact current timestamp in the map's target timezone
    current_time_tz = pd.Timestamp.now(tz="America/New_York")

    # 2. Find the closest match in the hourly dataframe
    hourly_match = hourly_dataframe.iloc[(hourly_dataframe['date'] - current_time_tz).abs().idxmin()]
    
    # 3. Find the closest match in the 15-minute dataframe
    minutely_match = minutely_15_dataframe.iloc[(minutely_15_dataframe['date'] - current_time_tz).abs().idxmin()]

    return {
        "hourly_dataframe": hourly_dataframe,
        "minutely_15_dataframe": minutely_15_dataframe,
        "latitude": response.Latitude(),
        "longitude": response.Longitude(),
        "timezone": response.Timezone().decode(),
        # FIX: Extracts the actual row closest to this exact minute
        "current_hourly_irradiance": hourly_match["direct_normal_irradiance_instant"],
        "current_minutely_irradiance": minutely_match["direct_normal_irradiance_instant"],
    }