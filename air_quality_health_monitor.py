import warnings
warnings.filterwarnings("ignore", category=UserWarning)  # suppress freq warning

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from datetime import timedelta

# --- Step 1: Generate synthetic pollution dataset for 2 years ---
np.random.seed(42)
days = 730  # 2 years

dates = pd.date_range(start="2024-01-01", periods=days, freq='D')

pm25 = 40 + 15 * np.sin(2 * np.pi * dates.dayofyear / 365) + np.random.normal(0, 5, days)
no2 = 30 + 10 * np.cos(2 * np.pi * dates.dayofyear / 365) + np.random.normal(0, 4, days)
co = 0.8 + 0.3 * np.sin(2 * np.pi * dates.dayofyear / 365) + np.random.normal(0, 0.1, days)

aqi = 0.5 * pm25 + 0.3 * no2 + 0.2 * (co * 50)
aqi = np.clip(aqi, 0, 500)

data = pd.DataFrame({
    'date': dates,
    'pm25': pm25,
    'no2': no2,
    'co': co,
    'aqi': aqi
})

data.to_csv("synthetic_air_quality_data.csv", index=False)
print("Synthetic air quality dataset saved as 'synthetic_air_quality_data.csv'.")

# Setup timeseries index and frequency
data.set_index('date', inplace=True)
data.index.freq = 'D'  # explicit frequency to suppress warning

def health_alert(aqi_value):
    if aqi_value <= 50:
        return "Good - Air quality is satisfactory."
    elif aqi_value <= 100:
        return "Moderate - Acceptable air quality."
    elif aqi_value <= 150:
        return "Unhealthy for Sensitive Groups - Take precaution."
    elif aqi_value <= 200:
        return "Unhealthy - Reduce outdoor exertion."
    elif aqi_value <= 300:
        return "Very Unhealthy - Avoid outdoor activities."
    else:
        return "Hazardous - Stay indoors and wear masks."

# --- User input for date query and forecast start ---
date_str = input(f"\nEnter a date (YYYY-MM-DD) to get pollutant data and forecast (e.g. {data.index[-1].strftime('%Y-%m-%d')}): ")

try:
    query_date = pd.to_datetime(date_str)
except Exception:
    print("Invalid date format. Please enter date as YYYY-MM-DD.")
    exit()

if query_date not in data.index:
    print("Date not found in dataset.")
    exit()

row = data.loc[query_date]
print(f"\nDate: {query_date.date()}")
print(f"PM2.5: {row.pm25:.2f}")
print(f"NO2: {row.no2:.2f}")
print(f"CO: {row.co:.2f}")
print(f"AQI: {row.aqi:.2f}")
print(f"Health Alert: {health_alert(row.aqi)}")

ts_sub = data.loc[query_date:]['aqi']
forecast_period = 14

if len(ts_sub) < 10:
    print(f"\nNot enough data available from {query_date.date()} to generate a 14-day forecast. Available days: {len(ts_sub)}.")
else:
    try:
        if len(ts_sub) >= 730:
            seasonal_periods = 365
            seasonal = 'add'
        elif len(ts_sub) >= 30:
            seasonal_periods = 30
            seasonal = 'add'
        else:
            seasonal_periods = None
            seasonal = None

        model_sub = ExponentialSmoothing(ts_sub, trend='add', seasonal=seasonal, seasonal_periods=seasonal_periods)
        fit_sub = model_sub.fit()
        forecast_sub = fit_sub.forecast(forecast_period)
        forecast_dates_sub = pd.date_range(ts_sub.index[-1] + timedelta(days=1), periods=forecast_period)
        alerts_sub = forecast_sub.map(health_alert)

        forecast_df_sub = pd.DataFrame({
            'forecast_date': forecast_dates_sub,
            'predicted_aqi': forecast_sub.values,
            'health_alert': alerts_sub.values
        })
        print("\nAQI Forecast & Health Alerts for Next 14 Days from input date:")
        print(forecast_df_sub)

    except Exception as e:
        print("Error during forecasting:", e)

# --- Updated Visualizations: Only show data from entered date onward ---
data_sub = data.loc[query_date:]

plt.figure(figsize=(14,6))
plt.plot(data_sub.index, data_sub['aqi'].values, label='Historical AQI')
plt.title('Air Quality Index (AQI) Over Time')
plt.xlabel('Date')
plt.ylabel('AQI')
plt.legend()
plt.tight_layout()
plt.show()

plt.figure(figsize=(10,7))
sns.lineplot(data=data_sub.reset_index(), x='date', y='pm25', label='PM2.5')
sns.lineplot(data=data_sub.reset_index(), x='date', y='no2', label='NO2')
sns.lineplot(data=data_sub.reset_index(), x='date', y='co', label='CO')
plt.title('Pollutant Concentrations Over Time')
plt.xlabel('Date')
plt.ylabel('Concentration')
plt.legend()
plt.tight_layout()
plt.show()
