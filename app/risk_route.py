import pickle
import pandas as pd
from flask import Blueprint, render_template, redirect, url_for, session, request

# Create a Blueprint
risk_bp = Blueprint('risk', __name__)

# Load the trained model
with open('app/models/risk_mod/linear_regression_model.pkl', 'rb') as file:
    risk_model = pickle.load(file)

# Define the route for risk prediction
@risk_bp.route('/riskpred', methods=['GET', 'POST'])
def riskpredt():

    # Get the role from the session
    user_role = session.get('role')
    if not user_role:
        return redirect(url_for('login'))  # Redirect to login if no role is found

    if request.method == 'POST':
        # Get input data from the form
        customer_age = int(request.form['Customer_Age'])
        annual_premium = float(request.form['Annual_Premium'])
        is_high_value_customer = int(request.form['Is_High_Value_Customer'])

        # Create DataFrame for model input
        input_data = pd.DataFrame({
            'Customer_Age': [customer_age],
            'Annual_Premium': [annual_premium],
            'Is_High_Value_Customer': [is_high_value_customer]
        })

        # Make prediction
        prediction = risk_model.predict(input_data)[0]

        # Render template with prediction
        return render_template('risk-mod/index.html', prediction=prediction, role=user_role)

    return render_template('risk-mod/index.html', prediction=None, role=user_role)
