import os
from pathlib import Path
import logging
import yaml
from preprocess import clean_data
from image_utils import batch_image_processing
from qaqc_rules import apply_qaqc_rules
from ollama_analysis import analyze_with_ollama
from report_gen import generate_report

# Load configuration
with open("config.yaml", 'r') as f:
    config = yaml.safe_load(f)

# Configure logging
logging.basicConfig(
    level=config['logging']['level'],
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(config['logging']['file']),
        logging.StreamHandler()
    ]
)

def run_pipeline():
    """Run the complete QA/QC pipeline."""
    try:
        # Ensure directories exist
        Path(config['data']['processed_dir']).mkdir(parents=True, exist_ok=True)
        Path(config['data']['lowres_dir']).mkdir(parents=True, exist_ok=True)
        Path(config['data']['reports_dir']).mkdir(parents=True, exist_ok=True)
        
        raw_dir = config['data']['raw_dir']
        processed_dir = config['data']['processed_dir']
        reports_dir = config['data']['reports_dir']
        
        # Process CSV files
        image_files = []
        for file in os.listdir(raw_dir):
            if file.endswith(".csv"):
                input_path = os.path.join(raw_dir, file)
                output_path = os.path.join(processed_dir, file)
                
                # Clean data
                df = clean_data(input_path, output_path)
                if df is None:
                    continue
                    
                # Apply QA/QC rules
                anomalies = apply_qaqc_rules(df)
                
                # Find corresponding image
                image_path = None
                base_name = file.split('.')[0]
                for img in os.listdir(raw_dir):
                    if img.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp', '.gif')) and img.startswith(base_name):
                        image_path = os.path.join(raw_dir, img)
                        image_files.append(img)
                        logging.info(f"Matched image {image_path} for CSV {file}")
                        break
                if not image_path:
                    logging.warning(f"No matching image found for CSV {file}")
                
                # Analyze with LLM
                summary = analyze_with_ollama(df.head(100).to_csv(index=False), image_path)
                
                # Generate report
                report_path = os.path.join(reports_dir, file.replace(".csv", ".md"))
                generate_report(summary, report_path, anomalies)
        
        # Process images
        img_count = batch_image_processing(
            raw_dir,
            config['data']['lowres_dir'],
            tuple(config['image']['size']),
            config['image']['quality']
        )
        logging.info(f"Processed {img_count} images")
        
    except Exception as e:
        logging.error(f"Pipeline failed: {str(e)}")

if __name__ == "__main__":
    run_pipeline()