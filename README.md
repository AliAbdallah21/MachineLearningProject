# 📈 Polish Real Estate Price Predictor

A robust machine learning application designed to predict real estate prices per square meter in Poland. This system leverages an **XGBoost model** and integrates key **economic indicators** to provide accurate, data-driven insights.

## ✨ Overview

This application offers a comprehensive solution for analyzing and forecasting real estate values across various regions in Poland. It provides predictions based on property characteristics and relevant economic factors, making it a valuable tool for investors, real estate professionals, and market analysts.

## 🚀 Features

* **Precise Price Prediction:** Predicts square meter prices for all Polish regions (voivodeships or powiats) with a high accuracy of 92%.
* **Multi-faceted Property Analysis:** Incorporates property size (small, medium, large, extra large), time period (year and quarter), and market type (primary or secondary) into predictions.
* **Economic Indicator Integration:** Analyzes the impact of crucial macroeconomic factors, including:
    * **Interest Rates:** Directly influences mortgage affordability and market demand.
    * **Inflation:** Reflects year-over-year price changes and purchasing power.
    * **GDP Growth:** Indicates overall economic health and investment climate.
    * **Unemployment Rate:** Reflects job market stability and consumer confidence.
    * **Apartments Sold:** A direct indicator of market demand and liquidity.
* **Historical Data & Forecasting:** Utilizes historical data from 2010 onwards, enabling both retrospective analysis and future price forecasting.
* **Interactive Web Interface:** Provides an intuitive web-based form for easy input and clear display of prediction results, economic context, and impact analysis.

## 🛠️ Technical Details

### Machine Learning Model

* **Model Type:** XGBoost Regression Model, chosen for its high performance and robustness in handling tabular data.
* **Training:** Trained on extensive historical Polish real estate data.
* **Features:** Integrates region, size category, market type, time period, and dynamic economic indicators.
* **Accuracy:** Achieves 92% accuracy on test data, ensuring reliable predictions.

### Prediction Workflow

1.  **User Input:** Users provide property details and desired time period via the web interface.
2.  **Data Retrieval:** The system retrieves relevant economic indicators for the specified time period from its database.
3.  **Preprocessing:** User inputs and economic data are validated and transformed using pre-trained `scikit-learn` preprocessor and scaler objects.
4.  **Prediction:** The preprocessed features are fed into the loaded XGBoost model to generate the price per square meter prediction.
5.  **Output:** Results are displayed, including the predicted price, the economic indicators used, and an assessment of each indicator's impact on the final prediction.

## 📂 Project Structure

.
├── backend/
│   └── views/             # EJS templates for the frontend UI
├── models/
│   ├── real_estate_model.json   # Primary XGBoost model (JSON format)
│   ├── real_estate_model.pkl    # XGBoost model (pickle format - backup)
│   ├── preprocessor.pkl         # Scikit-learn preprocessor object
│   ├── scaler.pkl               # Scikit-learn scaler object
│   └── economic_indicators.json # Database of historical economic indicators
├── public/
│   └── assets/            # CSS styles and static assets
├── index.js               # Main Express.js server application
└── predict.py             # Python script handling ML model loading and predictions

## ⚙️ Installation & Setup

To get this application running on your local machine, follow these steps:

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/AliAbdallah21/MachineLearningProject.git](https://github.com/AliAbdallah21/MachineLearningProject.git)
    cd MachineLearningProject
    ```

2.  **Install Node.js dependencies (for the web server):**
    ```bash
    npm install
    ```

3.  **Install Python dependencies (for the ML backend):**
    Ensure you have Python installed (preferably Python 3.8+).
    ```bash
    pip install pandas numpy scikit-learn xgboost joblib
    ```

4.  **Verify Model Files:**
    Ensure the following pre-trained model and data files are present in the `/models` directory. These are essential for the application's functionality and should be included in the repository.
    * `real_estate_model.json`
    * `real_estate_model.pkl`
    * `preprocessor.pkl`
    * `scaler.pkl`
    * `economic_indicators.json`

## ▶️ Usage

1.  **Start the application server:**
    ```bash
    node index.js
    ```
    The server will typically start on `http://localhost:3001`.

2.  **Open your web browser** and navigate to:
    ```
    http://localhost:3001
    ```

3.  **Fill in the prediction form** with the desired details:
    * Select a Polish region (voivodeship or powiat).
    * Choose a property size category.
    * Select the time period (month and year).
    * Choose the market type (primary or secondary).

4.  **Click "Calculate Price"** to receive your prediction.

### Prediction Output

The application will display:
* The predicted price per square meter in PLN.
* The economic indicators used in the calculation for the selected period.
* An impact assessment for each economic indicator on the final price.
* An option to make another prediction.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/AliAbdallah21/MachineLearningProject/blob/main/LICENSE) file for details.

## ✍️ Author

**Ali Abdallah**
* **Email:** [aliabdalla2110@gmail.com](mailto:aliabdalla2110@gmail.com)
* **GitHub:** [AliAbdallah21](https://github.com/AliAbdallah21)
