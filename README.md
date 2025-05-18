# Polish Real Estate Price Predictor

A machine learning application that predicts real estate prices per square meter in Poland based on region, size, time period, and market type with economic indicator analysis.

## Description

This application uses an XGBoost machine learning model with 92% accuracy to predict real estate prices in Poland. It takes into account:

- Region (voivodeship or powiat)
- Property size (small, medium, large, or extra large)
- Time period (year and quarter)
- Market type (primary or secondary)
- Economic indicators (interest rates, inflation, GDP growth, unemployment, apartments sold)

## Features

- Predict square meter prices for all Polish regions
- View economic factors affecting the prediction
- Analyze the impact of each economic indicator
- Support for both primary and secondary markets
- Historical data from 2010 and forecasting capabilities

## Installation

1. Clone the repository:
```bash
git clone https://github.com/AliAbdallah21/MachineLearningProject.git
cd MachineLearningProject

2. Install dependencies:
npm install

3. Make sure Python is installed with the required packages:
pip install pandas numpy scikit-learn xgboost joblib


Required Files
Ensure the following model files are in the /models directory:

real_estate_model.json (XGBoost model in JSON format)
real_estate_model.pkl (XGBoost model in pickle format - backup)
preprocessor.pkl (Sklearn preprocessor)
scaler.pkl (Sklearn scaler)
economic_indicators.json (Economic indicators database)


Usage:
1. Start the application: 
node index.js

2. Open your browser and navigate to:
http://localhost:3001

3. Fill in the prediction form with:
Select a Polish region (voivodeship or powiat)
Choose a property size category
Select the time period (month and year)
Choose the market type (primary or secondary)

4. Click "Calculate Price" to get your prediction
Prediction Output
The application provides:

Predicted price per square meter in PLN
Economic indicators used in the calculation
Impact assessment of each economic indicator on the price
Option to make another prediction

Project Structure
/backend/views/ - EJS templates for the frontend
/models/ - ML model files and economic indicators data
/public/assets/ - CSS styles and static assets
index.js - Express server and main application
predict.py - Python script that handles ML predictions

Technical Details
Machine Learning Model
Uses XGBoost regression model trained on historical Polish real estate data
Features include region, size category, market type, and time period
Integrates with economic indicators for the specified time period
Model accuracy: 92% on test data

Economic Indicators
Interest rates: Impact on mortgage affordability
Inflation: Year-over-year price changes
GDP growth: Overall economic health
Unemployment rate: Job market stability
Apartments sold: Market demand indicator

Prediction Workflow
1. User inputs are validated and preprocessed
2. The system retrieves relevant economic indicators
3. Features are transformed using stored preprocessor and scaler
4. XGBoost model generates the price prediction
5. Results are displayed with economic context and impact analysis

License
MIT

Author
Ali Abdallah