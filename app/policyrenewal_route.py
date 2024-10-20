import os
import pickle
import pandas as pd
import matplotlib.pyplot as plt
from flask import Blueprint, render_template, redirect, url_for, request, session

policyrenewal_bp = Blueprint('policyrenewal', __name__)

# Load models and label encoders
model_path = os.path.join('app', 'models', 'renewal_mod')

with open(os.path.join(model_path, 'RandomForest_model.pkl'), 'rb') as f:
    rf_model = pickle.load(f)

with open(os.path.join(model_path, 'LogisticRegression_model.pkl'), 'rb') as f:
    lr_model = pickle.load(f)

with open(os.path.join(model_path, 'SVC_model.pkl'), 'rb') as f:
    svc_model = pickle.load(f)

with open(os.path.join(model_path, 'label_encoders.pkl'), 'rb') as f:
    label_encoders = pickle.load(f)

def preprocess_input(data):
    if 'Policy_Start_Date' in data.columns:
        data['Policy_Start_Year'] = pd.to_datetime(data['Policy_Start_Date']).dt.year
        data['Policy_Start_Year'] = data['Policy_Start_Year'].astype(int)
        data.drop(columns=['Policy_Start_Date'], errors='ignore', inplace=True)
    
    for column, le in label_encoders.items():
        if column in data.columns:
            data[column] = le.transform(data[column])
    
    return data

def plot_renewal_chart(X_test_with_predictions, data):
    X_test_with_predictions['Policy_Type'] = data.loc[X_test_with_predictions.index, 'Policy_Type']

    policy_type_renewals = X_test_with_predictions.groupby('Policy_Type').agg(
        Total_Count=('Actual', 'size'),
        Renewed_Count=('Actual', 'sum'),
        Predicted_Renewed_Count=('Predicted', 'sum')
    ).reset_index()

    policy_type_renewals['Renewal_Rate'] = policy_type_renewals['Renewed_Count'] / policy_type_renewals['Total_Count'] * 100

    plt.figure(figsize=(10, 6))
    plt.bar(policy_type_renewals['Policy_Type'].astype(str), policy_type_renewals['Renewal_Rate'], color='skyblue')
    plt.xlabel('Policy Type')
    plt.ylabel('Renewal Rate (%)')
    plt.title('Policy Type-wise Renewal Rates')
    plt.xticks(rotation=45)
    plt.tight_layout()

    chart_path = os.path.join('app', 'static', 'result_img', 'renewal_chart.png')
    plt.savefig(chart_path)
    plt.close()

    return chart_path

@policyrenewal_bp.route('/policyrenewal', methods=['GET', 'POST'])
def renewal():

    # Get the role from the session
    user_role = session.get('role')
    if not user_role:
        return redirect(url_for('login'))  # Redirect to login if no role is found

    if request.method == 'POST':
        input_data = {
            'Policy_Name': [request.form['Policy_Name']],
            'Policy_Type': [request.form['Policy_Type']],
            'Gender': [request.form['Gender']],
            'Region': [request.form['Region']],
            'Occupation': [request.form['Occupation']],
            'Marital_Status': [request.form['Marital_Status']],
            'Policy_Start_Date': [request.form['Policy_Start_Date']]
        }
        
        df = pd.DataFrame(input_data)
        df = preprocess_input(df)

        rf_prediction = rf_model.predict(df)[0]
        lr_prediction = lr_model.predict(df)[0]
        svc_prediction = svc_model.predict(df)[0]

        X_test_with_predictions = df.copy()
        X_test_with_predictions['Actual'] = [1]  # Example: Assume actual renewal
        X_test_with_predictions['Predicted'] = [rf_prediction]

        chart_path = plot_renewal_chart(X_test_with_predictions, df)

        return render_template('policyrenewal-mod/result.html', 
                               rf_prediction='Yes' if rf_prediction == 1 else 'No',
                               lr_prediction='Yes' if lr_prediction == 1 else 'No',
                               svc_prediction='Yes' if svc_prediction == 1 else 'No',
                               chart_path=chart_path, role=user_role)
    
    return render_template('policyrenewal-mod/index.html', role=user_role)
