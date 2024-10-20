# app/saleforecast_route.py
import os
import pickle
import pandas as pd
import numpy as np
from flask import Blueprint, render_template, request, redirect, url_for, session

saleforecast_bp = Blueprint('saleforecast', __name__)

# Load the ARIMA model
model_path = os.path.join('app', 'models', 'sales_mod', 'arima_model.pkl')
with open(model_path, 'rb') as file:
    model_fit = pickle.load(file)

# Load and preprocess the dataset
data_path = os.path.join('app', 'data', 'insurance_dataset_full_2010_to_2024.csv')
data = pd.read_csv(data_path)
data['Date'] = pd.to_datetime(data[['Year', 'Month']].assign(DAY=1))
data.set_index('Date', inplace=True)
data = data[data.index >= '2000-01-01']

def predict_sales(policy_type, duration_years, min_threshold=0.5, moving_avg_window=5):
    filtered_data = data[data['Policy_Type'] == policy_type]['Sales'].resample('M').sum()
    forecast_periods = duration_years * 12
    forecast = model_fit.predict(n_periods=forecast_periods)

    historical_std = filtered_data.std()
    random_variation = np.random.normal(0, historical_std, size=forecast_periods)
    forecast += random_variation

    alpha = 0.9
    forecast_smooth = np.array([forecast[0]])
    for i in range(1, len(forecast)):
        forecast_smooth = np.append(forecast_smooth, alpha * forecast[i] + (1 - alpha) * forecast_smooth[-1])

    forecast_min = forecast_smooth.min()
    if forecast_min < min_threshold:
        adjustment_factor = min_threshold - forecast_min
        forecast_smooth += adjustment_factor

    forecast_series = pd.Series(forecast_smooth, index=pd.date_range(start=filtered_data.index[-1], periods=forecast_periods + 1, freq='M')[1:])
    moving_avg = forecast_series.rolling(window=moving_avg_window).mean()

    return forecast_series, moving_avg

def generate_interpretation(forecast_series, moving_avg):
    interpretation = []
    if forecast_series.mean() > moving_avg.mean():
        interpretation.append("The forecasted sales show an upward trend compared to the moving average, indicating potential growth in demand.")
    else:
        interpretation.append("The forecasted sales are relatively flat compared to the moving average, suggesting stable demand.")

    if forecast_series.max() > forecast_series.mean() * 1.5:
        interpretation.append("The forecast displays significant seasonal peaks, which may indicate high demand periods for targeted marketing.")
    else:
        interpretation.append("There are no pronounced seasonal peaks, suggesting consistent demand throughout the year.")

    if forecast_series.std() > moving_avg.std() * 1.5:
        interpretation.append("The forecast data shows high volatility, indicating possible uncertainty in future sales.")
    else:
        interpretation.append("The forecast data shows lower volatility, suggesting more predictable future sales.")

    return " ".join(interpretation)

@saleforecast_bp.route('/salesforecast', methods=['GET', 'POST'])
def salesforecast():

    # Get the role from the session
    user_role = session.get('role')
    if not user_role:
        return redirect(url_for('login'))  # Redirect to login if no role is found

    if request.method == 'POST':
        policy_type = request.form['policy_type']
        duration_years = int(request.form['duration_years'])

        forecast_series, moving_avg = predict_sales(policy_type, duration_years)

        forecast_data = {
            'dates': forecast_series.index.strftime('%Y-%m').tolist(),
            'values': forecast_series.tolist(),
            'moving_avg_dates': moving_avg.index.strftime('%Y-%m').tolist(),
            'moving_avg_values': moving_avg.tolist()
        }
        
        interpretation = generate_interpretation(forecast_series, moving_avg)

        return render_template('sales-mod/result.html', forecast_data=forecast_data, policy_type=policy_type, duration_years=duration_years, interpretation=interpretation, role=user_role)

    return render_template('sales-mod/index.html', role=user_role)
