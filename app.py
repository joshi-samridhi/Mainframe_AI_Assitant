"""
Mainframe AI Support Assistant - Main Flask Application
A web-based tool for analyzing mainframe logs and providing visual debugging support
"""
import os
import shutil
from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify, send_from_directory
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.utils import secure_filename
from datetime import datetime
import json

# ===== ADD THIS SECTION =====
# Load environment variables FIRST
from dotenv import load_dotenv
load_dotenv()

# Configure Tesseract OCR
import pytesseract
tesseract_path = os.environ.get('TESSERACT_PATH', r'C:\Program Files\Tesseract-OCR\tesseract.exe')
if os.path.exists(tesseract_path):
    pytesseract.pytesseract.tesseract_cmd = tesseract_path
    print(f"[OK] Tesseract configured: {tesseract_path}")
else:
    print(f"[WARNING] Tesseract not found at: {tesseract_path}")
    print("OCR features may not work. Please check TESSERACT_PATH in .env file")
# ===== END OF NEW SECTION =====


# Import configuration
from config import config

# Import models and modules
from modules.models import db, User, AnalysisHistory, INCRecord, init_db
from modules.log_extractor import LogExtractor
from modules.ocr_processor import OCRProcessor
from modules.ai_fallback import AIFallback
from modules.knowledge_base import KnowledgeBase

# Import error screen generator
from generate_error_screens import generate_u0777_screen, generate_s013_screen, generate_s0c7_screen


