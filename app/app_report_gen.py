import os
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def generate_report(summary_text: str, output_path: str, anomalies: list) -> None:
    """
    Generate a QA/QC report in Markdown format.
    
    Args:
        summary_text (str): LLM-generated summary
        output_path (str): Output file path
        anomalies (list): List of detected anomalies
    """
    try:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, 'w') as f:
            f.write("# QA/QC Report\n\n")
            f.write(f"**Generated on**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write("## Summary\n")
            f.write(summary_text + "\n\n")
            
            if anomalies:
                f.write("## Detected Anomalies\n")
                for col, bad in anomalies:
                    f.write(f"### {col}\n")
                    f.write(f"{len(bad)} anomalous rows detected\n")
                    f.write(bad.head().to_markdown() + "\n\n")
        
        logging.info(f"Report generated at: {output_path}")
    except Exception as e:
        logging.error(f"Error generating report: {str(e)}")