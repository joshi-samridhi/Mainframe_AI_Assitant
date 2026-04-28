# Mainframe AI Support Assistant

A comprehensive web-based tool for analyzing mainframe logs, providing visual debugging support, and tracking incident resolutions.

## 🌟 Features

### Core Functionality
- **Multi-Method Log Analysis**: Rule-based regex extraction with AI fallback
- **OCR Support**: Extract text from terminal screenshots using Tesseract
- **Visual Debugging**: Automatically generated annotated error screen images
- **Knowledge Base**: Comprehensive error code database with resolutions
- **Incident Tracking**: View previous INC records for similar issues
- **User Authentication**: Secure multi-user support with session management
- **Analysis History**: Track all your log analyses with full history

### Supported Error Codes
- **U0777** - Data Validation Abend
- **S013** - Dataset Open Error
- **S0C7** - Numeric Data Exception
- **S0C4** - Protection Exception
- **S0C1** - Operation Exception
- **S322** - Time-Out
- **S806** - Program Not Found
- **S222** - Job Cancelled

## 📋 Prerequisites

- **Python 3.7+**
- **Tesseract OCR** (optional, for image processing)
- **OpenAI API Key** (optional, for AI fallback)

## 🚀 Installation

### Step 1: Clone or Navigate to Project Directory

```bash
cd mainframe-error-screens
```

### Step 2: Create Virtual Environment (Recommended)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Install Tesseract OCR (Optional)

**Windows:**
1. Download from: https://github.com/UB-Mannheim/tesseract/wiki
2. Install to: `C:\Program Files\Tesseract-OCR\`
3. Add to PATH or update `.env` file

**Linux:**
```bash
sudo apt-get install tesseract-ocr
```

**Mac:**
```bash
brew install tesseract
```

### Step 5: Configure Environment Variables

Copy the example environment file:
```bash
copy .env.example .env  # Windows
cp .env.example .env    # Linux/Mac
```

Edit `.env` file:
```env
# Flask Configuration
FLASK_SECRET_KEY=your-secret-key-here-change-this
FLASK_ENV=development

# Database Configuration
DATABASE_URI=sqlite:///instance/mainframe_assistant.db

# OpenAI API Configuration (Optional)
OPENAI_API_KEY=your-openai-api-key-here

# Tesseract OCR Path
TESSERACT_PATH=C:/Program Files/Tesseract-OCR/tesseract.exe
```

### Step 6: Initialize Database

The database will be automatically created on first run. Sample INC records are pre-populated.

## 🎯 Usage

### Starting the Application

```bash
python app.py
```

The application will start on `http://localhost:5000`

### First Time Setup

1. **Register an Account**
   - Navigate to `http://localhost:5000`
   - Click "Register here"
   - Fill in username, email, and password
   - Click "REGISTER"

2. **Login**
   - Enter your username/email and password
   - Click "LOGIN"

### Workflow

#### STEP 1: Extract Information

1. Go to **New Analysis** from dashboard
2. Choose input method:
   - **Upload File**: Select a text file (.txt, .log) or image (.png, .jpg)
   - **Paste Content**: Copy and paste log content directly
3. Click **ANALYZE LOG**
4. Review extracted information:
   - JOBNAME
   - JOBID
   - STATUS
   - RETURN CODE
   - STEP
   - ERROR

#### STEP 2: View Resolution

1. Click **YES - Show Resolution**
2. Review:
   - Error code description
   - Annotated error screen image
   - Common causes
   - Step-by-step resolution
   - Prevention tips

#### STEP 3: Check Previous INCs

1. View related incident numbers (e.g., INC12345)
2. Click on any INC number
3. Review:
   - Problem description
   - Resolution steps followed
   - Timeline and resolution time

## 📁 Project Structure

