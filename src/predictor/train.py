import numpy as np
from datetime import datetime, timedelta
from sklearn.linear_model import LinearRegression
from src.scraper.web_scraper import fetch_hardware_history
from src.predictor.data_loader import prepare_training_data


def predict_hardware_price(raw_scraped_data: list) -> dict:
    X, y, df_metadata = prepare_training_data(raw_scraped_data)

    if X is None:
        return None

    model = LinearRegression()
    model.fit(X, y)

    last_day_index = int(X.max())
    current_price = float(df_metadata['price'].iloc[-1])
    latest_date = df_metadata['Date_Parsed'].max()

    future_features = []
    future_dates = []

    for i in range(1, 8):
        future_features.append([last_day_index + i])
        future_calendar_date = latest_date + timedelta(days=i)
        future_dates.append(future_calendar_date.strftime("%Y-%m-%d"))

    linear_predictions = model.predict(future_features)

    np.random.seed(42)
    noise = np.random.normal(0, 1.5, 7)
    final_predictions = linear_predictions + noise

    forecast_schedule = {}
    for date, pred_price in zip(future_dates, final_predictions):
        forecast_schedule[date] = round(float(pred_price), 2)

    predicted_7_days_out = round(float(final_predictions[-1]), 2)

    return {
        "status": "success",
        "product_id": df_metadata['product_id'].iloc[-1],
        "current_price": current_price,
        "predicted_price_next_week": predicted_7_days_out,
        "price_difference": round(predicted_7_days_out - current_price, 2),
        "7_day_forecast": forecast_schedule
    }


def get_hardware_forecast(product_url: str) -> dict:
    print(f"\n[PREDICTOR] Incoming asset evaluation request...")

    scraped_data = fetch_hardware_history(product_url)
    if scraped_data is None:
        print("[PREDICTOR] Pipeline Aborted: Invalid URL provided.")
        return {"status": "invalid_link"}
    results = predict_hardware_price(scraped_data)
    print(f"[PREDICTOR] ML Complete for '{results['product_id']}'.")
    return results
