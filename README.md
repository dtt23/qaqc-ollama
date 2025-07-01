# qaqc-ollama
AUV Data QA/QC Assistant with Ollama

GitHub-ready repository structure for marine sensor data QA/QC with customizable LLM parameters.

Repo Layout:

├── README.md
├── requirements.txt
├── config.yaml              # Configuration file for pipeline settings
├── Modelfile                # Enhanced model configuration
├── app/
│   ├── __init__.py
│   ├── preprocess.py        # Enhanced data cleaning with validation
│   ├── image_utils.py       # Improved image processing with batch support
│   ├── qaqc_rules.py        # Expanded rule-based QA/QC
│   ├── ollama_analysis.py   # Robust LLM interaction with error handling
│   ├── report_gen.py        # Enhanced report generation with templates
│   └── main.py              # Main pipeline with logging
└── data/
    ├── raw/                 # Raw incoming files
    ├── processed/           # Cleaned data
    ├── lowres_images/       # Compressed images
    └── reports/             # Generated summaries


Marine data QA/QC assistant specialised in analysing sensor logs from AUVs (e.g., CTD, ADCP, sonar). Tasks include:
Validating sensor data for consistency and accuracy.
Identifying and explaining anomalies in marine sensor data.
Summarising findings in clear, concise, and professional language.
Providing actionable recommendations for data quality improvement.
