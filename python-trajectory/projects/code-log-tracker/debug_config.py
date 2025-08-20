#!/usr/bin/env python3
"""
Debug configuration helper - helps diagnose environment variable issues.
Run this to check if your configuration is working.
"""

import os
import streamlit as st
from dotenv import load_dotenv

def check_config():
    """Check configuration sources."""
    load_dotenv()
    
    print("🔍 Configuration Debug Information")
    print("=" * 50)
    
    # Check environment variables
    env_url = os.getenv("SUPABASE_URL")
    env_anon = os.getenv("SUPABASE_ANON_KEY")
    env_service = os.getenv("SUPABASE_SERVICE_KEY")
    
    print(f"Environment Variables:")
    print(f"  SUPABASE_URL: {'✅ Set' if env_url else '❌ Missing'}")
    print(f"  SUPABASE_ANON_KEY: {'✅ Set' if env_anon else '❌ Missing'}")
    print(f"  SUPABASE_SERVICE_KEY: {'✅ Set' if env_service else '❌ Missing'}")
    
    # Check Streamlit secrets (if available)
    try:
        secret_url = st.secrets.get("SUPABASE_URL")
        secret_anon = st.secrets.get("SUPABASE_ANON_KEY") 
        secret_service = st.secrets.get("SUPABASE_SERVICE_KEY")
        
        print(f"\nStreamlit Secrets:")
        print(f"  SUPABASE_URL: {'✅ Set' if secret_url else '❌ Missing'}")
        print(f"  SUPABASE_ANON_KEY: {'✅ Set' if secret_anon else '❌ Missing'}")
        print(f"  SUPABASE_SERVICE_KEY: {'✅ Set' if secret_service else '❌ Missing'}")
        
    except Exception as e:
        print(f"\nStreamlit Secrets: ❌ Not available ({e})")
    
    # Final configuration
    final_url = None
    final_anon = None
    
    try:
        final_url = st.secrets.get("SUPABASE_URL", env_url)
        final_anon = st.secrets.get("SUPABASE_ANON_KEY", env_anon)
    except:
        final_url = env_url
        final_anon = env_anon
    
    print(f"\nFinal Configuration:")
    print(f"  Using URL: {'✅ Available' if final_url else '❌ Missing'}")
    print(f"  Using ANON_KEY: {'✅ Available' if final_anon else '❌ Missing'}")
    
    if final_url and final_anon:
        print(f"\n🎉 Configuration is complete!")
        try:
            from app.supabase_client import get_supabase_manager
            manager = get_supabase_manager()
            print(f"✅ Supabase connection test successful!")
        except Exception as e:
            print(f"❌ Connection test failed: {e}")
    else:
        print(f"\n⚠️  Configuration incomplete. Add missing variables to:")
        print(f"  - Local: .env file")
        print(f"  - Streamlit Cloud: App Settings → Secrets")

if __name__ == "__main__":
    check_config()
