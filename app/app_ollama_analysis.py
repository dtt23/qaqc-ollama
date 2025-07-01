from langchain.llms import Ollama
import logging
import yaml

# Load configuration
with open("config.yaml", 'r') as f:
    config = yaml.safe_load(f)

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def initialize_ollama() -> Ollama:
    """Initialize Ollama with configured model."""
    try:
        return Ollama(model=config['ollama']['model'], timeout=config['ollama']['timeout'])
    except Exception as e:
        logging.error(f"Failed to initialize Ollama: {str(e)}")
        raise

llm = initialize_ollama()

def analyze_with_ollama(data: str) -> str:
    """
    Analyze data using Ollama LLM.
    
    Args:
        data (str): Input data as CSV string
    
    Returns:
        str: LLM analysis summary
    """
    try:
        prompt = f"""
        Review this marine sensor data (CSV format) and provide a detailed QA/QC analysis:
        - Identify potential issues or anomalies
        - Suggest possible causes
        - Recommend corrective actions
        Data:
        {data}
        """
        response = llm(prompt)
        logging.info("Successfully completed Ollama analysis")
        return response
    except Exception as e:
        logging.error(f"Error in Ollama analysis: {str(e)}")
        return f"Analysis failed: {str(e)}"