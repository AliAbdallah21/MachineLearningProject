#!/usr/bin/env python3
import sys
import os
import logging
import json
import joblib
import pandas as pd
import numpy as np
import xgboost as xgb

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('predict')

def validate_input(region, size, year, quarter, market_type):
    """Validate input parameters"""
    # Validate region
    if not isinstance(region, str) or len(region) == 0:
        raise ValueError("Region must be a non-empty string")
    
    # Validate size
    valid_sizes = ['do 40 m²', 'od 40.1 do 60 m²', 'od 60.1 do 80 m²', 'od 80.1 m²']
    if size not in valid_sizes:
        raise ValueError(f"Size must be one of: {', '.join(valid_sizes)}")
    
    # Validate year
    try:
        year_int = int(year)
        if year_int < 2010 or year_int > 2025:
            raise ValueError("Year must be between 2010 and 2025")
    except ValueError:
        raise ValueError("Year must be a valid integer")
    
    # Validate quarter
    try:
        quarter_int = int(quarter)
        if quarter_int < 1 or quarter_int > 4:
            raise ValueError("Quarter must be between 1 and 4")
    except ValueError:
        raise ValueError("Quarter must be a valid integer")
    
    # Validate market type
    valid_markets = ['primary market', 'secondary market']
    if market_type not in valid_markets:
        raise ValueError(f"Market type must be one of: {', '.join(valid_markets)}")
    
    return True

def get_economic_indicators(year, quarter):
    """Get real economic indicators for a specific year and quarter"""
    # Load the economic indicators database
    model_dir = os.path.join(os.path.dirname(__file__), 'models')
    indicators_path = os.path.join(model_dir, 'economic_indicators.json')
    
    if not os.path.exists(indicators_path):
        logger.warning(f"Economic indicators file not found: {indicators_path}")
        # Return default values if file not found
        return {
            "interest_rate": 0.9,
            "inflation": 103.0,
            "gdp_growth": 97.7,
            "unemployment": 6.1,
            "apartments_sold": 630
        }
    
    # Load the indicators database
    with open(indicators_path, 'r') as f:
        indicators_db = json.load(f)
    
    # Look up by year and quarter
    key = f"{year}_{quarter}"
    if key in indicators_db:
        logger.info(f"Found economic indicators for {year}-Q{quarter}")
        return {
            "interest_rate": indicators_db[key]["interest_rate"],
            "inflation": indicators_db[key]["inflation"],
            "gdp_growth": indicators_db[key]["gdp_growth"],
            "unemployment": indicators_db[key]["unemployment"],
            "apartments_sold": indicators_db[key]["apartments_sold"]
        }
    
    # If not found directly, find closest available indicators
    closest_key = None
    min_diff = float('inf')
    
    for db_key in indicators_db:
        db_year, db_quarter = map(int, db_key.split('_'))
        # Calculate difference in quarters
        diff = abs(int(year) - db_year) * 4 + abs(int(quarter) - db_quarter)
        if diff < min_diff:
            min_diff = diff
            closest_key = db_key
    
    if closest_key:
        logger.info(f"Using closest economic indicators from {closest_key.replace('_', '-Q')} for {year}-Q{quarter}")
        return {
            "interest_rate": indicators_db[closest_key]["interest_rate"],
            "inflation": indicators_db[closest_key]["inflation"],
            "gdp_growth": indicators_db[closest_key]["gdp_growth"],
            "unemployment": indicators_db[closest_key]["unemployment"],
            "apartments_sold": indicators_db[closest_key]["apartments_sold"]
        }
    
    # Default fallback if no data found
    logger.warning(f"No economic indicators found for {year}-Q{quarter}, using defaults")
    return {
        "interest_rate": 0.9,
        "inflation": 103.0,
        "gdp_growth": 97.7,
        "unemployment": 6.1,
        "apartments_sold": 630
    }

