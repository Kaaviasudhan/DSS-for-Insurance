from flask import Blueprint, render_template, redirect, url_for, session
import pandas as pd
import seaborn as sns
import io
import base64

import matplotlib
matplotlib.use('Agg')  # Use a non-interactive backend
import matplotlib.pyplot as plt


# Create a blueprint
eda_bp = Blueprint('eda', __name__)

# Load and prepare the dataset
data = pd.read_csv('app/data/eda-data.csv')
data['Policy_Start_Date'] = pd.to_datetime(data['Policy_Start_Date'])
data['Policy_Start_Year'] = data['Policy_Start_Date'].dt.year

policy_trend = data.groupby(['Policy_Start_Year', 'Policy_Type']).size().reset_index(name='Policy_Count')

def plot_to_base64(fig):
    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    img_data = base64.b64encode(buf.getvalue()).decode('utf-8')
    plt.close(fig)  # Close the figure after saving
    return img_data

@eda_bp.route('/edat')
def edat():
    # Get the role from the session
    user_role = session.get('role')
    if not user_role:
        return redirect(url_for('login'))  # Redirect to login if no role is found

    # Generate various plots and pass them to the template
    fig, ax = plt.subplots()
    sns.countplot(x='Policy_Type', data=data, ax=ax)
    policy_types_img = plot_to_base64(fig)
    plt.close(fig)

    # Distribution of policy types
    fig, ax = plt.subplots()
    sns.countplot(x='Policy_Type', data=data, ax=ax)
    ax.set_title('Distribution of Policy Types')
    policy_types_img = plot_to_base64(fig)
    plt.close(fig)

    # Age distribution
    fig, ax = plt.subplots()
    sns.histplot(data['Customer_Age'], kde=True, ax=ax)
    ax.set_title('Distribution of Customer Ages')
    age_dist_img = plot_to_base64(fig)
    plt.close(fig)

    # Gender distribution
    fig, ax = plt.subplots()
    sns.countplot(x='Gender', data=data, ax=ax)
    ax.set_title('Distribution of Customer Genders')
    gender_dist_img = plot_to_base64(fig)
    plt.close(fig)

    # Region distribution
    fig, ax = plt.subplots()
    sns.countplot(x='Region', data=data, ax=ax)
    ax.set_title('Distribution of Customers by Region')
    region_dist_img = plot_to_base64(fig)
    plt.close(fig)

    # Occupation distribution
    fig, ax = plt.subplots()
    sns.countplot(x='Occupation', data=data, ax=ax)
    ax.set_title('Distribution of Customers by Occupation')
    occupation_dist_img = plot_to_base64(fig)
    plt.close(fig)

    # Marital status distribution
    fig, ax = plt.subplots()
    sns.countplot(x='Marital_Status', data=data, ax=ax)
    ax.set_title('Distribution of Customers by Marital Status')
    marital_status_dist_img = plot_to_base64(fig)
    plt.close(fig)

    # Annual premium distribution
    fig, ax = plt.subplots()
    sns.histplot(data['Annual_Premium'], kde=True, ax=ax)
    ax.set_title('Distribution of Annual Premiums')
    annual_premium_dist_img = plot_to_base64(fig)
    plt.close(fig)

    # Policy start date distribution
    fig, ax = plt.subplots()
    sns.histplot(data['Policy_Start_Date'], kde=True, ax=ax)
    ax.set_title('Distribution of Policy Start Dates')
    start_date_dist_img = plot_to_base64(fig)
    plt.close(fig)

    # Policy tenure distribution
    fig, ax = plt.subplots()
    sns.histplot(data['Tenure'], kde=True, ax=ax)
    ax.set_title('Distribution of Policy Tenures')
    tenure_dist_img = plot_to_base64(fig)
    plt.close(fig)

    # Coverage amount distribution
    fig, ax = plt.subplots()
    sns.histplot(data['Coverage_Amount'], kde=True, ax=ax)
    ax.set_title('Distribution of Coverage Amounts')
    coverage_amount_dist_img = plot_to_base64(fig)
    plt.close(fig)

    # Trend analysis of policy types
    fig, ax = plt.subplots(figsize=(14, 7))
    sns.lineplot(data=policy_trend, x='Policy_Start_Year', y='Policy_Count', hue='Policy_Type', marker='o', ax=ax)
    ax.set_title('Trend Analysis of Policy Types Based on Year')
    ax.set_xlabel('Year')
    ax.set_ylabel('Number of Policies')
    ax.legend(title='Policy Type', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.xticks(rotation=45)
    trend_analysis_img = plot_to_base64(fig)
    plt.close(fig)

    # Policy Type vs. Gender
    fig, ax = plt.subplots(figsize=(14, 7))
    sns.countplot(data=data, x='Policy_Type', hue='Gender', ax=ax)
    ax.set_title('Policy Type vs. Gender')
    policy_gender_img = plot_to_base64(fig)
    plt.close(fig)

    # Policy Type vs. Region
    fig, ax = plt.subplots(figsize=(14, 7))
    sns.countplot(data=data, x='Policy_Type', hue='Region', ax=ax)
    ax.set_title('Policy Type vs. Region')
    policy_region_img = plot_to_base64(fig)
    plt.close(fig)

    # Policy Type vs. Occupation
    fig, ax = plt.subplots(figsize=(14, 7))
    sns.countplot(data=data, x='Policy_Type', hue='Occupation', ax=ax)
    ax.set_title('Policy Type vs. Occupation')
    policy_occupation_img = plot_to_base64(fig)
    plt.close(fig)

    # Policy Type vs. Marital Status
    fig, ax = plt.subplots(figsize=(14, 7))
    sns.countplot(data=data, x='Policy_Type', hue='Marital_Status', ax=ax)
    ax.set_title('Policy Type vs. Marital Status')
    policy_marital_status_img = plot_to_base64(fig)
    plt.close(fig)

    return render_template('eda_mod/index.html',
                           policy_types_img=policy_types_img,
                           age_dist_img=age_dist_img,
                           gender_dist_img=gender_dist_img,
                           region_dist_img=region_dist_img,
                           occupation_dist_img=occupation_dist_img,
                           marital_status_dist_img=marital_status_dist_img,
                           annual_premium_dist_img=annual_premium_dist_img,
                           start_date_dist_img=start_date_dist_img,
                           tenure_dist_img=tenure_dist_img,
                           coverage_amount_dist_img=coverage_amount_dist_img,
                           trend_analysis_img=trend_analysis_img,
                           policy_gender_img=policy_gender_img,
                           policy_region_img=policy_region_img,
                           policy_occupation_img=policy_occupation_img,
                           policy_marital_status_img=policy_marital_status_img,
                           insights=generate_insights(), role=user_role)

def generate_insights():
    insights = {}

    # Insights for distribution of policy types
    insights['policy_types'] = (
        "The distribution of policy types reveals the popularity of different policies. "
        "For instance, if 'Motor' policies are the most common, it may indicate a strong market presence in automotive insurance."
    )

    # Insights for age distribution
    insights['age_dist'] = (
        "The age distribution of customers helps in understanding the age groups that are most engaged with the insurance products. "
        "A peak in certain age ranges might suggest targeted marketing opportunities."
    )

    # Insights for gender distribution
    insights['gender_dist'] = (
        "Gender distribution can provide insights into the market's demographic split. "
        "Significant imbalances might suggest potential areas for more inclusive marketing strategies."
    )

    # Insights for region distribution
    insights['region_dist'] = (
        "The distribution of customers across regions shows which areas have the highest engagement with the insurance policies. "
        "This information is valuable for regional marketing and resource allocation."
    )

    # Insights for occupation distribution
    insights['occupation_dist'] = (
        "Understanding the distribution of customers by occupation can highlight which professional groups are more likely to purchase insurance. "
        "This can guide targeted product offerings."
    )

    # Insights for marital status distribution
    insights['marital_status_dist'] = (
        "Marital status distribution provides insights into customer life stages, which can influence insurance needs and preferences."
    )

    # Insights for annual premium distribution
    insights['annual_premium_dist'] = (
        "The distribution of annual premiums shows the range of spending by customers. "
        "A high concentration in certain ranges could indicate price sensitivity or premium affordability."
    )

    # Insights for policy start date distribution
    insights['start_date_dist'] = (
        "The distribution of policy start dates can help in understanding seasonality trends and planning for policy renewals."
    )

    # Insights for policy tenure distribution
    insights['tenure_dist'] = (
        "Policy tenure distribution indicates how long customers typically stay with the insurance provider. "
        "Longer tenures might suggest higher customer satisfaction and loyalty."
    )

    # Insights for coverage amount distribution
    insights['coverage_amount_dist'] = (
        "Coverage amount distribution helps in understanding the value of policies held by customers. "
        "Higher coverage amounts may suggest a more affluent customer base or higher risk coverage."
    )

    # Insights for trend analysis
    insights['trend_analysis'] = (
        "Trend analysis of policy types over the years can show how customer preferences have evolved. "
        "For example, an increasing trend in 'Health' policies might indicate growing health consciousness among customers."
    )

    return insights