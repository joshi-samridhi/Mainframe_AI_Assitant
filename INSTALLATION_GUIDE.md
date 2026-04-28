# 📖 Step-by-Step Installation Guide

This guide will walk you through setting up and running the Mainframe AI Support Assistant on Windows.

## Prerequisites

Before starting, ensure you have:
- Windows 10 or 11
- Internet connection
- Administrator access (for Python installation)

---

## Step 1: Install Python

### Check if Python is Already Installed

1. Press `Windows + R` to open Run dialog
2. Type `cmd` and press Enter
3. In the Command Prompt, type:
   ```
   python --version
   ```
4. If you see `Python 3.7` or higher, skip to Step 2
5. If you see an error, continue with Python installation below

### Install Python (if needed)

1. Go to https://www.python.org/downloads/
2. Click the yellow "Download Python" button
3. Run the downloaded installer
4. **IMPORTANT**: Check the box "Add Python to PATH" at the bottom
5. Click "Install Now"
6. Wait for installation to complete
7. Click "Close"

### Verify Python Installation

1. Open a NEW Command Prompt (close old one)
2. Type:
   ```
   python --version
   ```
3. You should see: `Python 3.x.x`

---

## Step 2: Navigate to Project Directory

### Option A: Using File Explorer + Command Prompt

1. Open File Explorer
2. Navigate to: `C:\Users\SamridhiJoshi\Desktop\mainframe-error-screens`
3. Click in the address bar at the top
4. Type `cmd` and press Enter
5. A Command Prompt will open in that directory

### Option B: Using Command Prompt Directly

1. Press `Windows + R`
2. Type `cmd` and press Enter
3. Type the following command:
   ```
   cd C:\Users\SamridhiJoshi\Desktop\mainframe-error-screens
   ```
4. Press Enter

### Verify You're in the Right Directory

Type:
```
dir
```

You should see files like:
- app.py
- config.py
- requirements.txt
- README_APP.md

---

## Step 3: Install Dependencies

In the Command Prompt (in the project directory), type:

```
pip install -r requirements.txt
```

Press Enter and wait. You'll see:
```
Collecting Flask>=3.0.0
Collecting Flask-Login>=0.6.3
...
Successfully installed Flask-3.0.0 Flask-Login-0.6.3 ...
```

This may take 2-5 minutes depending on your internet speed.

### If You Get an Error

**Error: "pip is not recognized"**
- Try: `python -m pip install -r requirements.txt`

**Error: "Permission denied"**
- Run Command Prompt as Administrator:
  - Press `Windows + X`
  - Click "Command Prompt (Admin)" or "PowerShell (Admin)"
  - Navigate to project directory again
  - Retry the command

---

## Step 4: Create Environment File

### Using Command Prompt

Type:
```
copy .env.example .env
```

Press Enter. You should see:
```
1 file(s) copied.
```

### Using File Explorer (Alternative)

1. Open File Explorer
2. Navigate to `mainframe-error-screens` folder
3. Find `.env.example` file
4. Right-click → Copy
5. Right-click in empty space → Paste
6. Rename the copy to `.env` (remove `.example`)

### Edit .env File (Optional)

1. Right-click `.env` file
2. Open with Notepad
3. Change `FLASK_SECRET_KEY` to something random (optional)
4. Save and close

**Note**: For basic testing, you can skip editing the .env file. The defaults will work.

---

## Step 5: Run the Application

In the Command Prompt (in project directory), type:

```
python app.py
```

Press Enter. You should see:
```
 * Serving Flask app 'app'
 * Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment.
 * Running on http://127.0.0.1:5000
Press CTRL+C to quit
```

**Important**: Keep this Command Prompt window open! The application is running.

### If You Get an Error

**Error: "Address already in use"**
- Another program is using port 5000
- Solution: Edit `app.py`, change the last line to:
  ```python
  app.run(debug=True, host='0.0.0.0', port=5001)
  ```
- Then use `http://localhost:5001` instead

**Error: "ModuleNotFoundError"**
- Dependencies not installed properly
- Go back to Step 3 and reinstall

---

## Step 6: Open in Browser

### Method 1: Click the Link
1. In the Command Prompt, hold `Ctrl` and click on `http://127.0.0.1:5000`