```
mainframe-error-screens/
├── app.py                      # Main Flask application
├── config.py                   # Configuration settings
├── requirements.txt            # Python dependencies
├── .env                        # Environment variables (create from .env.example)
├── generate_error_screens.py  # Error screen generator
│
├── modules/                    # Application modules
│   ├── __init__.py
│   ├── models.py              # Database models
│   ├── log_extractor.py       # Log parsing logic
│   ├── ocr_processor.py       # OCR handling
│   ├── ai_fallback.py         # OpenAI integration
│   └── knowledge_base.py      # Error code resolutions
│
├── templates/                  # HTML templates
│   ├── base.html
│   ├── dashboard.html
│   ├── index.html             # Analysis form
│   ├── result.html            # Extraction results
│   ├── resolution.html        # Resolution display
│   ├── inc_detail.html        # INC detail page
│   ├── history.html
│   └── auth/
│       ├── login.html
│       ├── register.html
│       └── profile.html
│
├── static/                     # Static files
│   ├── css/
│   │   └── style.css          # Main stylesheet
│   └── js/
│
├── data/                       # Data files
│   └── error_codes.json       # Error code database
│
├── instance/                   # Instance folder
│   └── mainframe_assistant.db # SQLite database
│
├── uploads/                    # User uploads
├── output/                     # Generated images
└── README_APP.md              # This file
```

## 🔧 Configuration

### Flask Settings

Edit `config.py` to modify:
- Secret key
- Database URI
- Session timeout
- File upload limits
- Allowed file extensions

### Error Codes

Add new error codes to `data/error_codes.json`:

```json
{
  "ERROR_CODE": {
    "name": "Error Name",
    "description": "Detailed description",
    "common_causes": ["Cause 1", "Cause 2"],
    "resolution_steps": ["Step 1", "Step 2"],
    "prevention": ["Tip 1", "Tip 2"]
  }
}
```

## 🎨 Features in Detail

### Rule-Based Extraction
- Uses regex patterns to extract information
- Fast and reliable for standard log formats
- No external API required

### OCR Processing
- Extracts text from terminal screenshots
- Automatic preprocessing for better accuracy
- Supports multiple image formats

### AI Fallback
- Activates when regex confidence is low
- Uses OpenAI GPT-3.5 for intelligent extraction
- Requires API key (optional)

### Visual Debugging
- Automatically generates annotated error screens
- Highlights error areas with boxes and arrows
- Includes resolution checklist

### User Management
- Secure password hashing with bcrypt
- Session management with Flask-Login
- User-specific analysis history

## 📊 Database Schema

### Users Table
- id, username, email, password_hash
- full_name, created_at, last_login

### Analysis History Table
- id, user_id, jobname, jobid, status
- return_code, step, error_message
- log_content, image_path, annotated_image_path
- extraction_method, created_at

### INC Records Table
- id, inc_number, error_code
- jobname, description, resolution
- status, created_by, created_at, resolved_at

## 🔒 Security

- Passwords hashed with bcrypt
- CSRF protection with Flask-WTF
- Session cookies with secure settings
- SQL injection prevention (SQLAlchemy ORM)
- XSS protection (Jinja2 auto-escaping)
- File upload validation

## 🐛 Troubleshooting

### Database Issues
```bash
# Delete and recreate database
rm instance/mainframe_assistant.db
python app.py
```

### Tesseract Not Found
- Verify installation path
- Update `TESSERACT_PATH` in `.env`
- Add to system PATH

### OpenAI API Errors
- Verify API key in `.env`
- Check API quota and billing
- AI fallback is optional

### Port Already in Use
```bash
# Change port in app.py
app.run(debug=True, host='0.0.0.0', port=5001)
```

## 📝 API Endpoints

- `GET /` - Home (redirects to login/dashboard)
- `GET/POST /register` - User registration
- `GET/POST /login` - User login
- `GET /logout` - User logout
- `GET /dashboard` - User dashboard
- `GET/POST /analyze` - Log analysis form
- `GET /result/<id>` - Analysis results
- `GET /resolution/<id>` - Resolution display
- `GET /inc/<number>` - INC detail page
- `GET /history` - Analysis history
- `GET /profile` - User profile

## 🚀 Deployment

### Development
```bash
python app.py
```

### Production (with Gunicorn)
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Docker (Optional)
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "app.py"]
```

## 📄 License

This project is provided as-is for educational and training purposes.

## 🤝 Support

For issues or questions:
1. Check the troubleshooting section
2. Review error logs in console
3. Verify configuration in `.env`

## 🎯 Future Enhancements

- [ ] Email notifications
- [ ] Export to PDF
- [ ] Batch log processing
- [ ] Advanced search and filtering
- [ ] Role-based access control
- [ ] REST API for programmatic access
- [ ] Integration with mainframe systems
- [ ] Real-time log monitoring

---

**Made with ❤️ for Mainframe Engineers**