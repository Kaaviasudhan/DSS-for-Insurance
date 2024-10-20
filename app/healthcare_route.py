import os
import pickle
import numpy as np
from flask import Blueprint, render_template, request, redirect, url_for, session

# Create a blueprint for healthcare predictions
health_bp = Blueprint('health', __name__)

# Load the trained model
model_path = os.path.join(os.path.dirname(__file__), 'models', 'healthcare_mod','rf_tuned.pkl')
with open(model_path, 'rb') as file:
    modelrf = pickle.load(file)

# Route for Annual Premium Predictions
@health_bp.route('/healthpred', methods=['GET', 'POST'])
def healthpredcost():

    # Get the role from the session
    user_role = session.get('role')
    if not user_role:
        return redirect(url_for('main.login'))  # Redirect to login if no role is found

    prediction = None
    if request.method == 'POST':
        # Get input values from the form
        age = float(request.form['age'])
        gender = int(request.form['Gender'])
        bmi = float(request.form['bmi'])
        children = int(request.form['children'])
        smoker = int(request.form['smoker'])
        region = int(request.form['region'])
        
        # Prepare the input for the model
        input_features = np.array([[age, gender, bmi, children, smoker, region]])
        
        # Predict
        prediction = modelrf.predict(input_features)[0]
        
    return render_template('healthcare-mod/index.html', pred=prediction, role=user_role)
