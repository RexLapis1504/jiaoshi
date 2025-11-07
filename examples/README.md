# Examples

This directory contains example files to help you get started with the AI Paper Checker.

## Files

### answer_key_template.txt
Template for creating MCQ answer keys. Shows all supported formats.

### sample_paper.txt
Example student paper with:
- Student information
- MCQ answers
- Subjective answers

## Usage

1. **Try the sample paper:**
   ```bash
   python app.py
   # Upload sample_paper.txt
   # Use answer_key_template.txt as answer key
   ```

2. **Create your own papers:**
   - Copy sample_paper.txt as a template
   - Modify student info and answers
   - Upload to the system

3. **Create answer keys:**
   - Use answer_key_template.txt format
   - One answer per line
   - Supports multiple formats (see template)

## Supported Formats

Papers can be:
- Plain text (.txt)
- PDF documents (.pdf)
- Word documents (.docx)

Answer keys can be:
- Plain text (.txt)
- Pasted directly in the UI
