# 🚀 Quick Start Guide

Get the Mainframe AI Support Assistant running in 5 minutes!

## Prerequisites Check

- [ ] Python 3.7+ installed
- [ ] pip package manager available
- [ ] (Optional) Tesseract OCR for image processing
- [ ] (Optional) OpenAI API key for AI fallback

## Installation Steps

### 1. Navigate to Project Directory
```bash
cd mainframe-error-screens
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Create Environment File
```bash
# Windows
copy .env.example .env

# Linux/Mac
cp .env.example .env
```

### 4. Edit .env File (Optional)
```env
FLASK_SECRET_KEY=change-this-to-something-secure
OPENAI_API_KEY=your-key-here  # Optional
TESSERACT_PATH=C:/Program Files/Tesseract-OCR/tesseract.exe  # If installed
```

### 5. Run the Application
```bash
python app.py
```

### 6. Open Browser
Navigate to: **http://localhost:5000**

## First Time Usage

### Register Account
1. Click **"Register here"**
2. Enter:
   - Username (min 3 characters)
   - Email
   - Password (min 8 characters)
   - Full Name (optional)
3. Click **"REGISTER"**

### Login
1. Enter username/email and password
2. Click **"LOGIN"**

### Analyze Your First Log

#### Option 1: Paste Log Content
1. Click **"New Analysis"**
2. Paste this sample log:
```
JOBNAME: DUMMYBATCH01
JOBID: 12345
STATUS: ABEND
RETURN CODE: U0777
STEP: STEP002
ERROR: DATA VALIDATION FAILED

Job Log:
Invalid record RECORD#007, STEP002 ended abnormally
```
3. Click **"ANALYZE LOG"**

#### Option 2: Upload File
1. Click **"New Analysis"**
2. Click **"Choose File"**
3. Select a .txt, .log, or image file
4. Click **"ANALYZE LOG"**

### View Results
1. Review extracted information
2. Click **"YES - Show Resolution"**
3. View annotated error screen
4. Check resolution steps
5. Click on INC numbers to see previous incidents

## Sample Test Data

### Test Log 1: U0777 Error
```
JOBNAME: DUMMYBATCH01
JOBID: 12345
STATUS: ABEND
RETURN CODE: U0777
STEP: STEP002
ERROR: DATA VALIDATION FAILED
```

### Test Log 2: S013 Error
```
JOBNAME: FILEBATCH05
JOBID: 67890
STATUS: ABEND
RETURN CODE: S013
STEP: STEP005
ERROR: DATASET OPEN ERROR (DCB / RECFM MISMATCH)
```

### Test Log 3: S0C7 Error
```
JOBNAME: CALCBATCH10
JOBID: 11111
STATUS: ABEND
RETURN CODE: S0C7
STEP: STEP010
ERROR: DATA EXCEPTION
```

## Features to Try

### 1. Dashboard
- View statistics
- See recent analyses
- Check common error codes

### 2. Analysis History
- View all past analyses
- Filter and search
- Re-open previous results

### 3. Profile
- View account information
- Check usage statistics
- See recent activity

### 4. INC Records
- Click on INC numbers (e.g., INC12345)
- View resolution history
- See timeline and resolution time

## Troubleshooting

### Application Won't Start
```bash
# Check Python version
python --version  # Should be 3.7+

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### Can't Login
- Verify you registered an account
- Check username/email spelling
- Password is case-sensitive

### No Resolution Shown
- Ensure error code was extracted
- Check if error code is supported
- Try a different log format

### OCR Not Working
- Install Tesseract OCR
- Update TESSERACT_PATH in .env
- Try with text input instead

## Next Steps

1. **Explore Features**: Try all three workflow steps
2. **Test Different Logs**: Upload various error logs
3. **Check Documentation**: Read README_APP.md for details
4. **Customize**: Add your own error codes to data/error_codes.json
5. **Configure**: Set up OpenAI API for AI fallback

## Support

- 📖 Full Documentation: `README_APP.md`
- 🐛 Issues: Check console for error messages
- ⚙️ Configuration: Review `config.py` and `.env`

## Default Credentials

No default credentials - you must register a new account on first use.

## Port Already in Use?

Change the port in `app.py`:
```python
app.run(debug=True, host='0.0.0.0', port=5001)  # Change 5000 to 5001
```

---

**🎉 You're all set! Start analyzing mainframe logs now!**