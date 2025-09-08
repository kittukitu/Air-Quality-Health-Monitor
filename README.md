🌍 Air Quality Health Monitor

An AI-powered air quality forecasting & health monitoring system that predicts AQI trends using Holt-Winters Exponential Smoothing and provides AI-driven health & safety recommendations.

🚀 Features

Forecasts next 3 AQI values from historical data.

Detects trend (improving 📉 or worsening 📈).

Classifies health risk level based on AQI.

Provides health & safety recommendations using Gemini AI.

Supports command-line arguments and interactive input.

⚙️ Installation
1. Clone Repository
git clone https://github.com/yourusername/air-quality-monitor.git
cd air-quality-monitor

2. Create Virtual Environment (recommended)
python -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate      # Windows

3. Install Dependencies
pip install -r requirements.txt


requirements.txt

pandas
numpy
statsmodels
google-generativeai
argparse

🔑 Setup Gemini API

Get an API Key from Google AI Studio
.

Replace your key in the script:

genai.configure(api_key="YOUR_API_KEY")

🖥️ Usage
Run with CLI arguments
python app.py --aqi 90,110,130,150,170,200,220

Run in interactive mode
python app.py


Example Input/Output:

Enter AQI History (comma-separated, at least 5 values): 90,110,130,150,170,200,220

🌍 Air Quality Forecast & Health Insights
--------------------------------------------------
Next 3 AQI Predictions: 230.45, 240.67, 250.89
Trend                : increasing 📈 (worsening)
Health Risk          : ⚠️ Very Unhealthy – Avoid outdoor activities.

🤖 AI Recommendation:
Limit outdoor exposure and use N95 masks.

AI Explanation:
The forecast indicates a worsening air trend with unhealthy AQI levels. Restricting outdoor activity reduces exposure risk and protects vulnerable groups.

✅ Test Cases
Test Case 1: Good Air Quality
python app.py --aqi 30,40,35,45,50,55,60


Expected:

Forecast remains low AQI (<100).

Trend: Either stable or slight increase.

Health Risk: 🟢 Good.

AI suggests normal outdoor activities.

Test Case 2: Unhealthy Trend
python app.py --aqi 120,140,160,170,190,200,220


Expected:

Forecast shows rising AQI values.

Trend: increasing 📈 (worsening).

Health Risk: 🟠 Unhealthy.

AI suggests limiting outdoor exposure.

Test Case 3: Hazardous Air
python app.py --aqi 280,300,320,340,360,380,400


Expected:

Forecast predicts very high AQI.

Trend: increasing 📈 (worsening).

Health Risk: ☠️ Hazardous.

AI suggests staying indoors & using air purifiers.

📊 Methodology

Forecasting Model → Holt-Winters Exponential Smoothing (trend="add").

Trend Detection → Compares last 3 values vs first 3.

Health Risk Classification:

🟢 Good: AQI ≤ 100

🟡 Moderate: 101–150

🟠 Unhealthy: 151–200

⚠️ Very Unhealthy: 201–300

☠️ Hazardous: > 300

AI Layer → Gemini generates health & pollution reduction advice.

📌 Roadmap

 Add real AQI API integration (e.g., OpenWeather, AQICN).

 Build Flask dashboard with charts.

 Extend to regional pollution forecasting.