def predict_price(region, size, year, quarter, market_type='primary market'):
    """Make a prediction with proper validation and handling"""
    try:
        # Validate inputs
        validate_input(region, size, year, quarter, market_type)
        
        # Paths to model files
        model_dir = os.path.join(os.path.dirname(__file__), 'models')
        
        # List all files in the model directory to debug
        files_in_dir = os.listdir(model_dir)
        logger.info(f"Files in models directory: {files_in_dir}")
        
        json_path = os.path.join(model_dir, 'real_estate_model.json')
        preprocessor_path = os.path.join(model_dir, 'preprocessor.pkl')
        scaler_path = os.path.join(model_dir, 'scaler.pkl')
        
        # Load model using XGBoost's native loader for JSON
        model = xgb.XGBRegressor()
        model.load_model(json_path)
        logger.info(f"Successfully loaded XGBoost model from JSON: {json_path}")
        
        # Load preprocessor and scaler with joblib
        preprocessor = joblib.load(preprocessor_path)
        scaler = joblib.load(scaler_path)
        logger.info("Successfully loaded preprocessor and scaler")
        
        # Column names for input data
        column_names = [
            'Location',
            'Attribute',
            'Type of market',
            'Type of property',
            'year',
            'number of apartments sold',
            'usable floor space',
            'average value of 1 square meter',
            'weighted average interest rate on new housing loans to households',
            'inflation same period of previous year',
            'Dynamics of gross domestic product per capita, previous year = 100'
        ]
        
        # Format quarter text
        quarter_text = f"{quarter}{'st' if int(quarter) == 1 else 'nd' if int(quarter) == 2 else 'rd' if int(quarter) == 3 else 'th'} quarter"
        
        # Map size category
        size_mapping = {
            'do 40 m²': 'up to 40 square meters',
            'od 40.1 do 60 m²': 'from 40.1 to 60\u202fm²',
            'od 60.1 do 80 m²': 'from 60.1 to 80\u202fm²',
            'od 80.1 m²': 'from 80.1\u202fm²'
        }
        size_category = size_mapping.get(size, size)
        
        # Get economic indicators for the specified year and quarter
        indicators = get_economic_indicators(year, quarter)
        interest_rate = indicators["interest_rate"]
        inflation = indicators["inflation"]
        gdp_growth = indicators["gdp_growth"]
        unemployment = indicators["unemployment"]
        apartments_sold = indicators["apartments_sold"]
        
        # Create input data
        input_data = pd.DataFrame([
            [region, quarter_text, market_type, size_category, 
             int(year), apartments_sold, 0, 0, 
             interest_rate, inflation, gdp_growth]
        ], columns=column_names)
        
        logger.info(f"Prepared input data with economic indicators: interest={interest_rate}, inflation={inflation}, gdp={gdp_growth}")
        
        # Apply preprocessing and scaling
        try:
            X_preprocessed = preprocessor.transform(input_data)
            X_scaled = scaler.transform(X_preprocessed)
            logger.info("Successfully preprocessed and scaled input data")
        except Exception as e:
            logger.error(f"Error in preprocessing: {str(e)}")
            raise ValueError(f"Failed to preprocess input data: {str(e)}")
        
        # Get prediction from model
        try:
            raw_prediction = float(model.predict(X_scaled)[0])
            logger.info(f"Raw model prediction: {raw_prediction}")
        except Exception as e:
            logger.error(f"Error in prediction: {str(e)}")
            raise ValueError(f"Failed to make prediction: {str(e)}")
        
        # Ensure positive prediction
        prediction = abs(raw_prediction)
        
        # Print economic indicators for display in UI
        print(f"ECONOMIC_INDICATORS: interest={interest_rate}, " +
              f"inflation={inflation}, " +
              f"gdp={gdp_growth}, " +
              f"unemployment={unemployment}, " +
              f"apartments_sold={apartments_sold}")
        
        return prediction
    
    except Exception as e:
        logger.error(f"Error in prediction: {str(e)}")
        raise

if __name__ == "__main__":
    try:
        # Get command line arguments
        if len(sys.argv) < 5:
            print("Usage: python predict.py <region> <year> <quarter> <size> [market_type]")
            sys.exit(1)
        
        region = sys.argv[1]
        year = sys.argv[2]
        quarter = sys.argv[3]
        size = sys.argv[4]
        market_type = sys.argv[5] if len(sys.argv) > 5 else 'primary market'
        
        logger.info(f"Predicting for region={region}, year={year}, quarter={quarter}, size={size}, market={market_type}")
        
        # Get prediction
        price = predict_price(region, size, year, quarter, market_type)
        
        # Print result (ensuring positive)
        logger.info(f"Final prediction: {price}")
        print(price)
        
        sys.exit(0)
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        print(f"ERROR: {str(e)}")
        sys.exit(1)