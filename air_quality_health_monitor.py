import argparse
import pandas as pd
import numpy as np
from statsmodels.tsa.holtwinters import ExponentialSmoothing
import google.generativeai as genai

# -----------------------
# 1. Configure Gemini API
# -----------------------
genai.configure(api_key="AIzaSyC2EVCSgC-DRWVunkKi7Ro0J1upoN3UglE")  # Replace with your API key
model = genai.GenerativeModel("gemini-1.5-flash")

# -----------------------
# 2. Helper: Health Risk Detection
# -----------------------
def health_risk(aqi):
    if aqi > 300:
        return "☠️ Hazardous – Stay indoors, use air purifiers & masks!"
    elif aqi > 200:
        return "⚠️ Very Unhealthy – Avoid outdoor activities."
    elif aqi > 150:
        return "🟠 Unhealthy – Sensitive groups at risk."
    elif aqi > 100:
        return "🟡 Moderate – Acceptable but caution for sensitive groups."
    else:
        return "🟢 Good – Air quality is safe."

# -----------------------
# 3. Forecast & AI Function
# -----------------------
def forecast(aqi_history):
    try:
        if len(aqi_history) < 5:
            print("❌ Error: Need at least 5 AQI data points for forecasting.")
            return

        # Holt-Winters forecasting
        series = pd.Series(aqi_history)
        model_hw = ExponentialSmoothing(series, trend="add", seasonal=None)
        model_fit = model_hw.fit()
        forecast_values = model_fit.forecast(steps=3).tolist()

        # Detect trend
        trend = "increasing 📈 (worsening)" if np.mean(aqi_history[-3:]) > np.mean(aqi_history[:3]) else "decreasing 📉 (improving)"

        # Health risk
        risk_message = health_risk(forecast_values[0])

        # AI Recommendation
        prompt = f"""
        You are an AI health & environment analyst.
        Given AQI history: {aqi_history}
        Forecasted next 3 AQI values: {forecast_values}
        Trend: {trend}
        Health Risk: {risk_message}

        Provide:
        1. Health & safety recommendations.
        2. Steps to reduce pollution exposure.
        """
        response = model.generate_content(prompt)
        ai_text = response.text if response else "❌ No AI response"

        # Split AI output
        parts = ai_text.split("\n", 1)
        ai_recommendation = parts[0].strip() if parts else "Not generated"
        ai_explanation = parts[1].strip() if len(parts) > 1 else ai_text

        # Print results
        print("\n🌍 Air Quality Forecast & Health Insights")
        print("-" * 50)
        print(f"Next 3 AQI Predictions: {', '.join([str(round(x,2)) for x in forecast_values])}")
        print(f"Trend                : {trend}")
        print(f"Health Risk          : {risk_message}")
        print("\n🤖 AI Recommendation:")
        print(ai_recommendation)
        print("\nAI Explanation:")
        print(ai_explanation)

    except Exception as e:
        print(f"❌ Error: {e}")

# -----------------------
# 4. CLI Setup
# -----------------------
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="🌍 Air Quality Health Monitor (Terminal Version)")
    parser.add_argument("--aqi", type=str, help="Comma-separated AQI history (at least 5 values)")

    args = parser.parse_args()

    # Interactive input if not provided
    if args.aqi:
        aqi_input = args.aqi
    else:
        aqi_input = input("Enter AQI History (comma-separated, at least 5 values): ")

    aqi_history = [float(x.strip()) for x in aqi_input.split(",") if x.strip()]
    forecast(aqi_history)
