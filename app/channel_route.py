import os
from flask import Blueprint, render_template, request, redirect, url_for, session
import pandas as pd
# import numpy as np
# import pickle
import io
import base64
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

channel_bp = Blueprint('channel', __name__)

# Construct the path to the dataset
dataset_path = os.path.join(os.path.dirname(__file__), 'data', 'updated_marketing_campaign_dataset.csv')
df = pd.read_csv(dataset_path)

possible_target_audiences = df['TargetAudience'].unique().tolist()
possible_policy_types = df['PolicyType'].unique().tolist()

le_target_audience = LabelEncoder()
le_target_audience.fit(possible_target_audiences)
le_policy_type = LabelEncoder()
le_policy_type.fit(possible_policy_types)
le_channel = LabelEncoder()
le_channel.fit(df['Channel'].unique())

# Encode the dataset
df['Channel'] = le_channel.transform(df['Channel'])
df['TargetAudience'] = le_target_audience.transform(df['TargetAudience'])
df['PolicyType'] = le_policy_type.transform(df['PolicyType'])

# Define input features and target variables
X = df[['TargetAudience', 'PolicyType', 'Budget']]
y_channel = df['Channel']
y_growth_rate = df['GrowthRate']
y_roi = df['ROI']
y_retention_rate = df['CustomerRetentionRate']

# Split the data
X_train, X_test, y_train_channel, y_test_channel = train_test_split(X, y_channel, test_size=0.2, random_state=42)
_, _, y_train_growth_rate, y_test_growth_rate = train_test_split(X, y_growth_rate, test_size=0.2, random_state=42)
_, _, y_train_roi, y_test_roi = train_test_split(X, y_roi, test_size=0.2, random_state=42)
_, _, y_train_retention_rate, y_test_retention_rate = train_test_split(X, y_retention_rate, test_size=0.2, random_state=42)

# Initialize and train models
model_channel = RandomForestClassifier(n_estimators=100, random_state=42)
model_growth_rate = RandomForestRegressor(n_estimators=100, random_state=42)
model_roi = RandomForestRegressor(n_estimators=100, random_state=42)
model_retention_rate = RandomForestRegressor(n_estimators=100, random_state=42)

model_channel.fit(X_train, y_train_channel)
model_growth_rate.fit(X_train, y_train_growth_rate)
model_roi.fit(X_train, y_train_roi)
model_retention_rate.fit(X_train, y_train_retention_rate)

@channel_bp.route('/channelpred', methods=['GET', 'POST'])
def channelpredgwt():

    # Get the role from the session
    user_role = session.get('role')
    if not user_role:
        return redirect(url_for('main.login'))  # Redirect to login if no role is found

    if request.method == 'POST':
        target_audience = request.form.get('target_audience')
        policy_type = request.form.get('policy_type')
        budget = float(request.form.get('budget'))

        # Process the input
        example_input = {
            'TargetAudience': le_target_audience.transform([target_audience])[0],
            'PolicyType': le_policy_type.transform([policy_type])[0],
            'Budget': budget
        }

        input_df = pd.DataFrame([example_input])

        # Predict outcomes
        predicted_channel = le_channel.inverse_transform(model_channel.predict(input_df))
        predicted_growth_rate = model_growth_rate.predict(input_df)[0]
        predicted_roi = model_roi.predict(input_df)[0]
        predicted_retention_rate = model_retention_rate.predict(input_df)[0]

        # Create visualizations
        fig, axes = plt.subplots(1, 3, figsize=(18, 5))
        sns.barplot(x=['Growth Rate'], y=[predicted_growth_rate], ax=axes[0])
        axes[0].set_ylim(0, 20)
        axes[0].set_title('Predicted Growth Rate')

        sns.barplot(x=['ROI'], y=[predicted_roi], ax=axes[1])
        axes[1].set_ylim(0, 3)
        axes[1].set_title('Predicted ROI')

        sns.barplot(x=['Customer Retention Rate'], y=[predicted_retention_rate], ax=axes[2])
        axes[2].set_ylim(60, 100)
        axes[2].set_title('Predicted Customer Retention Rate')

        # Save plot to a BytesIO object
        img = io.BytesIO()
        plt.savefig(img, format='png')
        plt.close(fig)
        img.seek(0)
        plot_url = base64.b64encode(img.getvalue()).decode()

        # Interpretation note
        interpretation = (
            f"Based on the latest analysis, here’s what we predict for your marketing strategy:\n\n"
            f"<br><br><b>Marketing Channel:</b> Our model suggests that the most effective channel for your campaign is likely to be <b><i>{predicted_channel[0]}</i></b>. This choice could help you reach your target audience more effectively and drive better results.\n\n"
            f"<br><br><b>Growth Rate:</b> We anticipate a growth rate of approximately <b><i>{predicted_growth_rate:.2f}%</i></b>. This indicates a positive trend in your marketing efforts, with expected growth in your target metrics.\n\n"
            f"<br><br><b>Return on Investment (ROI):</b> The predicted ROI stands at <b><i>{predicted_roi:.2f}%</i></b>. This figure reflects the efficiency of your marketing investments and suggests a favorable return relative to your expenditures.\n\n"
            f"<br><br><b>Customer Retention Rate:</b> We forecast a customer retention rate of about <b><i>{predicted_retention_rate:.2f}%</i></b>. This high rate demonstrates strong customer loyalty and satisfaction, indicating that your marketing strategies are resonating well with your audience.\n\n"
            f"<br><br><i>Leveraging these insights will help you refine your approach and optimize your marketing strategies for even greater success.</i>"
        )

        return render_template('channelpred-mod/index.html', plot_url=plot_url, interpretation=interpretation, role=user_role)

    return render_template('channelpred-mod/index.html', plot_url=None, interpretation=None, role=user_role)

