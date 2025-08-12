import pandas as pd
import logging
import yaml

# Load configuration
with open("config.yaml", 'r') as f:
    config = yaml.safe_load(f)

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def apply_qaqc_rules(df: pd.DataFrame) -> list:
    """
    Apply QA/QC rules to detect anomalies in marine sensor data.
    Args:
        df (pd.DataFrame): Input DataFrame
    Returns:
        list: List of (column, anomalous_rows) tuples
    """
    anomalies = []
    try:
        # Temperature check
        for col in df.columns:
            if 'Distance (cm)' in col.lower():
                bad = df[df[col] > config['qaqc']['dist_threshold']]
                if not bad.empty:
                    anomalies.append((col, bad))
                    logging.warning(f"Temperature anomalies detected in {col}: {len(bad)} rows")
            
            # Depth check
            if 'Confidence (%)' in col.lower():
                bad = df[df[col] > config['qaqc']['conf_threshold']]
                if not bad.empty:
                    anomalies.append((col, bad))
                    logging.warning(f"Depth anomalies detected in {col}: {len(bad)} rows")
            
            # Salinity check
            """if 'salinity' in col.lower():
                bad = df[df[col] > config['qaqc']['salinity_threshold']]
                if not bad.empty:
                    anomalies.append((col, bad))
                    logging.warning(f"Salinity anomalies detected in {col}: {len(bad)} rows")"""
    
    except Exception as e:
        logging.error(f"Error in QA/QC rules: {str(e)}")
    
    return anomalies