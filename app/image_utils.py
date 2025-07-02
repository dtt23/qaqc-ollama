from PIL import Image
import os
from pathlib import Path
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def compress_image(input_path: str, output_path: str, size: tuple = (640, 480), quality: int = 60) -> bool:
    """
    Compress and resize an image.
    
    Args:
        input_path (str): Input image path
        output_path (str): Output image path
        size (tuple): Target size (width, height)
        quality (int): JPEG quality (0-100)
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        img = Image.open(input_path)
        img = img.resize(size, Image.Resampling.LANCZOS)
        
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        img.save(output_path, quality=quality, optimize=True)
        logging.info(f"Compressed image saved to: {output_path}")
        return True
    except Exception as e:
        logging.error(f"Error processing image {input_path}: {str(e)}")
        return False

def batch_image_processing(input_dir: str, output_dir: str, size: tuple, quality: int) -> int:
    """
    Process all images in a directory.
    
    Returns:
        int: Number of successfully processed images
    """
    processed = 0
    for img in os.listdir(input_dir):
        if img.lower().endswith(('.jpg', '.jpeg', '.png')):
            in_path = os.path.join(input_dir, img)
            out_path = os.path.join(output_dir, img)
            if compress_image(in_path, out_path, size, quality):
                processed += 1
    return processed