def create_app(config_name='development'):
    """Create and configure Flask application"""
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Get base directory
    basedir = os.path.abspath(os.path.dirname(__file__))
    
    # Initialize extensions
    db.init_app(app)
    
    # Initialize Flask-Login
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'login'
    login_manager.login_message = 'Please log in to access this page.'
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    # Ensure required directories exist
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(app.config['OUTPUT_FOLDER'], exist_ok=True)
    
    # Ensure instance directory exists for database
    instance_path = os.path.join(basedir, 'instance')
    os.makedirs(instance_path, exist_ok=True)
    
    # Initialize database and create tables
    with app.app_context():
        init_db(app)
    
    # Initialize modules
    log_extractor = LogExtractor()
    ocr_processor = OCRProcessor(app.config.get('TESSERACT_PATH'))
    ai_fallback = AIFallback(app.config.get('OPENAI_API_KEY'))
    knowledge_base = KnowledgeBase()
    
    # Helper function to check allowed file extensions
    def allowed_file(filename, allowed_extensions=None):
        if allowed_extensions is None:
            allowed_extensions = app.config['ALLOWED_EXTENSIONS']
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in allowed_extensions
    
    # ==================== ROUTES ====================
    
    @app.route('/')
    def index():
        """Home page - redirects based on authentication"""
        if current_user.is_authenticated:
            return redirect(url_for('dashboard'))
        return redirect(url_for('login'))
    
    @app.route('/register', methods=['GET', 'POST'])
    def register():
        """User registration"""
        if current_user.is_authenticated:
            return redirect(url_for('dashboard'))
        
        if request.method == 'POST':
            username = request.form.get('username', '').strip()
            email = request.form.get('email', '').strip()
            password = request.form.get('password', '')
            full_name = request.form.get('full_name', '').strip()
            
            # Validation
            if not username or not email or not password:
                flash('All fields are required', 'error')
                return render_template('auth/register.html')
            
            if len(username) < 3:
                flash('Username must be at least 3 characters', 'error')
                return render_template('auth/register.html')
            
            if len(password) < 8:
                flash('Password must be at least 8 characters', 'error')
                return render_template('auth/register.html')
            
            # Check if user exists
            if User.query.filter_by(username=username).first():
                flash('Username already exists', 'error')
                return render_template('auth/register.html')
            
            if User.query.filter_by(email=email).first():
                flash('Email already registered', 'error')
                return render_template('auth/register.html')
            
            # Create new user
            user = User(username=username, email=email, full_name=full_name)
            user.set_password(password)
            
            db.session.add(user)
            db.session.commit()
            
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('login'))
        
        return render_template('auth/register.html')
    
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        """User login"""
        if current_user.is_authenticated:
            return redirect(url_for('dashboard'))
        
        if request.method == 'POST':
            username = request.form.get('username', '').strip()
            password = request.form.get('password', '')
            remember = request.form.get('remember', False)
            
            if not username or not password:
                flash('Please enter username and password', 'error')
                return render_template('auth/login.html')
            
            # Find user by username or email
            user = User.query.filter(
                (User.username == username) | (User.email == username)
            ).first()
            
            if user and user.check_password(password):
                login_user(user, remember=remember)
                user.update_last_login()
                
                flash(f'Welcome back, {user.full_name or user.username}!', 'success')
                
                # Redirect to next page or dashboard
                next_page = request.args.get('next')
                return redirect(next_page) if next_page else redirect(url_for('dashboard'))
            else:
                flash('Invalid username or password', 'error')
        
        return render_template('auth/login.html')
    
    @app.route('/logout')
    @login_required
    def logout():
        """User logout"""
        logout_user()
        flash('You have been logged out', 'info')
        return redirect(url_for('login'))
    
    @app.route('/dashboard')
    @login_required
    def dashboard():
        """User dashboard"""
        # Get user's recent analyses
        recent_analyses = AnalysisHistory.query.filter_by(user_id=current_user.id)\
            .order_by(AnalysisHistory.created_at.desc())\
            .limit(5)\
            .all()
        
        # Get statistics
        total_analyses = AnalysisHistory.query.filter_by(user_id=current_user.id).count()
        
        # Get most common error codes
        error_codes = db.session.query(
            AnalysisHistory.return_code,
            db.func.count(AnalysisHistory.return_code).label('count')
        ).filter(
            AnalysisHistory.user_id == current_user.id,
            AnalysisHistory.return_code != 'NOT FOUND'
        ).group_by(AnalysisHistory.return_code)\
         .order_by(db.text('count DESC'))\
         .limit(5)\
         .all()
        
        return render_template('dashboard.html',
                             recent_analyses=recent_analyses,
                             total_analyses=total_analyses,
                             error_codes=error_codes)
    
    @app.route('/analyze', methods=['GET', 'POST'])
    @login_required
    def analyze():
        """Main analysis interface - STEP 1"""
        if request.method == 'POST':
            log_content = ''
            extraction_method = 'regex'
            image_path = None
            
            # Check if file was uploaded
            if 'log_file' in request.files:
                file = request.files['log_file']
                if file and file.filename and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                    filename = f"{current_user.id}_{timestamp}_{filename}"
                    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    file.save(filepath)
                    
                    # Check if it's an image
                    if allowed_file(filename, {'png', 'jpg', 'jpeg', 'bmp', 'tiff'}):
                        # Use OCR to extract text
                        log_content, success = ocr_processor.extract_with_preprocessing(filepath)
                        if not success:
                            flash(f'OCR Error: {log_content}', 'error')
                            return render_template('index.html')
                        image_path = filepath
                        extraction_method = 'ocr'
                    else:
                        # Read text file
                        try:
                            with open(filepath, 'r', encoding='utf-8') as f:
                                log_content = f.read()
                        except Exception as e:
                            flash(f'Error reading file: {str(e)}', 'error')
                            return render_template('index.html')
            
            # Get text from textarea if no file
            if not log_content:
                log_content = request.form.get('log_content', '').strip()
            
            if not log_content:
                flash('Please provide log content or upload a file', 'error')
                return render_template('index.html')
            
            # Extract information using regex
            extracted_data, confidence, method = log_extractor.extract(log_content)
            
            # Use AI fallback if confidence is low
            if confidence < 0.7 and ai_fallback.is_available():
                extracted_data, confidence = ai_fallback.enhance_extraction(extracted_data, log_content)
                extraction_method = 'hybrid'
            
            # Save to database
            analysis = AnalysisHistory(
                user_id=current_user.id,
                jobname=extracted_data.get('jobname'),
                jobid=extracted_data.get('jobid'),
                status=extracted_data.get('status'),
                return_code=extracted_data.get('return_code'),
                step=extracted_data.get('step'),
                error_message=extracted_data.get('error'),
                log_content=log_content,
                image_path=image_path,
                extraction_method=extraction_method
            )
            db.session.add(analysis)
            db.session.commit()
            
            # Store analysis ID in session for next steps
            session['current_analysis_id'] = analysis.id
            
            return redirect(url_for('result', analysis_id=analysis.id))
        
        return render_template('index.html')
    
    @app.route('/result/<int:analysis_id>')
    @login_required
    def result(analysis_id):
        """Display extraction results - STEP 1 Results"""
        analysis = AnalysisHistory.query.get_or_404(analysis_id)
        
        # Verify ownership
        if analysis.user_id != current_user.id:
            flash('Access denied', 'error')
            return redirect(url_for('dashboard'))
        
        return render_template('result.html', analysis=analysis)
    
    @app.route('/resolution/<int:analysis_id>')
    @login_required
    def resolution(analysis_id):
        """Display resolution and annotated image - STEP 2"""
        analysis = AnalysisHistory.query.get_or_404(analysis_id)
        
        # Verify ownership
        if analysis.user_id != current_user.id:
            flash('Access denied', 'error')
            return redirect(url_for('dashboard'))
        
        # Get resolution from knowledge base
        error_code = analysis.return_code
        error_info = knowledge_base.get_error_info(error_code)
        
        # Generate annotated image if not already generated
        if not analysis.annotated_image_path and error_code != 'NOT FOUND':
            image_filename = f"annotated_{analysis.id}_{error_code}.png"
            image_path = os.path.join(app.config['OUTPUT_FOLDER'], image_filename)
            
            # Generate based on error code
            try:
                if error_code == 'U0777':
                    generate_u0777_screen()
                    # Copy generated image to user-specific path
                    import shutil
                    shutil.copy('mainframe-error-screens/output/U0777_error_screen.png', image_path)
                elif error_code == 'S013':
                    generate_s013_screen()
                    shutil.copy('mainframe-error-screens/output/S013_error_screen.png', image_path)
                elif error_code == 'S0C7':
                    generate_s0c7_screen()
                    shutil.copy('mainframe-error-screens/output/S0C7_error_screen.png', image_path)
                
                analysis.annotated_image_path = image_path
                db.session.commit()
            except Exception as e:
                print(f"Error generating annotated image: {e}")
        
        # Get related INC records
        related_incs = INCRecord.query.filter_by(error_code=error_code)\
            .order_by(INCRecord.created_at.desc())\
            .limit(5)\
            .all()
        
        return render_template('resolution.html',
                             analysis=analysis,
                             error_info=error_info,
                             related_incs=related_incs)
    
    @app.route('/inc/<inc_number>')
    @login_required
    def inc_detail(inc_number):
        """Display INC detail page - STEP 3"""
        inc = INCRecord.query.filter_by(inc_number=inc_number).first_or_404()
        return render_template('inc_detail.html', inc=inc)
    
    @app.route('/history')
    @login_required
    def history():
        """View user's analysis history"""
        page = request.args.get('page', 1, type=int)
        per_page = 20
        
        analyses = AnalysisHistory.query.filter_by(user_id=current_user.id)\
            .order_by(AnalysisHistory.created_at.desc())\
            .paginate(page=page, per_page=per_page, error_out=False)
        
        return render_template('history.html', analyses=analyses)
    
    @app.route('/profile')
    @login_required
    def profile():
        """User profile page"""
        from datetime import datetime, timedelta
        
        # Get user's recent analyses
        recent_analyses = AnalysisHistory.query.filter_by(user_id=current_user.id)\
            .order_by(AnalysisHistory.created_at.desc())\
            .limit(10)\
            .all()
        
        # Calculate statistics
        total_analyses = AnalysisHistory.query.filter_by(user_id=current_user.id).count()
        
        # Calculate days active (days since first analysis or registration)
        first_analysis = AnalysisHistory.query.filter_by(user_id=current_user.id)\
            .order_by(AnalysisHistory.created_at.asc())\
            .first()
        
        if first_analysis:
            days_active = (datetime.now() - first_analysis.created_at).days + 1
        else:
            days_active = (datetime.now() - current_user.created_at).days + 1
        
        # Count AI-assisted analyses
        ai_assisted = AnalysisHistory.query.filter_by(
            user_id=current_user.id,
            extraction_method='hybrid'
        ).count()
        
        stats = {
            'total_analyses': total_analyses,
            'days_active': days_active,
            'ai_assisted': ai_assisted
        }
        
        return render_template('auth/profile.html',
                             stats=stats,
                             recent_analyses=recent_analyses,
                             now=datetime.now())
    
    @app.route('/output/<path:filename>')
    @login_required
    def serve_output(filename):
        """Serve generated output files"""
        return send_from_directory(app.config['OUTPUT_FOLDER'], filename)
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return render_template('errors/404.html'), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return render_template('errors/500.html'), 500
    
    return app


# Create app instance
app = create_app(os.environ.get('FLASK_ENV', 'development'))


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

# Made with Bob
