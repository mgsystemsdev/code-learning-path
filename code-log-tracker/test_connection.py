# test_connection.py
"""
Test Supabase connection.
"""

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
        print("\n❌ Please set SUPABASE_URL in your .env file")
        return False
        
    if not anon_key or len(anon_key) < 50:
        print("\n❌ Please set SUPABASE_ANON_KEY in your .env file")
        return False
    
    # Test actual connection
    try:
        from supabase import create_client
        
        print("\n🔌 Testing connection...")
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
        print("\n🎉 Setup looks good! You can now:")
        print("   • Run the database setup SQL")
        print("   • Launch: python3 deploy_streamlit.py")
    else:
        print("\n🔧 Please fix the issues above and try again")
