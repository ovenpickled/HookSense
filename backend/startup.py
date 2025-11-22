"""
Startup script that initializes the database before starting the server.
"""
import os
import subprocess
import sys

def run_migrations():
    """Run database migrations"""
    print("🔄 Running database migrations...")
    try:
        # Create tables directly using SQLAlchemy models
        from app.database import engine
        from app.models import Base
        
        print("Creating database tables...")
        Base.metadata.create_all(bind=engine)
        print("✅ Database tables created successfully!")
        return True
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        return False

def start_worker():
    """Start Celery worker in background"""
    print("🚀 Starting Celery worker...")
    subprocess.Popen([
        "celery", "-A", "app.worker.celery", 
        "worker", "--loglevel=info"
    ])
    print("✅ Celery worker started!")

def start_server():
    """Start FastAPI server"""
    print("🚀 Starting FastAPI server...")
    os.execvp("uvicorn", [
        "uvicorn", "app.main:app", 
        "--host", "0.0.0.0", 
        "--port", "10000"
    ])

if __name__ == "__main__":
    print("=" * 50)
    print("🎯 AI Code Reviewer - Starting Up")
    print("=" * 50)
    
    # Step 1: Run migrations
    if not run_migrations():
        print("⚠️  Migration failed, but continuing anyway...")
    
    # Step 2: Start worker
    start_worker()
    
    # Step 3: Start server (this replaces current process)
    start_server()
