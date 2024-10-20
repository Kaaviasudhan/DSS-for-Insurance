from flask import Blueprint, render_template, request, redirect, url_for, session
import pickle
import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns

# Define the fraud blueprint
fraud_bp = Blueprint('fraud', __name__, url_prefix='/fraud')

# Load the saved RandomForest model and encoders
fraud_model_path = 'app/models/fraud_mod/RandomForest_model.pkl'
fraud_encoder_path = 'app/models/fraud_mod/label_encoders.pkl'

with open(fraud_model_path, 'rb') as f:
    fraud_rf_model = pickle.load(f)

with open(fraud_encoder_path, 'rb') as f:
    fraud_label_encoders = pickle.load(f)

# Fraud Prediction Route
@fraud_bp.route('/fraudpred', methods=['GET', 'POST'])
def fraudpredt():

    # Get the role from the session
    user_role = session.get('role')
    if not user_role:
        return redirect(url_for('login'))  # Redirect to login if no role is found

    if request.method == 'POST':
        # Retrieve form data
        policy_type = int(request.form['policy_type'])
        annual_premium = float(request.form['annual_premium'])
        claims_made = int(request.form['claims_made'])
        total_claim_amount = float(request.form['total_claim_amount'])
        last_claim_amount = float(request.form['last_claim_amount'])
        risk_score = float(request.form['risk_score'])

        # Prepare the sample data
        sample_data = {
            'Policy_Type': policy_type,
            'Annual_Premium': annual_premium,
            'Claims_Made': claims_made,
            'Total_Claim_Amount': total_claim_amount,
            'Last_Claim_Amount': last_claim_amount,
            'Risk_Score': risk_score
        }
        sample_df = pd.DataFrame([sample_data])

        # Predict using the loaded model
        predicted = fraud_rf_model.predict(sample_df)
        predicted_proba = fraud_rf_model.predict_proba(sample_df)

        # Map the prediction back to the original label names
        fraud_mapping = {0: 'Non-Fraud', 1: 'Fraud'}
        predicted_label = fraud_mapping[predicted[0]]

        # Save the plot as an image
        plt.figure(figsize=(8, 5))
        sns.barplot(x=['Non-Fraud', 'Fraud'], y=predicted_proba[0])
        plt.title('Prediction Probability for Sample Data')
        plt.ylabel('Probability')
        plot_path = os.path.join('app', 'static', 'result_img', 'fraud_prediction_plot.png')  # Change to the correct path
        plt.savefig(plot_path)
        plt.close()

        return render_template('fraud-mod/index.html', predicted_label=predicted_label, plot_path=plot_path, role=user_role)

    return render_template('fraud-mod/index.html', predicted_label=None, role=user_role)
