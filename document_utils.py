"""
AI Paper Checker - Core utilities for document processing
"""
import os
import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import PyPDF2
import pdfplumber
from docx import Document


def extract_text_from_pdf(file_path: str) -> str:
    """Extract text from PDF file using multiple methods for robustness."""
    text = ""
    
    # Try with pdfplumber first (better for tables and layout)
    try:
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
    except Exception as e:
        print(f"pdfplumber failed: {e}, trying PyPDF2")
    
    # Fallback to PyPDF2 if pdfplumber fails or returns empty
    if not text.strip():
        try:
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page in pdf_reader.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
        except Exception as e:
            print(f"PyPDF2 also failed: {e}")
    
    return text.strip()


def extract_text_from_docx(file_path: str) -> str:
    """Extract text from DOCX file."""
    try:
        doc = Document(file_path)
        text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
        return text.strip()
    except Exception as e:
        print(f"Error extracting from DOCX: {e}")
        return ""


def extract_text_from_txt(file_path: str) -> str:
    """Extract text from TXT file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read().strip()
    except UnicodeDecodeError:
        # Try with different encoding
        try:
            with open(file_path, 'r', encoding='latin-1') as file:
                return file.read().strip()
        except Exception as e:
            print(f"Error extracting from TXT: {e}")
            return ""
    except Exception as e:
        print(f"Error extracting from TXT: {e}")
        return ""


def extract_text_from_file(file_path: str) -> str:
    """Extract text from supported file formats."""
    file_ext = Path(file_path).suffix.lower()
    
    if file_ext == '.pdf':
        return extract_text_from_pdf(file_path)
    elif file_ext == '.docx':
        return extract_text_from_docx(file_path)
    elif file_ext == '.txt':
        return extract_text_from_txt(file_path)
    else:
        raise ValueError(f"Unsupported file format: {file_ext}")


def extract_student_info(text: str, filename: str) -> Dict[str, str]:
    """
    Extract student information from document text and filename.
    
    Looks for patterns like:
    - Name: John Doe
    - Student ID: 12345
    - Roll No: 67890
    - Also extracts from filename patterns like: JohnDoe_12345.pdf
    """
    info = {
        'name': '',
        'student_id': '',
        'roll_no': ''
    }
    
    # Extract from text content
    name_patterns = [
        r'(?:name|student name|full name)\s*[:：]\s*([A-Za-z\s]+?)(?:\n|$)',
        r'(?:name|student name|full name)\s*[:：]\s*([^\n]+)',
    ]
    
    id_patterns = [
        r'(?:student id|id|student number|registration number)\s*[:：]\s*([A-Za-z0-9]+)',
        r'(?:id|student id)\s*[:：]\s*([0-9]+)',
    ]
    
    roll_patterns = [
        r'(?:roll no|roll number|roll)\s*[:：]\s*([A-Za-z0-9]+)',
    ]
    
    text_lower = text.lower()
    
    for pattern in name_patterns:
        match = re.search(pattern, text_lower, re.IGNORECASE)
        if match:
            info['name'] = match.group(1).strip().title()
            break
    
    for pattern in id_patterns:
        match = re.search(pattern, text_lower, re.IGNORECASE)
        if match:
            info['student_id'] = match.group(1).strip()
            break
    
    for pattern in roll_patterns:
        match = re.search(pattern, text_lower, re.IGNORECASE)
        if match:
            info['roll_no'] = match.group(1).strip()
            break
    
    # Extract from filename
    # Pattern: Name_ID.ext or Name-ID.ext or similar
    filename_base = Path(filename).stem
    
    # Try to extract student info from filename
    if not info['name'] or not info['student_id']:
        # Try patterns like: JohnDoe_12345 or John_Doe_12345
        parts = re.split(r'[_\-]', filename_base)
        if len(parts) >= 2:
            # Last part might be ID if it's numeric
            if parts[-1].isdigit() and not info['student_id']:
                info['student_id'] = parts[-1]
                if not info['name']:
                    info['name'] = ' '.join(parts[:-1]).replace('_', ' ').title()
            elif not info['name']:
                info['name'] = filename_base.replace('_', ' ').replace('-', ' ').title()
    
    # If still no name, use filename
    if not info['name']:
        info['name'] = filename_base.replace('_', ' ').replace('-', ' ').title()
    
    return info


def parse_answer_key(answer_key_text: str) -> Dict[str, str]:
    """
    Parse answer key from text format.
    
    Expected format:
    1. A
    2. B
    3. C
    Or:
    Q1: A
    Q2: B
    """
    answers = {}
    
    lines = answer_key_text.strip().split('\n')
    for line in lines:
        line = line.strip()
        if not line:
            continue
        
        # Try pattern: "1. A" or "1) A" or "1: A"
        match = re.match(r'(\d+)[\.\):\s]+([A-Za-z0-9]+)', line)
        if match:
            q_num = match.group(1)
            answer = match.group(2).upper()
            answers[q_num] = answer
            continue
        
        # Try pattern: "Q1: A" or "Q1. A"
        match = re.match(r'[Qq](\d+)[\.\):\s]+([A-Za-z0-9]+)', line)
        if match:
            q_num = match.group(1)
            answer = match.group(2).upper()
            answers[q_num] = answer
    
    return answers


def extract_mcq_answers(text: str, num_questions: Optional[int] = None) -> Dict[str, str]:
    """
    Extract MCQ answers from student's paper.
    
    Looks for patterns like:
    1. A
    2. B
    3. C
    """
    answers = {}
    
    lines = text.split('\n')
    for line in lines:
        line = line.strip()
        if not line:
            continue
        
        # Try pattern: "1. A" or "1) A" or "1: A"
        match = re.match(r'(\d+)[\.\):\s]+([A-Ea-e])\b', line)
        if match:
            q_num = match.group(1)
            answer = match.group(2).upper()
            answers[q_num] = answer
            continue
        
        # Try pattern: "Q1: A" or "Q1. A"
        match = re.match(r'[Qq](\d+)[\.\):\s]+([A-Ea-e])\b', line)
        if match:
            q_num = match.group(1)
            answer = match.group(2).upper()
            answers[q_num] = answer
    
    return answers


def calculate_mcq_score(student_answers: Dict[str, str], 
                        answer_key: Dict[str, str]) -> Tuple[int, int, List[str]]:
    """
    Calculate MCQ score with 100% accuracy.
    
    Returns: (correct_count, total_questions, incorrect_questions)
    """
    correct = 0
    incorrect = []
    total = len(answer_key)
    
    for q_num, correct_answer in answer_key.items():
        student_answer = student_answers.get(q_num, '').upper()
        if student_answer == correct_answer.upper():
            correct += 1
        else:
            incorrect.append(q_num)
    
    return correct, total, incorrect
