# Mainframe AI Support Assistant

A Flask-based web application for analyzing mainframe error logs using OCR and AI-powered analysis.

## Features

- 🔐 User authentication (login/register)
- 📸 OCR support for screenshot analysis
- 🤖 AI-powered error code detection
- 📊 Analysis history tracking
- 🎯 Error resolution suggestions
- 📝 INC (Incident) record management

## Prerequisites

- Python 3.8 or higher
- Tesseract OCR (optional, for image analysis)
- Git

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/mainframe-error-screens.git
cd mainframe-error-screens
```

### 2. Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment

```bash
# Copy the example environment file
copy .env.example .env    # Windows
cp .env.example .env      # Linux/Mac

# Edit .env file and update:
# - FLASK_SECRET_KEY (generate a random secret key)
# - TESSERACT_PATH (if using OCR features)
# - OPENAI_API_KEY (optional, for AI features)
```

### 5. Run the Application

```bash
python app.py
```

The application will be available at `http://localhost:5000`

## Default Login

- **Username:** `admin`
- **Password:** `admin123`

⚠️ **Important:** Change the default admin password after first login!

## Project Structure

```
mainframe-error-screens/
├── app.py                 # Main Flask application
├── config.py             # Configuration settings
├── requirements.txt      # Python dependencies
├── .env                  # Environment variables (not in git)
├── .env.example         # Example environment file
├── modules/             # Application modules
│   ├── models.py        # Database models
│   ├── ocr_processor.py # OCR functionality
│   ├── ai_fallback.py   # AI integration
│   └── knowledge_base.py # Error code database
├── templates/           # HTML templates
├── static/             # CSS, JS, images
├── data/               # JSON data files
├── instance/           # Database files (not in git)
├── uploads/            # User uploads (not in git)
└── output/             # Generated files (not in git)
```

## Usage

1. **Register/Login:** Create an account or use default admin credentials
2. **Upload Log:** Upload mainframe error log (text or screenshot)
3. **View Analysis:** See extracted error codes and details
4. **Get Resolution:** View suggested fixes and related incidents
5. **Track History:** Access your previous analyses

## Development

### Running in Development Mode

```bash
# Set environment variable
set FLASK_ENV=development  # Windows
export FLASK_ENV=development  # Linux/Mac

python app.py
```

### Database

The application uses SQLite database stored in `instance/mainframe_assistant.db`. To reset:

```bash
# Stop the server (Ctrl+C)
# Delete the database
rm instance/mainframe_assistant.db  # Linux/Mac
del instance\mainframe_assistant.db  # Windows
# Restart the server
python app.py
```

## Deployment

For production deployment:

1. Set `FLASK_ENV=production` in `.env`
2. Generate a strong `FLASK_SECRET_KEY`
3. Use a production WSGI server (gunicorn, uWSGI)
4. Configure HTTPS
5. Use a production database (PostgreSQL, MySQL)

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License.

## Support

For issues and questions, please open an issue on GitHub.

## Acknowledgments

- Flask framework
- Tesseract OCR
- OpenAI API
- SQLAlchemy

---

**Made with ❤️ by Bob**