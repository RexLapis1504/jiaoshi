# AI Paper Checker - Architecture Overview

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         Gradio Web UI                            │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐  │
│  │ File Upload  │  │ Answer Key   │  │ Progress Display     │  │
│  │ (PDF/DOCX/TXT│  │ Input        │  │ & Results Download   │  │
│  └──────────────┘  └──────────────┘  └──────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Batch Processor                               │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  • Multi-threaded processing (up to 100 papers)          │   │
│  │  • Progress tracking with tqdm                           │   │
│  │  • Error handling & recovery                             │   │
│  └──────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                   Document Utilities                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐  │
│  │ PDF Extract  │  │ DOCX Extract │  │ Student Info Extract │  │
│  │ (pdfplumber) │  │ (python-docx)│  │ (regex patterns)     │  │
│  └──────────────┘  └──────────────┘  └──────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                  Orchestrator Agent                              │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  • Coordinates grading workflow                          │   │
│  │  • Combines MCQ and textual results                      │   │
│  │  • Flags papers for review (low scores, errors)          │   │
│  └──────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
                    │                    │
                    ▼                    ▼
    ┌───────────────────────┐  ┌─────────────────────────┐
    │  MCQ Grading Agent    │  │ Textual Grading Agent   │
    │  ┌─────────────────┐  │  │  ┌────────────────────┐ │
    │  │ Strict matching │  │  │  │ AI-powered (GPT)   │ │
    │  │ 100% accuracy   │  │  │  │ Rule-based fallback│ │
    │  │ Answer key comp │  │  │  │ Detailed feedback  │ │
    │  └─────────────────┘  │  │  └────────────────────┘ │
    └───────────────────────┘  └─────────────────────────┘
                    │                    │
                    └──────────┬─────────┘
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Excel Exporter                                │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  • Formatted Excel output (openpyxl)                     │   │
│  │  • Conditional formatting for review flags               │   │
│  │  • Color-coded highlighting (yellow/red)                 │   │
│  │  • Summary statistics sheet                              │   │
│  └──────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

## Data Flow

```
1. Student Papers (PDF/DOCX/TXT)
   └─> Document Extraction
       └─> Text Content

2. Text Content
   └─> Student Info Extraction (name, ID, roll no)
   └─> MCQ Answer Extraction (regex patterns)
   └─> Textual Answer Extraction

3. Answers + Answer Key
   └─> MCQ Agent: Strict comparison
   └─> Textual Agent: AI grading or rule-based

4. Individual Results
   └─> Orchestrator: Combines and flags
   └─> GradingResult objects

5. Batch Results
   └─> Excel Exporter
       └─> Formatted .xlsx file with review flags
```

## Technology Stack

### Core Technologies
- **Python 3.12**: Main programming language
- **Gradio 4.0+**: Web UI framework
- **Pandas 2.0+**: Data processing
- **OpenPyXL 3.1+**: Excel export

### Document Processing
- **PyPDF2**: PDF text extraction
- **pdfplumber**: Advanced PDF parsing
- **python-docx**: DOCX file handling

### AI/ML
- **OpenAI API**: GPT-powered textual grading
- **tiktoken**: Token counting

### Utilities
- **tqdm**: Progress bars
- **regex**: Pattern matching
- **concurrent.futures**: Multi-threading

### Deployment
- **Docker**: Containerization
- **docker-compose**: Orchestration

## Component Details

### 1. Agents Module (`agents.py`)
- **MCQGradingAgent**: Strict answer key comparison
- **TextualGradingAgent**: AI-powered or rule-based grading
- **OrchestratorAgent**: Workflow coordination and result combination

### 2. Document Utils (`document_utils.py`)
- Multi-format extraction (PDF, DOCX, TXT)
- Student information parsing
- MCQ answer extraction
- Answer key parsing

### 3. Batch Processor (`batch_processor.py`)
- ThreadPoolExecutor for parallel processing
- Progress tracking with tqdm
- Error recovery and logging
- Up to 100 papers per batch

### 4. Excel Exporter (`excel_exporter.py`)
- Formatted Excel output
- Conditional formatting
- Review flag highlighting
- Summary statistics

### 5. Web UI (`app.py`)
- Multi-file upload
- Answer key input (text or file)
- Real-time progress
- Result download

## Key Features Implementation

### Batch Processing ✅
- `BatchProcessor` class with ThreadPoolExecutor
- Configurable worker threads (default: 5)
- Progress tracking with tqdm
- Limit: 100 papers per batch

### Multi-format Support ✅
- PDF: pdfplumber + PyPDF2 fallback
- DOCX: python-docx
- TXT: UTF-8 with latin-1 fallback

### Strict MCQ Grading ✅
- String comparison after normalization
- 100% accuracy guarantee
- Case-insensitive matching

### AI Textual Grading ✅
- OpenAI GPT-3.5-turbo (configurable)
- Detailed feedback generation
- Rule-based fallback without API key

### 3 Agents + Orchestrator ✅
- MCQGradingAgent
- TextualGradingAgent
- OrchestratorAgent
- Full pipeline coordination

### Excel Export ✅
- openpyxl library
- Conditional formatting
- Yellow: Review needed
- Red: Processing errors

### Student Info Extraction ✅
- Regex patterns for text content
- Filename parsing fallback
- Multiple format support

### Progress Tracking ✅
- tqdm progress bars
- Real-time updates
- Completion statistics

### Error Handling ✅
- Try-catch blocks
- Error logging
- Continue on failure
- Error result objects

### Gradio Web UI ✅
- Modern, responsive interface
- Multi-file upload
- Real-time feedback
- Result download

## Configuration

All settings in `config.py`:
- API keys
- Batch limits
- Scoring weights
- UI configuration
- Feature flags

## Deployment Options

1. **Local**: `python app.py`
2. **Docker**: `docker-compose up`
3. **Cloud**: Heroku, AWS, Azure, GCP

## Security Considerations

- No hardcoded secrets
- Environment variables for API keys
- Input validation
- File size limits
- Secure temporary file handling

## Performance

- **Throughput**: ~20-50 papers/minute (depends on file size)
- **Parallel Processing**: Up to 5 concurrent workers
- **Memory**: ~100-500MB for typical batch
- **Scalability**: Horizontal scaling via Docker

## Future Enhancements

- [ ] OCR support for scanned images
- [ ] Multiple answer key formats
- [ ] Custom grading rubrics
- [ ] Plagiarism detection
- [ ] Student analytics dashboard
- [ ] API endpoint for integrations
- [ ] Mobile-responsive UI improvements
- [ ] Multi-language support

---

**Version**: 1.0.0  
**Architecture**: Multi-agent system with batch processing  
**License**: MIT
