# Quick Reference Guide - AI Paper Checker

## 🚀 Quick Commands

### Setup
```bash
./setup.sh                    # Automated setup
source venv/bin/activate      # Activate virtual environment
```

### Run
```bash
python app.py                 # Start web UI
python test_system.py         # Run tests
python validate_structure.py  # Validate code structure
```

### Docker
```bash
docker-compose up             # Start with Docker
docker-compose up -d          # Start in background
docker-compose down           # Stop
```

## 📋 File Formats

### Student Papers
- **PDF**: `.pdf` (scanned or text-based)
- **Word**: `.docx` (Microsoft Word)
- **Text**: `.txt` (plain text)

### Answer Keys
```
1. A
2. B
3. C
```

## 🎯 Student Info Format

Papers should include:
```
Name: John Doe
Student ID: 12345
Roll No: CS101
```

Or use filename: `JohnDoe_12345.pdf`

## 📊 Output

Results exported to Excel with:
- Student information
- MCQ scores
- Textual scores
- Review flags
- Detailed feedback
- Color-coded highlighting

## ⚙️ Configuration

### Environment Variables
```bash
export OPENAI_API_KEY="sk-..."  # For AI grading
```

### Config File
Edit `config.py` for:
- Batch size (default: 100)
- Worker threads (default: 5)
- Scoring weights
- UI settings

## 🔧 Troubleshooting

### Issue: Dependencies fail to install
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Issue: Port 7860 already in use
Edit `config.py`:
```python
UI_SERVER_PORT = 8080  # Change to different port
```

### Issue: File extraction fails
- Ensure file isn't corrupted
- Try different format (convert to PDF/TXT)
- Check file permissions

### Issue: Low AI grading quality
- Use GPT-4 model instead of GPT-3.5
- Provide reference answers
- Adjust prompts in `agents.py`

## 📈 Best Practices

### Paper Preparation
1. Ensure student info is clearly labeled
2. Use consistent MCQ format (1. A, 2. B, etc.)
3. Keep file sizes reasonable (<10MB)
4. Use clear, readable fonts

### Answer Keys
1. Double-check correct answers
2. Use consistent format
3. Number questions sequentially
4. Test with sample papers first

### Batch Processing
1. Start with small batches (10-20 papers)
2. Verify results before large batches
3. Review flagged papers manually
4. Keep backup of original papers

### Grading Quality
1. Use AI grading for best results (set API key)
2. Provide reference answers for textual questions
3. Review low-scoring papers
4. Adjust scoring weights if needed

## 🎓 Example Workflow

1. **Prepare Papers**
   - Collect student submissions
   - Ensure consistent format
   - Create answer key

2. **Upload & Process**
   - Open web UI (http://localhost:7860)
   - Upload papers (max 100)
   - Paste/upload answer key
   - Click "Process Papers"

3. **Review Results**
   - Download Excel file
   - Review flagged papers
   - Check error logs
   - Verify scores

4. **Final Grading**
   - Make manual adjustments if needed
   - Export final grades
   - Archive results

## 📞 Support

- **Documentation**: See README.md
- **Issues**: GitHub Issues
- **Contributing**: See CONTRIBUTING.md
- **Examples**: Check examples/ directory

## 🔗 Useful Links

- [Gradio Documentation](https://gradio.app/docs)
- [OpenAI API](https://platform.openai.com/docs)
- [Project Repository](https://github.com/RexLapis1504/jiaoshi)

---

**Version**: 1.0.0  
**Last Updated**: November 2024
