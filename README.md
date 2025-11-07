# 📝 Jiaoshi - AI Paper Checker

Complete MVP for AI-powered paper grading system with multi-agent architecture.

## ✨ Features

### What's Included - Complete MVP
- ✅ **Batch Processing** - Grade up to 100 papers at once
- 📄 **Multi-format Support** - PDF, DOCX, TXT
- 🎯 **Strict MCQ Grading** - 100% accuracy on answer key
- 🤖 **Textual Answer Grading** - AI-powered with feedback
- 🔧 **3 Agents + Orchestrator** - Full multi-agent pipeline
- 📊 **Excel Export** - Formatted with review flags
- 🔍 **Student Info Extraction** - From text + filename
- ⚡ **Progress Tracking** - Real-time progress bars
- 🛡️ **Error Handling** - Robust error recovery
- 🌐 **Gradio Web UI** - Beautiful frontend interface

## 🏗️ Architecture

The system uses a multi-agent architecture:

1. **MCQ Grading Agent** - Strict comparison against answer key for 100% accuracy
2. **Textual Grading Agent** - AI-powered grading with detailed feedback
3. **Orchestrator Agent** - Coordinates workflow and combines results

## 🚀 Quick Start

### Option 1: Automated Setup (Recommended)

```bash
# Clone the repository
git clone https://github.com/RexLapis1504/jiaoshi.git
cd jiaoshi

# Run setup script
./setup.sh

# Activate virtual environment
source venv/bin/activate

# Start the application
python app.py
```

### Option 2: Docker

```bash
# Clone the repository
git clone https://github.com/RexLapis1504/jiaoshi.git
cd jiaoshi

# Set API key (optional)
export OPENAI_API_KEY="your-api-key-here"

# Run with Docker Compose
docker-compose up
```

### Option 3: Manual Installation

```bash
# Clone the repository
git clone https://github.com/RexLapis1504/jiaoshi.git
cd jiaoshi

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set OpenAI API key (optional, for AI grading)
export OPENAI_API_KEY="your-api-key-here"

# Launch the web UI
python app.py
```

The application will be available at `http://localhost:7860`

### Without OpenAI API Key

The system works without an API key using rule-based grading as fallback:
```bash
python app.py
```

## 📖 Usage Guide

### 1. Prepare Your Papers

Supported formats:
- **PDF** - Scanned or text-based
- **DOCX** - Microsoft Word documents  
- **TXT** - Plain text files

Student information can be included in:
- Document content: `Name: John Doe`, `Student ID: 12345`
- Filename: `JohnDoe_12345.pdf`

### 2. Create Answer Key

For MCQ grading, provide answer key in format:
```
1. A
2. B
3. C
4. D
5. A
```

Or:
```
Q1: A
Q2: B
Q3: C
```

### 3. Process Papers

1. Upload papers (max 100)
2. Provide answer key
3. Click "Process Papers"
4. Download Excel results

### 4. Review Results

The Excel file includes:
- Student information
- MCQ scores and incorrect answers
- Textual scores and feedback
- Review flags for papers needing attention
- Color-coded highlighting

## 🧪 Testing

Run the test script to verify installation:

```bash
python test_system.py
```

This will:
- Create sample papers
- Process them through the system
- Generate test results
- Verify all components work

## 📁 Project Structure

```
jiaoshi/
├── app.py                  # Main Gradio web UI
├── agents.py              # MCQ, Textual, and Orchestrator agents
├── document_utils.py      # Document processing utilities
├── batch_processor.py     # Batch processing engine
├── excel_exporter.py      # Excel export functionality
├── requirements.txt       # Python dependencies
├── test_system.py         # Test script
└── README.md             # This file
```

## 🔧 Configuration

### Environment Variables

- `OPENAI_API_KEY` - OpenAI API key for AI grading (optional)

### Customization

Edit these parameters in the code:

- **Batch size limit**: Change `max_papers` in `BatchProcessor` (default: 100)
- **Worker threads**: Change `max_workers` in `BatchProcessor` (default: 5)
- **AI model**: Change `model` in `TextualGradingAgent` (default: gpt-3.5-turbo)
- **Grading weights**: Modify scoring logic in `OrchestratorAgent`

## 📊 Output Format

Excel file includes:

| Column | Description |
|--------|-------------|
| Student Name | Extracted from document/filename |
| Student ID | Unique identifier |
| Roll No | Roll number |
| MCQ Score | Score out of total (e.g., 8/10) |
| MCQ Percentage | Percentage score |
| MCQ Incorrect | List of incorrect question numbers |
| Textual Score | Score for subjective answers |
| Total Score | Combined final score |
| Needs Review | YES/NO flag |
| Review Reason | Why flagged for review |
| Feedback | Detailed feedback for textual answers |
| Error | Any processing errors |

## 🚨 Error Handling

The system handles:
- **Invalid file formats** - Skip and report
- **Corrupted files** - Error recovery and logging
- **Missing student info** - Extract from filename
- **Empty answers** - Mark as 0 and flag for review
- **Batch failures** - Continue processing remaining papers

Papers with issues are automatically flagged for manual review.

## 🚀 Deployment

### Local Development
```bash
python app.py
```

### Production with Docker
```bash
docker-compose up -d
```

### Cloud Deployment

#### Heroku
```bash
# Create Heroku app
heroku create your-app-name

# Set environment variables
heroku config:set OPENAI_API_KEY=your-api-key

# Deploy
git push heroku main
```

#### AWS/Azure/GCP
Use the provided Dockerfile for container-based deployment:
```bash
docker build -t jiaoshi .
docker run -p 7860:7860 -e OPENAI_API_KEY=your-key jiaoshi
```

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📝 License

MIT License - See LICENSE file for details

## 🙏 Acknowledgments

Built with:
- [Gradio](https://gradio.app/) - Web UI framework
- [OpenAI](https://openai.com/) - AI grading capabilities
- [pandas](https://pandas.pydata.org/) - Data processing
- [openpyxl](https://openpyxl.readthedocs.io/) - Excel export

## 📧 Support

For issues or questions:
- Open an issue on GitHub
- Contact: [Your contact info]

---

Made with ❤️ for educators and students