### Method 2: Manual Entry
1. Open your web browser (Chrome, Edge, Firefox)
2. In the address bar, type:
   ```
   http://localhost:5000
   ```
3. Press Enter

### What You Should See

You should see the **Login Page** with:
- Green text on dark background
- "⚡ MAINFRAME AI SUPPORT" header
- Username/Email and Password fields
- "Register here" link

---

## Step 7: Create Your Account

### Register

1. Click **"Register here"** link
2. Fill in the form:
   - **Username**: Choose any username (min 3 characters)
   - **Email**: Enter your email
   - **Full Name**: Your name (optional)
   - **Password**: Choose a password (min 8 characters)
   - **Confirm Password**: Re-enter the same password
3. Click **"REGISTER"** button
4. You'll see: "Registration successful! Please log in."

### Login

1. Enter your username (or email) and password
2. Click **"LOGIN"** button
3. You'll be redirected to the Dashboard

---

## Step 8: Test the Application

### Quick Test with Sample Log

1. Click **"New Analysis"** in the navigation
2. In the text area, paste this sample log:
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
3. Click **"ANALYZE LOG"** button
4. Review the extracted information
5. Click **"YES - Show Resolution"**
6. View the annotated error screen and resolution steps
7. Click on any INC number (e.g., INC12345) to see incident details

---

## Stopping the Application

When you're done:

1. Go to the Command Prompt window where the app is running
2. Press `Ctrl + C`
3. You'll see: `Keyboard interrupt received, exiting.`
4. The application has stopped

---

## Restarting the Application

To run it again later:

1. Open Command Prompt
2. Navigate to project directory:
   ```
   cd C:\Users\SamridhiJoshi\Desktop\mainframe-error-screens
   ```
3. Run:
   ```
   python app.py
   ```
4. Open browser to `http://localhost:5000`

---

## Common Issues & Solutions

### Issue: "Python is not recognized"
**Solution**: 
- Reinstall Python and check "Add Python to PATH"
- Or use full path: `C:\Python39\python.exe app.py`

### Issue: "No module named 'flask'"
**Solution**: 
- Run: `pip install -r requirements.txt`
- Or: `python -m pip install -r requirements.txt`

### Issue: "Port 5000 is already in use"
**Solution**: 
- Change port in `app.py` to 5001
- Or stop other programs using port 5000

### Issue: "Can't see .env file"
**Solution**: 
- In File Explorer, click View → Show → File name extensions
- Then you can see and edit `.env`

### Issue: "Database error"
**Solution**: 
- Delete `instance/mainframe_assistant.db`
- Restart the application (it will recreate the database)

### Issue: "Browser shows 'Can't reach this page'"
**Solution**: 
- Check if app is running (Command Prompt should show "Running on...")
- Try `http://127.0.0.1:5000` instead of `localhost`
- Check firewall settings

---

## Optional: Install Tesseract OCR

For image-based log analysis (optional):

1. Download from: https://github.com/UB-Mannheim/tesseract/wiki
2. Run installer
3. Install to: `C:\Program Files\Tesseract-OCR\`
4. Edit `.env` file:
   ```
   TESSERACT_PATH=C:/Program Files/Tesseract-OCR/tesseract.exe
   ```
5. Restart the application

---

## Optional: Add OpenAI API Key

For AI-powered log analysis (optional):

1. Get API key from: https://platform.openai.com/api-keys
2. Edit `.env` file:
   ```
   OPENAI_API_KEY=sk-your-key-here
   ```
3. Restart the application

---

## Video Tutorial Alternative

If you prefer video instructions, search YouTube for:
- "How to install Python on Windows"
- "How to run Flask application"
- "Python pip install tutorial"

---

## Need Help?

1. Check the error message in Command Prompt
2. Read `README_APP.md` for detailed documentation
3. Review `QUICKSTART.md` for quick reference
4. Check if all files are in the correct directory

---

## Summary of Commands

```bash
# Navigate to project
cd C:\Users\SamridhiJoshi\Desktop\mainframe-error-screens

# Install dependencies
pip install -r requirements.txt

# Create .env file
copy .env.example .env

# Run application
python app.py

# Stop application
Ctrl + C
```

---

**🎉 Congratulations! You're ready to use the Mainframe AI Support Assistant!**