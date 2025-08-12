from langchain_ollama import OllamaLLM
import logging
import yaml
import ollama
import base64
from pathlib import Path

# Load configuration
with open("config.yaml", 'r') as f:
    config = yaml.safe_load(f)

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def initialize_ollama() -> OllamaLLM:
    """Initialize Ollama with configured model."""
    try:
        return OllamaLLM(model=config['ollama']['model'], timeout=config['ollama']['timeout'])
    except Exception as e:
        logging.error(f"Failed to initialize Ollama: {str(e)}")
        raise

llm = initialize_ollama()

def encode_image(image_path: str) -> str:
    """Encode image to base64 for Ollama vision input."""
    try:
        if not Path(image_path).exists():
            logging.error(f"Image path {image_path} does not exist")
            return ""
        with open(image_path, "rb") as image_file:
            encoded = base64.b64encode(image_file.read()).decode('utf-8')
            logging.info(f"Successfully encoded image: {image_path}")
            return encoded
    except Exception as e:
        logging.error(f"Error encoding image {image_path}: {str(e)}")
        return ""

def analyze_with_ollama(data: str, image_path: str = None) -> str:
    """
    Analyze data and optional image using Ollama LLM.
    Args:
        data (str): Input data as CSV string
        image_path (str, optional): Path to image for analysis
    Returns:
        str: LLM analysis summary
    """
    try:
        prompt = f"""
        Review this marine sensor data (CSV format, ignore column 1, use the date and time for timestamping and make use of the other values especially the confidence level to test the accuracy of the data) and provide a detailed QA/QC analysis:
        - Identify potential issues or anomalies
        - Suggest possible causes
        - Recommend corrective actions
        Data:
        {data if data else 'No CSV data provided'}
        """
        if image_path:
            logging.info(f"Attempting to analyze image: {image_path}")
            image_base64 = encode_image(image_path)
            if image_base64:
                prompt += "\nAdditionally, analyze this image for any visual anomalies relevant to marine QA/QC (e.g., AUV camera data, equipment issues, or environmental conditions)."
                response = ollama.chat(
                    model=config['ollama']['model'],
                    messages=[
                        {
                            'role': 'user',
                            'content': prompt,
                            'images': [image_base64]
                        }
                    ]
                )
                logging.info("Successfully completed Ollama analysis with image")
                return response['message']['content']
            else:
                logging.warning("Image encoding failed, falling back to text-only analysis")
        
        # Text-only analysis
        response = llm(prompt)
        logging.info("Successfully completed Ollama text analysis")
        return response
    except Exception as e:
        logging.error(f"Error in Ollama analysis: {str(e)}")
        return f"Analysis failed: {str(e)}"