# Sample Mainframe Logs for Testing

This directory contains sample mainframe error logs that you can use to test the Mainframe AI Support Assistant application.

## 📁 Available Sample Logs

### 1. **sample_log_S0C7.txt** - Data Exception Error
- **JOBNAME**: PAYBATCH
- **JOBID**: JOB12345
- **ERROR CODE**: S0C7
- **STEP**: STEP010
- **DESCRIPTION**: System detected a data exception - typically caused by invalid numeric data
- **USE CASE**: Test numeric data validation errors

**How to use:**
1. Copy the entire content of this file
2. Go to http://localhost:5000/analyze
3. Paste into the "Log Text" field
4. Click "Analyze Log"

---

### 2. **sample_log_S013.txt** - Dataset Open Error
- **JOBNAME**: FILEBATCH
- **JOBID**: JOB98765
- **ERROR CODE**: S013
- **STEP**: STEP005
- **DESCRIPTION**: Unable to allocate dataset - file access or allocation issue
- **USE CASE**: Test file/dataset access errors

**How to use:**
1. Copy the entire content of this file
2. Go to http://localhost:5000/analyze
3. Paste into the "Log Text" field
4. Click "Analyze Log"

---

### 3. **sample_log_S806.txt** - Load Module Not Found
- **JOBNAME**: LOADBATCH
- **JOBID**: JOB54321
- **ERROR CODE**: S806
- **STEP**: STEP003
- **DESCRIPTION**: Module not found - missing program or library
- **USE CASE**: Test module/program loading errors

**How to use:**
1. Copy the entire content of this file
2. Go to http://localhost:5000/analyze
3. Paste into the "Log Text" field
4. Click "Analyze Log"

---

## 🖼️ Sample Error Screen Images

Error screen images are available in the `output/` directory:
- **U0777_error_screen.png** - Data validation error screen
- **S013_error_screen.png** - Dataset open error screen
- **S0C7_error_screen.png** - Data exception error screen

**How to use images:**
1. Go to http://localhost:5000/analyze
2. Click "Choose File" under "Upload Error Screen Image"
3. Select one of the PNG files from the `output/` directory
4. Click "Analyze Log"
5. The OCR will extract text from the image

---

## 🎯 Testing Workflow

### Complete Test Scenario:

1. **Login**
   - Go to http://localhost:5000
   - Username: `admin`
   - Password: `admin123`

2. **Analyze a Log (Text)**
   - Click "Analyze New Log" from dashboard
   - Copy content from `sample_log_S0C7.txt`
   - Paste into the text area
   - Click "Analyze Log"

3. **View Results**
   - See extracted information (JOBNAME, JOBID, STATUS, etc.)
   - Click "Yes" when asked about resolution

4. **View Resolution**
   - See the error resolution and steps to fix
   - View the annotated error screen image
   - Click "Yes" to see previous INC records

5. **Browse INC History**
   - Click on INC numbers (INC12345, INC98765, etc.)
   - View detailed resolution history

6. **Test Image Upload**
   - Go back to "Analyze New Log"
   - Upload `S013_error_screen.png` from output folder
   - See OCR extract the text automatically

---

## 📊 Expected Extraction Results

### For sample_log_S0C7.txt:
```
JOBNAME: PAYBATCH
JOBID: JOB12345
STATUS: ABEND
RETURN CODE: S0C7
STEP: STEP010
ERROR: CEE3204S The system detected a data exception
```

### For sample_log_S013.txt:
```
JOBNAME: FILEBATCH
JOBID: JOB98765
STATUS: ABEND
RETURN CODE: S013
STEP: STEP005
ERROR: IEC141I 013-18 UNABLE TO ALLOCATE
```

### For sample_log_S806.txt:
```
JOBNAME: LOADBATCH
JOBID: JOB54321
STATUS: ABEND
RETURN CODE: S806
STEP: STEP003
ERROR: CEE3501S The module CUSTPROG was not found
```

---

## 💡 Tips

1. **Text vs Image**: Text analysis is faster, but image upload tests the OCR functionality
2. **Multiple Tests**: Try all three sample logs to see different error types
3. **INC History**: Each error code links to different previous incidents
4. **Analysis History**: Check your dashboard to see all previous analyses
5. **Custom Logs**: You can create your own mainframe logs following the same format

---

## 🔧 Troubleshooting

**If extraction fails:**
- Make sure the log contains the required fields (JOBNAME, JOBID, etc.)
- Check that error codes are in the format S0C7, S013, S806, etc.
- Verify the log follows standard mainframe JCL output format

**If image upload fails:**
- Ensure Tesseract OCR is installed (optional for basic testing)
- Use the pre-generated images in the `output/` folder
- Images should be clear and readable

---

## 📝 Creating Your Own Sample Logs

To create custom test logs, follow this structure:

```
IEF236I ALLOC. FOR [JOBNAME] [JOBID]
IEF237I JES2 ALLOCATED TO SYSOUT
IEF142I [JOBNAME] [STEP] - STEP WAS EXECUTED - COND CODE 0000
[Error message here]
IEF450I [JOBNAME] [STEP] - ABEND=[ERROR_CODE] U0000 REASON=00000000
IEF472I [JOBNAME] [STEP] - COMPLETION CODE - SYSTEM=[ERROR_CODE]
```

Replace:
- `[JOBNAME]` with your job name
- `[JOBID]` with job ID (e.g., JOB12345)
- `[STEP]` with step name (e.g., STEP001)
- `[ERROR_CODE]` with error code (e.g., S0C7, S013, S806)

---

**Happy Testing! 🚀**