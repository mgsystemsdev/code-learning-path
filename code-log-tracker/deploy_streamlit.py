# deploy_streamlit.py
"""
Deployment script for Streamlit + Supabase integration.
"""

import subprocess
import sys
import os
from pathlib import Path

def install_dependencies():
    """Install required dependencies."""
    print("📦 Installing dependencies...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], check=True)
        print("✅ Dependencies installed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing dependencies: {e}")
        return False
    return True

def check_environment():
    """Check if environment variables are set."""
    print("🔍 Checking environment configuration...")
    
    required_vars = ["SUPABASE_URL", "SUPABASE_ANON_KEY"]
    missing_vars = []
    
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print(f"❌ Missing environment variables: {', '.join(missing_vars)}")
        print("Please set these in your .env file or environment.")
        return False
    
    print("✅ Environment configuration looks good!")
    return True

def run_streamlit():
    """Run the Streamlit application."""
    print("🚀 Starting Streamlit application...")
    try:
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "streamlit_app.py",
            "--server.port=8501",
            "--server.address=0.0.0.0",
            "--theme.base=dark",
            "--theme.primaryColor=#60a5fa",
            "--theme.backgroundColor=#0f172a",
            "--theme.secondaryBackgroundColor=#1e293b"
        ])
    except KeyboardInterrupt:
        print("\n👋 Streamlit application stopped.")
    except Exception as e:
        print(f"❌ Error running Streamlit: {e}")

def main():
    """Main deployment process."""
    print("🎓 Smart Learning Tracker - Streamlit Deployment")
    print("=" * 50)
    
    # Change to script directory
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    # Check if we're in the right directory
    if not Path("streamlit_app.py").exists():
        print("❌ streamlit_app.py not found. Are you in the right directory?")
        return
    
    # Install dependencies
    if not install_dependencies():
        return
    
    # Check environment
    if not check_environment():
        return
    
    # Run Streamlit
    run_streamlit()

if __name__ == "__main__":
    main()
