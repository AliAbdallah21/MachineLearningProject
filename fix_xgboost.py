#!/usr/bin/env python3
import os
import sys
import logging
import xgboost as xgb
import joblib

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('fix_model')

def fix_model():
    try:
        model_dir = os.path.join(os.path.dirname(__file__), 'models')
        model_path = os.path.join(model_dir, 'real_estate_model.pkl')
        json_path = os.path.join(model_dir, 'real_estate_model.json')
        
        # Try loading with joblib
        logger.info(f"Attempting to load model with joblib: {model_path}")
        model = joblib.load(model_path)
        
        # If it's an XGBoost model, save in JSON format
        if isinstance(model, xgb.XGBRegressor):
            logger.info("Model is an XGBoost regressor, saving in JSON format")
            model.save_model(json_path)
            logger.info(f"Successfully saved model to: {json_path}")
            print(f"Model fixed and saved to {json_path}")
            return True
        else:
            logger.info(f"Model is not an XGBoost regressor: {type(model)}")
            print(f"Model is not an XGBoost regressor: {type(model)}")
            return False
    
    except Exception as e:
        logger.error(f"Error fixing model: {str(e)}")
        print(f"Error fixing model: {str(e)}")
        return False

if __name__ == "__main__":
    fix_model()