import pandas as pd
import logging
import numpy as np
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def clean_data(file_path: str, output_path: str) -> pd.DataFrame:
    """
    Clean and validate sensor data from CSV files.
    
    Args:
        file_path (str): Path to input CSV
        output_path (str): Path to save cleaned data
    
    Returns:
        pd.DataFrame: Cleaned DataFrame
    """
    try:
        logging.info(f"Processing file: {file_path}")
        df = pd.read_csv(file_path)
        
        # Remove duplicates
        initial_rows = len(df)
        df.drop_duplicates(inplace=True)
        logging.info(f"Removed {initial_rows - len(df)} duplicate rows")
        
        # Handle missing values
        df.interpolate(method='linear', inplace=True, limit_direction='both')
        df.fillna(method='ffill', inplace=True)
        
        # Basic validation
        if df.empty:
            logging.warning(f"Empty DataFrame after cleaning: {file_path}")
            return None
            
        # Save cleaned data
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(output_path, index=False)
        logging.info(f"Saved cleaned data to: {output_path}")
        
        return df
    
    except Exception as e:
        logging.error(f"Error processing {file_path}: {str(e)}")
        return None