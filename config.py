"""
Configuration settings for AI Paper Checker
"""
import os

# API Configuration
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
DEFAULT_AI_MODEL = "gpt-3.5-turbo"

# Batch Processing Settings
MAX_BATCH_SIZE = 100  # Maximum number of papers to process at once
MAX_WORKERS = 5  # Number of parallel workers for processing

# Grading Settings
MCQ_PASSING_PERCENTAGE = 40  # Papers below this are flagged for review
TEXTUAL_PASSING_PERCENTAGE = 30  # Papers below this are flagged for review

# Scoring Weights (must sum to 100)
MCQ_WEIGHT = 50  # Weight for MCQ section in final score
TEXTUAL_WEIGHT = 50  # Weight for textual section in final score

# File Processing
SUPPORTED_FORMATS = ['.pdf', '.docx', '.txt']
MAX_FILE_SIZE_MB = 10  # Maximum file size in MB

# Excel Export
EXCEL_SHEET_NAME = "Grading Results"
EXCEL_SUMMARY_SHEET = "Summary"

# UI Configuration
UI_TITLE = "AI Paper Checker - Complete MVP"
UI_THEME = "soft"
UI_SERVER_NAME = "0.0.0.0"
UI_SERVER_PORT = 7860
UI_SHARE = False  # Set to True to create a public link

# Temp Directory
TEMP_DIR = "/tmp/jiaoshi_temp"
OUTPUT_DIR = "output"

# Progress Tracking
SHOW_PROGRESS_BAR = True
PROGRESS_BAR_STYLE = "blue"

# Error Handling
CONTINUE_ON_ERROR = True  # Continue processing remaining papers if one fails
LOG_ERRORS = True  # Log errors to file

# Feature Flags
ENABLE_AI_GRADING = True  # Enable AI-powered textual grading (requires API key)
ENABLE_STUDENT_INFO_EXTRACTION = True  # Extract student info from documents
ENABLE_AUTO_REVIEW_FLAGGING = True  # Automatically flag papers for review
ENABLE_EXCEL_FORMATTING = True  # Apply conditional formatting to Excel output

# Logging
LOG_LEVEL = "INFO"  # Options: DEBUG, INFO, WARNING, ERROR
LOG_FILE = "paper_checker.log"

def validate_config():
    """Validate configuration settings."""
    errors = []
    
    if MCQ_WEIGHT + TEXTUAL_WEIGHT != 100:
        errors.append(f"Scoring weights must sum to 100 (currently: {MCQ_WEIGHT + TEXTUAL_WEIGHT})")
    
    if MAX_BATCH_SIZE <= 0 or MAX_BATCH_SIZE > 1000:
        errors.append(f"MAX_BATCH_SIZE must be between 1 and 1000 (currently: {MAX_BATCH_SIZE})")
    
    if MAX_WORKERS <= 0:
        errors.append(f"MAX_WORKERS must be positive (currently: {MAX_WORKERS})")
    
    if errors:
        raise ValueError("Configuration errors:\n" + "\n".join(errors))
    
    return True

# Validate on import
if __name__ != "__main__":
    validate_config()
