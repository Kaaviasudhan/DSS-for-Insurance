# policyrec_routes.py
from flask import Blueprint, render_template, request, session, redirect, url_for
import pandas as pd
import pickle
import numpy as np
import os

policy_recommend_bp = Blueprint('policy_recommend', __name__)

# Load the model and label encoders
model_path = os.path.join('app', 'models', 'policyrecommend_mod', 'Recommend_model.pkl')
le_path = os.path.join('app', 'models', 'policyrecommend_mod', 'Recommend_label_encoders.pkl')
df_path = os.path.join('app', 'data', 'Policy-recommend.csv')

with open(model_path, 'rb') as model_file:
    policy_model = pickle.load(model_file)

with open(le_path, 'rb') as le_file:
    policy_label_encoders = pickle.load(le_file)

# Load dataset
df = pd.read_csv(df_path)

# Extract unique values for dropdowns
unique_values = {}
for column in ['Occupation', 'Education', 'Marital Status', 'Gender', 'Region']:
    unique_values[column] = df[column].unique()

@policy_recommend_bp.route('/policypred', methods=['GET', 'POST'])
def policypredt():
    user_role = session.get('role')
    if not user_role:
        return redirect(url_for('login'))

    if request.method == 'POST':
        # Extract data from the form
        data = {
            'Customer Age': [int(request.form['customer_age'])],
            'Occupation': [request.form['occupation']],
            'Income': [int(request.form['income'])],
            'Education': [request.form['education']],
            'Marital Status': [request.form['marital_status']],
            'Tenure (Years)': [int(request.form['tenure'])],
            'Premium (INR)': [int(request.form['premium'])],
            'Coverage (INR)': [int(request.form['coverage'])],
            'Family Size': [int(request.form['family_size'])],
            'Gender': [request.form['gender']],
            'Region': [request.form['region']]
        }

        # Create DataFrame
        sample_data = pd.DataFrame(data)

        # Apply label encoding to categorical columns
        for column in ['Occupation', 'Education', 'Marital Status', 'Gender', 'Region']:
            sample_data[column] = policy_label_encoders[column].transform(sample_data[column])

        # Predict the policy type
        predicted_policy_type = policy_model.predict(sample_data)
        predicted_policy_type = policy_label_encoders['Policy Type'].inverse_transform(predicted_policy_type)

        return render_template('policyrecommend-mod/index.html', unique_values=unique_values, prediction=predicted_policy_type[0], role=user_role)

    return render_template('policyrecommend-mod/index.html', unique_values=unique_values, role=user_role)