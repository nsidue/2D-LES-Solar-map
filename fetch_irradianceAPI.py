import openmeteo_requests

import pandas as pd
import requests_cache
from retry_requests import retry

# Setup the Open-Meteo API client with cache and retry on error
cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
openmeteo = openmeteo_requests.Client(session = retry_session)

# Make sure all required weather variables are listed here
# The order of variables in hourly or daily is important to assign them correctly below
url = "https://api.open-meteo.com/v1/forecast"
params = {
	"latitude": 52.52,
	"longitude": 13.41,
	"hourly": ["temperature_2m", "direct_normal_irradiance", "direct_normal_irradiance_instant"],
	"models": "best_match",
	"minutely_15": ["direct_normal_irradiance", "direct_normal_irradiance_instant", "temperature_2m"],
	"past_days": 14,
	"forecast_days": 14,
	"temperature_unit": "fahrenheit",
}
responses = openmeteo.weather_api(url, params = params)

# Process first location. Add a for-loop for multiple locations or weather models
response = responses[0]
print(f"Coordinates: {response.Latitude()}°N {response.Longitude()}°E")
print(f"Elevation: {response.Elevation()} m asl")
print(f"Timezone difference to GMT+0: {response.UtcOffsetSeconds()}s")

# Process minutely_15 data. The order of variables needs to be the same as requested.
minutely_15 = response.Minutely15()
minutely_15_direct_normal_irradiance = minutely_15.Variables(0).ValuesAsNumpy()
minutely_15_direct_normal_irradiance_instant = minutely_15.Variables(1).ValuesAsNumpy()
minutely_15_temperature_2m = minutely_15.Variables(2).ValuesAsNumpy()

minutely_15_data = {
	"date": pd.date_range(
		start = pd.to_datetime(minutely_15.Time(), unit = "s", utc = True),
		end =  pd.to_datetime(minutely_15.TimeEnd(), unit = "s", utc = True),
		freq = pd.Timedelta(seconds = minutely_15.Interval()),
		inclusive = "left"
	)
}

minutely_15_data["direct_normal_irradiance"] = minutely_15_direct_normal_irradiance
minutely_15_data["direct_normal_irradiance_instant"] = minutely_15_direct_normal_irradiance_instant
minutely_15_data["temperature_2m"] = minutely_15_temperature_2m

minutely_15_dataframe = pd.DataFrame(data = minutely_15_data)
print("\nMinutely15 data\n", minutely_15_dataframe)

# Process hourly data. The order of variables needs to be the same as requested.
hourly = response.Hourly()
hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()
hourly_direct_normal_irradiance = hourly.Variables(1).ValuesAsNumpy()
hourly_direct_normal_irradiance_instant = hourly.Variables(2).ValuesAsNumpy()

hourly_data = {
	"date": pd.date_range(
		start = pd.to_datetime(hourly.Time(), unit = "s", utc = True),
		end =  pd.to_datetime(hourly.TimeEnd(), unit = "s", utc = True),
		freq = pd.Timedelta(seconds = hourly.Interval()),
		inclusive = "left"
	)
}

hourly_data["temperature_2m"] = hourly_temperature_2m
hourly_data["direct_normal_irradiance"] = hourly_direct_normal_irradiance
hourly_data["direct_normal_irradiance_instant"] = hourly_direct_normal_irradiance_instant

hourly_dataframe = pd.DataFrame(data = hourly_data)
print("\nHourly data\n", hourly_dataframe)
