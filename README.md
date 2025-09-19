Air Quality Index (AQI) Forecasting and Visualization
This project simulates a synthetic air quality dataset over two years with daily pollutant measurements and computes the Air Quality Index (AQI). It supports querying historical pollutant data by date, generating a 14-day AQI forecast using Holt-Winters Exponential Smoothing, providing health alerts, and visualizing both historical and recent air quality trends.

Features
Synthetic dataset generation for daily PM2.5, NO2, and CO concentrations over 2 years.

AQI calculation combining pollutant levels with clipping to realistic bounds.

Health alert messaging based on AQI value categories.

User input for date-specific pollutant data querying and subsequent AQI forecasting.

Time series forecasting with trend and optional seasonality (daily and yearly).

Visualizations for AQI trends and individual pollutant concentrations starting from the user input date.

Requirements
Python 3.x

pandas

numpy

matplotlib

seaborn

statsmodels

Install dependencies with:

bash
pip install pandas numpy matplotlib seaborn statsmodels
Usage
Run the script
The script will generate a synthetic air quality dataset saved as synthetic_air_quality_data.csv.

Enter a date (format YYYY-MM-DD) when prompted to:

View pollutant concentrations and AQI for that specific day.

Receive a health alert based on AQI.

Generate and report a 14-day AQI forecast starting from the given date.

Display visualizations showing AQI and pollutant trends from the entered date forward.

Interpret output:

Numerical pollutant data and AQI for the input date.

Health risk alerts aligned with AQI values.

Forecasted AQI values with corresponding health alerts for 14 days.

Time series plots focusing on the selected period and onward.

Files
synthetic_air_quality_data.csv: Generated synthetic pollutant and AQI dataset.

Script file: Generates data, accepts user input, forecasts AQI, and produces visualizations.

Notes
The forecasting model automatically adjusts seasonal period parameters depending on available data length.

AQI and health alerts follow standard air quality classification.

Visual outputs require an environment capable of displaying plots.

This project uses synthetic data intended for educational and demonstration purposes only.

