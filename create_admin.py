"""
Script to create admin user in the database
"""
from app import create_app
from modules.models import db, User

app = create_app('development')

with app.app_context():
    # Check if admin exists
    admin = User.query.filter_by(username='admin').first()
    
    if admin:
        print(f"Admin user already exists: {admin.username}")
        print(f"Email: {admin.email}")
        # Update password to be sure
        admin.set_password('admin123')
        db.session.commit()
        print("Password reset to: admin123")
    else:
        # Create new admin user
        admin = User(username='admin', email='admin@mainframe.local')
        admin.set_password('admin123')
        db.session.add(admin)
        db.session.commit()
        print("Admin user created successfully!")
        print("Username: admin")
        print("Password: admin123")
        print(f"Email: {admin.email}")
    
    # List all users
    print("\nAll users in database:")
    users = User.query.all()
    for user in users:
        print(f"  - {user.username} ({user.email})")

# Made with Bob
