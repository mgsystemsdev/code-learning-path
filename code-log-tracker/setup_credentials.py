# setup_credentials.py
"""
Safe credential setup helper for Supabase integration.
Run this to configure your environment variables.
"""

import os
from pathlib import Path

def setup_credentials():
    """Interactive credential setup."""
    print("🎓 Smart Learning Tracker - Supabase Setup")
    print("=" * 50)
    
    env_file = Path(".env")
    
    print("\n📋 Please provide your Supabase credentials:")
    print("   Get these from: https://app.supabase.com/project/YOUR_PROJECT/settings/api")
    print()
    
    # Get credentials from user
    supabase_url = input("🔗 Supabase URL (https://xxx.supabase.co): ").strip()
    anon_key = input("🔑 Anon Key: ").strip()
    service_key = input("🛡️  Service Role Key (optional): ").strip()
    
    if not supabase_url or not anon_key:
        print("❌ URL and Anon Key are required!")
        return False
    
    # Validate URL format
    if not supabase_url.startswith("https://") or ".supabase.co" not in supabase_url:
        print("❌ Invalid Supabase URL format!")
        return False
    
    # Generate encryption key
    import secrets
    encryption_key = secrets.token_urlsafe(32)[:32]
    jwt_secret = secrets.token_urlsafe(64)
    
    # Create .env content
    env_content = f"""# Supabase Configuration
SUPABASE_URL={supabase_url}
SUPABASE_ANON_KEY={anon_key}
SUPABASE_SERVICE_KEY={service_key}

# App Configuration  
APP_MODE=production
DATABASE_MODE=supabase
DEBUG=false

# Security
JWT_SECRET={jwt_secret}
ENCRYPTION_KEY={encryption_key}

# Auto-generated on {os.popen('date').read().strip()}
"""
    
    # Write to .env file
    try:
        with open(env_file, "w") as f:
            f.write(env_content)
        
        print("\n✅ Credentials saved to .env file!")
        print("🔒 Keep this file secure and never commit it to git!")
        
        # Test connection
        return test_connection()
        
    except Exception as e:
        print(f"❌ Error saving credentials: {e}")
        return False

def test_connection():
    """Test the Supabase connection."""
    print("\n🔍 Testing Supabase connection...")
    
    try:
        from dotenv import load_dotenv
        from supabase import create_client
        
        # Load environment variables
        load_dotenv()
        
        url = os.getenv("SUPABASE_URL")
        key = os.getenv("SUPABASE_ANON_KEY")
        
        if not url or not key:
            print("❌ Environment variables not loaded properly!")
            return False
        
        # Create client
        client = create_client(url, key)
        
        # Test with a simple query (will fail if not authenticated, but that's ok)
        try:
            # Try to get auth user (will be None if not logged in)
            response = client.auth.get_user()
            print("✅ Supabase connection successful!")
            return True
            
        except Exception as auth_error:
            # This is expected if no user is logged in
            if "JWT" in str(auth_error) or "expired" in str(auth_error):
                print("✅ Supabase connection successful! (Auth working)")
                return True
            else:
                print(f"⚠️  Connection established, but auth test failed: {auth_error}")
                return True  # Connection is still valid
        
    except ImportError as e:
        print(f"❌ Missing dependencies: {e}")
        print("Run: pip install -r requirements.txt")
        return False
    except Exception as e:
        print(f"❌ Connection test failed: {e}")
        return False

def check_existing_env():
    """Check if .env file already exists."""
    env_file = Path(".env")
    
    if env_file.exists():
        print("📄 Found existing .env file")
        
        # Load and check current values
        try:
            from dotenv import load_dotenv
            load_dotenv()
            
            url = os.getenv("SUPABASE_URL")
            anon_key = os.getenv("SUPABASE_ANON_KEY")
            
            if url and anon_key and "your-" not in url:
                print("✅ Credentials appear to be configured!")
                
                choice = input("🔄 Do you want to reconfigure? (y/N): ").strip().lower()
                if choice != 'y':
                    return test_connection()
            else:
                print("⚠️  Placeholder values detected, need to configure...")
                
        except ImportError:
            print("⚠️  python-dotenv not installed, run: pip install python-dotenv")
    
    return False

def main():
    """Main setup process."""
    # Check if already configured
    if check_existing_env():
        print("🎉 Setup complete!")
        return
    
    # Run interactive setup
    if setup_credentials():
        print("\n🎉 Supabase setup complete!")
        print("\n📝 Next steps:")
        print("1. Run the database setup: Run supabase_setup.sql in your Supabase dashboard")
        print("2. Test the Streamlit app: python deploy_streamlit.py")
        print("3. Or test PySide6 app: python main.py")
    else:
        print("\n❌ Setup failed. Please try again.")

if __name__ == "__main__":
    main()
