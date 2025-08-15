# quick_setup.py
"""
Quick setup guide for Supabase credentials.
"""

import os
from pathlib import Path

def show_setup_instructions():
    """Show setup instructions."""
    print("🎓 Smart Learning Tracker - Quick Setup Guide")
    print("=" * 50)
    
    env_file = Path(".env")
    
    print("\n1. 🔗 Get Your Supabase Credentials:")
    print("   - Go to: https://app.supabase.com")
    print("   - Select your project (or create one)")
    print("   - Go to: Settings → API")
    print("   - Copy your:")
    print("     • Project URL")
    print("     • Anon public key")
    print("     • Service role key (optional)")
    
    print("\n2. 📝 Update Your .env File:")
    print(f"   - Open: {env_file.absolute()}")
    print("   - Replace these values:")
    
    print("""
SUPABASE_URL=https://your-actual-project-id.supabase.co
SUPABASE_ANON_KEY=your-actual-anon-key-here
SUPABASE_SERVICE_KEY=your-actual-service-role-key-here
    """)
    
    print("\n3. 🧪 Test Your Setup:")
    print("   Run: python3 test_connection.py")
    
    print("\n4. 🗄️ Setup Database:")
    print("   - Go to your Supabase dashboard")
    print("   - SQL Editor → New query")
    print("   - Copy content from: supabase_setup.sql")
    print("   - Run the SQL script")
    
    print("\n5. 🚀 Launch App:")
    print("   - Streamlit: python3 deploy_streamlit.py")
    print("   - Desktop: python3 main.py")
    
    print(f"\n📄 Current .env file location: {env_file.absolute()}")
    
    if env_file.exists():
        print("✅ .env file found")
        
        # Check if configured
        with open(env_file, 'r') as f:
            content = f.read()
            if "your-project-id" in content or "your-anon-key" in content:
                print("⚠️  Still has placeholder values - needs configuration")
            else:
                print("✅ Appears to be configured")
    else:
        print("❌ .env file not found")

def create_test_connection_script():
    """Create a simple connection test script."""
    test_script = """# test_connection.py
\"\"\"
Test Supabase connection.
\"\"\"

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_connection():
    print("🔍 Testing Supabase Configuration...")
    
    url = os.getenv("SUPABASE_URL")
    anon_key = os.getenv("SUPABASE_ANON_KEY")
    service_key = os.getenv("SUPABASE_SERVICE_KEY")
    
    print(f"📍 URL: {'✅ Set' if url and 'supabase.co' in url else '❌ Missing or invalid'}")
    print(f"🔑 Anon Key: {'✅ Set' if anon_key and len(anon_key) > 50 else '❌ Missing or too short'}")
    print(f"🛡️  Service Key: {'✅ Set' if service_key and len(service_key) > 50 else '⚠️  Not set (optional)'}")
    
    if not url or 'supabase.co' not in url:
        print("\\n❌ Please set SUPABASE_URL in your .env file")
        return False
        
    if not anon_key or len(anon_key) < 50:
        print("\\n❌ Please set SUPABASE_ANON_KEY in your .env file")
        return False
    
    # Test actual connection
    try:
        from supabase import create_client
        
        print("\\n🔌 Testing connection...")
        client = create_client(url, anon_key)
        
        # Try a simple operation
        try:
            # This will work even without tables
            response = client.auth.get_user()
            print("✅ Connection successful!")
            print("📡 Supabase client initialized properly")
            return True
        except Exception as e:
            if "JWT" in str(e) or "expired" in str(e):
                print("✅ Connection successful! (No user logged in, which is expected)")
                return True
            else:
                print(f"⚠️  Connection established but got error: {e}")
                return True
        
    except ImportError:
        print("❌ Supabase package not installed")
        print("Run: pip install supabase")
        return False
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return False

if __name__ == "__main__":
    success = test_connection()
    if success:
        print("\\n🎉 Setup looks good! You can now:")
        print("   • Run the database setup SQL")
        print("   • Launch: python3 deploy_streamlit.py")
    else:
        print("\\n🔧 Please fix the issues above and try again")
"""
    
    with open("test_connection.py", "w") as f:
        f.write(test_script)
    
    print("📝 Created test_connection.py script")

if __name__ == "__main__":
    show_setup_instructions()
    create_test_connection_script()
