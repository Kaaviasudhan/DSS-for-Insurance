# Decision Support System (DSS) - Insurance Analytics & Prediction System

This project is a web-based system designed to help insurance companies and agents predict and analyze various aspects of their business, such as risk assessment, fraud detection, policy renewal, sales forecasting, healthcare insurance cost predictions, and channel optimization for marketing. The application also provides an AI-powered `Insurance GPT` feature to assist users with queries related to insurance policies.

## Table of Contents
1. [Project Overview](#project-overview)
2. [Features](#features)
3. [Installation](#installation)
4. [Usage](#usage)
5. [Technologies Used](#technologies-used)
6. [Models Used](#models-used)
7. [Screenshots](#screenshots)
8. [Contributing](#contributing)
9. [License](#license)

## Project Overview
The Insurance Analytics & Prediction System aims to provide insightful analytics and predictions using machine learning models for decision-making. The project incorporates several predictive models and dashboards to assist in better business management.

## Features
- **Risk Assessment:** Assess potential risk factors for insurance applicants.
- **Fraud Detection:** Detect fraudulent claims using machine learning models.
- **Policy Renewal Prediction:** Predict whether a policyholder will renew their insurance.
- **Policy Recommendation:** Recommend the best policies to clients based on their profiles.
- **Sales Forecasting:** Predict future sales trends using ARIMA time series models.
- **Channel Optimization:** Predict which marketing channels will be most effective for acquiring new customers.
- **Healthcare Insurance Cost Prediction:** Predict the cost of healthcare insurance based on user inputs like age, gender, BMI, smoking habits, and region.
- **Insurance GPT:** AI-powered assistant to solve queries related to insurance policies. (using llama 3.1 model from huggingface repo.)

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/DSS-for-insurance-analytics-prediction.git
   cd DSS-for-insurance-analytics-prediction
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables by creating a `.env` file with the following details:
   ```plaintext
   MONGO_URI="mongodb://localhost:270xx/lxxm"
   DB_NAME="xx"
   EMAIL_USER="@gmail.com"
   EMAIL_PASS=""
   SECRET_KEY=""

   ```

4. Run the Flask app:
   ```bash
   python inapp.py
   ```

## Usage
Once the server is running, open your browser and go to `http://localhost:5001`.

### Admin Dashboard:
1. Sign in as an admin to access the **Admin Dashboard** and manage data.

### User Functionality:
2. Users can access various features such as risk assessment, fraud detection, healthcare cost predictions, and more.

### Internet Requirement:
- The application checks for internet connectivity before allowing login.

## Technologies Used
- **Backend**: Flask, MongoDB
- **Frontend**: HTML, CSS, JavaScript
- **Machine Learning**: Scikit-learn, ARIMA, Logistic Regression, SVC, Linear Regression
- **Email Service**: Flask-Mail
- **Environment Management**: Python-dotenv
- **Model Deployment**: Pickle for model serialization

## Models Used
- **Time Series Model (ARIMA)**: Used for sales forecasting.
- **Logistic Regression**: Applied for policy renewal prediction.
- **Support Vector Classifier (SVC)**: Used in policy renewal prediction.
- **Linear Regression**: Utilized for risk assessment module.
- **Random Forest**: Employed for healthcare insurance cost prediction.

## Screenshots
All Screenshots and images are added in the documents and presentation ppts.

## Project Video

[![Watch the video](https://github.com/Kaaviasudhan/DSS-for-Insurance-Sector/blob/main/Documents/LLM_Recording.mp4)

Click the image above to watch the demo video or [download it here](https://github.com/Kaaviasudhan/DSS-for-Insurance-Sector/blob/main/Documents/LLM_Recording.mp4).

## Contributing
1. Fork the project.
2. Create your feature branch (`git checkout -b feature/YourFeature`).
3. Commit your changes (`git commit -m 'Add YourFeature'`).
4. Push to the branch (`git push origin feature/YourFeature`).
5. Open a Pull Request.

## Disclaimer
This project is developed for educational purposes only and is not intended for commercial use.

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss the changes.
