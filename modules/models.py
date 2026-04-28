"""
Database models for Mainframe AI Support Assistant
"""
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

db = SQLAlchemy()


class User(UserMixin, db.Model):
    """User model for authentication"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    
    # Relationships
    analyses = db.relationship('AnalysisHistory', backref='user', lazy='dynamic', 
                              cascade='all, delete-orphan')
    inc_records = db.relationship('INCRecord', backref='creator', lazy='dynamic')
    
    def set_password(self, password):
        """Hash and set password"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Check if password matches hash"""
        return check_password_hash(self.password_hash, password)
    
    def update_last_login(self):
        """Update last login timestamp"""
        self.last_login = datetime.utcnow()
        db.session.commit()
    
    def __repr__(self):
        return f'<User {self.username}>'


class AnalysisHistory(db.Model):
    """Analysis history model to track user's log analyses"""
    __tablename__ = 'analysis_history'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    
    # Extracted information
    jobname = db.Column(db.String(50))
    jobid = db.Column(db.String(20))
    status = db.Column(db.String(20))
    return_code = db.Column(db.String(20), index=True)
    step = db.Column(db.String(50))
    error_message = db.Column(db.Text)
    
    # Original data
    log_content = db.Column(db.Text)
    image_path = db.Column(db.String(255))
    
    # Generated output
    annotated_image_path = db.Column(db.String(255))
    resolution_text = db.Column(db.Text)
    
    # Metadata
    extraction_method = db.Column(db.String(20))  # 'regex' or 'ai'
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'jobname': self.jobname or 'NOT FOUND',
            'jobid': self.jobid or 'NOT FOUND',
            'status': self.status or 'NOT FOUND',
            'return_code': self.return_code or 'NOT FOUND',
            'step': self.step or 'NOT FOUND',
            'error_message': self.error_message or 'NOT FOUND',
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'extraction_method': self.extraction_method
        }
    
    def __repr__(self):
        return f'<Analysis {self.id} - {self.return_code}>'


class INCRecord(db.Model):
    """Incident record model for tracking previous incidents"""
    __tablename__ = 'inc_records'
    
    id = db.Column(db.Integer, primary_key=True)
    inc_number = db.Column(db.String(20), unique=True, nullable=False, index=True)
    error_code = db.Column(db.String(20), index=True)
    
    # Incident details
    jobname = db.Column(db.String(50))
    description = db.Column(db.Text)
    resolution = db.Column(db.Text)
    status = db.Column(db.String(20), default='Open')  # Open, In Progress, Resolved, Closed
    
    # Metadata
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    resolved_at = db.Column(db.DateTime)
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'inc_number': self.inc_number,
            'error_code': self.error_code,
            'jobname': self.jobname,
            'description': self.description,
            'resolution': self.resolution,
            'status': self.status,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'resolved_at': self.resolved_at.strftime('%Y-%m-%d %H:%M:%S') if self.resolved_at else None
        }
    
    def __repr__(self):
        return f'<INC {self.inc_number}>'


def init_db(app):
    """Initialize database with app context"""
    # db.init_app(app) is already called in create_app(), so we don't call it here
    db.create_all()
    
    # Create default admin user if no users exist
    if User.query.count() == 0:
        admin = User(
            username='admin',
            email='admin@example.com',
            full_name='Administrator'
        )
        admin.set_password('admin123')
        db.session.add(admin)
        db.session.commit()
        print("[OK] Default admin user created (username: admin, password: admin123)")
    
    # Create sample INC records if none exist
    if INCRecord.query.count() == 0:
        sample_incs = [
        INCRecord(
            inc_number='INC12345',
            error_code='U0777',
            jobname='DUMMYBATCH01',
            description='Data validation failed in STEP002 - Invalid character in RECORD#007',
            resolution='Fixed invalid character in input file. Verified copybook format matches data structure. Re-ran job successfully.',
            status='Resolved',
            resolved_at=datetime(2026, 4, 15, 10, 30)
        ),
        INCRecord(
            inc_number='INC98765',
            error_code='S013',
            jobname='FILEBATCH05',
            description='Dataset open error in STEP005 - RECFM mismatch on DDNAME INPUT1',
            resolution='Updated JCL DD statement to match dataset attributes (RECFM=FB, LRECL=80). Job completed successfully.',
            status='Resolved',
            resolved_at=datetime(2026, 4, 16, 14, 45)
        ),
        INCRecord(
            inc_number='INC54321',
            error_code='S0C7',
            jobname='CALCBATCH10',
            description='Numeric data exception in STEP010 - Invalid data in AMOUNT field',
            resolution='Identified non-numeric characters in input data. Cleaned data and added validation step. Job ran without errors.',
            status='Resolved',
            resolved_at=datetime(2026, 4, 17, 9, 15)
        ),
        INCRecord(
            inc_number='INC11111',
            error_code='U0777',
            jobname='VALIDBATCH03',
            description='Data validation abend - Record format mismatch',
            resolution='Updated copybook definition to match new data format. Recompiled program and re-ran successfully.',
            status='Resolved',
            resolved_at=datetime(2026, 4, 18, 11, 20)
        ),
        INCRecord(
            inc_number='INC22222',
            error_code='S013',
            jobname='DATABATCH07',
            description='DCB attribute mismatch on output dataset',
            resolution='Corrected LRECL in JCL from 100 to 80. Deleted and recreated output dataset with correct attributes.',
            status='Resolved',
            resolved_at=datetime(2026, 4, 19, 8, 50)
        )
        ]
        
        db.session.bulk_save_objects(sample_incs)
        db.session.commit()
        print("[OK] Sample INC records created")

# Made with Bob
