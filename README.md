# Marine Data QA/QC Assistant

This project provides a pipeline for quality assurance and quality control (QA/QC) of marine sensor data (e.g., from AUVs like CTD, ADCP, sonar) using a custom `marine-qaqc` model based on `gemma3:4b` from Ollama. It processes CSV sensor logs and images, detects anomalies, and generates detailed reports with text and image analysis.

## Repository Structure
```
marine_qaqc_project/
├── README.md
├── requirements.txt        # Python dependencies
├── Modelfile              # Custom Ollama model definition
├── app/
│   ├── __init__.py
│   ├── preprocess.py      # Cleans sensor data
│   ├── image_utils.py     # Resizes and compresses images
│   ├── qaqc_rules.py      # Rule-based anomaly detection
│   ├── ollama_analysis.py  # LLM-based analysis (text and images)
│   ├── repoen.py      # Generates Markdown reports
│   ├── main.py            # Main pipeline script
│   ├── config.yaml            # Configuration settings
│   └── data/
    ├── raw/               # Input CSV and image files
    ├── processed/         # Cleaned CSV data
    ├── lowrmages/     # Compressed images
    ├── reports/           # Generated QA/QC reports
```

## Prerequisites
- **System**: Windows, macOS, or Linux with ~4GB free RAM and ~4GB storage.
- **Python**: 3.8 or higher.
- **Ollama**: Version 0.6 or later (for `gemma3:4b` support).
- **Sample Data**: CSV files (e.g., `test.csv`) and images (e.g., `test.jpg`) for testing.

## Installation

### 1. Install Ollama
1. **Download and Install**:
   - **Linux/macOS**:
     ```bash
     curl -fsSL https://ollama.com/install.sh | sh
     ```
   - **Windows**: Download the installer from [https://ollama.com/download](https://ollama.com/download) and run it.
2. **Verify**:
   ```bash
   ollama --version
   ```

### 2. Install the `marine-qaqc` Model
1. **Pull Base Model**:
   ```bash
   ollama pull gemma3:4b
   ```
   This downloads the ~3.3GB `gemma3:4b` model.
2. **Create Custom Model**:
   ```bash
   ollama create marine-qaqc -f Modelfile
   ```
   The `Modelfile` configures `gemma3:4b` for marine QA/QC tasks.
3. **Verify**:
   ```bash
   ollama list
   ```
   Confirm `marine-qaqc` is listed.
4. **Optional**: Remove `gemma3:4b` to save space (~3.3GB):
   ```bash
   ollama rm gemma3:4b
   ```

### 3. Set Up Python Environment
1. **Clone or Navigate to Project**:
   ```bash
   cd /path/to/marine_qaqc_project
   ```
2. **Create Virtual Environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # Linux/macOS
   ```
   On Windows:
   ```cmd
   python -m venv venv
   venv\Scripts\activate
   ```
3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
   This installs `pandas`, `numpy`, `ollama`, `langchain`, `pillow`, `watchdog`, `openai`, `llama-index`, and `pyyaml`.

### 4. Prepare Test Data
1. **Create Directories**:
   ```bash
   mkdir -p data/raw data/processed data/lowres_images data/reports
   ```
2. **Add Sample CSV**:
   Create `data/raw/test.csv`:
   ```csv
   timestamp,temp,depth,salinity
   2025-07-02T10:00:00,25.5,100,35
   2025-07-02T10:01:00,45.0,150,36
   ```
3. **Add Sample Image**:
   Place an image (e.g., `test.jpg`) in `data/raw/`, matching the CSV name (e.g., `test.csv` → `test.jpg`). Use a marine-related image (e.g., AUV camera capture) or any JPEG/PNG for testing.

## Usage
1. **Start Ollama**:
   Run in a separate terminal:
   ```bash
   ollama serve
   ```
2. **Run the Pipeline**:
   ```bash
   cd app
   python3 main.py
   ```
   This:
   - Cleans CSV data (`preprocess.py`).
   - Compresses images (`image_utils.py`).
   - Applies rule-based QA/QC (`qaqc_rules.py`).
   - Analyzes data and images with `marine-qaqc` (`ollama_analysis.py`).
   - Generates reports (`report_gen.py`).

### Outputs
- **Log**: `pipeline.log` (logs processing steps, e.g., `Processed 1 images`, `Successfully completed Ollama analysis with image`).
- **Processed Data**: Cleaned CSVs in `data/processed/`.
- **Compressed Images**: Resized images in `data/lowres_images/`.
- **Reports**: Markdown reports in `data/reports/` (e.g., `test.md`), including CSV and image analysis.

### Example Report (`data/reports/test.md`)
```markdown
## QA/QC Report
**Generated on**: 2025-07-02 10:08:06
## Summary
Anomaly detected: Temperature of 45.0°C at 2025-07-02T10:01:00 is unrealistic. Possible sensor malfunction.
Image analysis: The image shows a clear underwater view with no visible equipment damage.
```
## Notes
- **Image Naming**: Images must match CSV filenames (e.g., `test.jpg` for `test.csv`) for analysis.
- **Performance**: Expect ~20–40s per CSV/image pair due to `gemma3:4b` processing.
- **Vision Support**: `gemma3:4b` analyzes images for marine QA/QC (e.g., equipment issues, underwater features).
- **Dependencies**: If `requirements.txt` fails, install packages manually (e.g., `pip install pandas`).

For issues, check `pipeline.log` or consult the [Ollama documentation](https://github.com/ollama/ollama).