# streamlit_auth.py
"""
Streamlit authentication interface for Supabase integration.
"""

import streamlit as st
from typing import Dict, Any, Optional
from app.supabase_client import get_supabase_manager

def init_session_state():
    """Initialize session state variables."""
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    if 'user' not in st.session_state:
        st.session_state.user = None
    if 'supabase' not in st.session_state:
        st.session_state.supabase = get_supabase_manager()

def show_auth_page():
    """Show authentication page."""
    st.title("🎓 Smart Learning Tracker")
    st.markdown("Track your coding progress with intelligent insights")
    
    # Create tabs for login and signup
    tab1, tab2 = st.tabs(["🔑 Login", "📝 Sign Up"])
    
    with tab1:
        show_login_form()
    
    with tab2:
        show_signup_form()

def show_login_form():
    """Show login form."""
    st.subheader("Welcome Back!")
    
    with st.form("login_form"):
        email = st.text_input("📧 Email", placeholder="your.email@example.com")
        password = st.text_input("🔒 Password", type="password")
        
        col1, col2 = st.columns([1, 1])
        with col1:
            login_btn = st.form_submit_button("🚀 Login", use_container_width=True)
        with col2:
            forgot_btn = st.form_submit_button("❓ Forgot Password", use_container_width=True)
        
        if login_btn:
            if email and password:
                with st.spinner("Logging in..."):
                    result = st.session_state.supabase.sign_in(email, password)
                    
                if result['success']:
                    st.session_state.authenticated = True
                    st.session_state.user = st.session_state.supabase.get_user()
                    st.success("✅ Login successful!")
                    st.rerun()
                else:
                    st.error(f"❌ Login failed: {result['error']}")
            else:
                st.error("Please fill in all fields")
        
        if forgot_btn:
            st.info("Password reset functionality coming soon!")

def show_signup_form():
    """Show signup form."""
    st.subheader("Join the Learning Community!")
    
    with st.form("signup_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            first_name = st.text_input("👤 First Name")
            email = st.text_input("📧 Email")
            
        with col2:
            last_name = st.text_input("👤 Last Name")
            password = st.text_input("🔒 Password", type="password")
            
        confirm_password = st.text_input("🔒 Confirm Password", type="password")
        
        # Experience level
        experience = st.selectbox(
            "💻 Programming Experience",
            ["Beginner", "Intermediate", "Advanced", "Expert"]
        )
        
        # Privacy agreement
        agree_terms = st.checkbox("I agree to the Terms of Service and Privacy Policy")
        
        signup_btn = st.form_submit_button("🎯 Create Account", use_container_width=True)
        
        if signup_btn:
            if not all([first_name, last_name, email, password, confirm_password]):
                st.error("Please fill in all fields")
            elif password != confirm_password:
                st.error("Passwords don't match")
            elif len(password) < 6:
                st.error("Password must be at least 6 characters")
            elif not agree_terms:
                st.error("Please agree to the terms and conditions")
            else:
                with st.spinner("Creating account..."):
                    metadata = {
                        "first_name": first_name,
                        "last_name": last_name,
                        "experience_level": experience
                    }
                    
                    result = st.session_state.supabase.sign_up(email, password, metadata)
                    
                if result['success']:
                    st.success("✅ Account created! Please check your email for verification.")
                    st.info("Once verified, you can login with your credentials.")
                else:
                    st.error(f"❌ Signup failed: {result['error']}")

def show_logout_button():
    """Show logout button in sidebar."""
    if st.sidebar.button("🚪 Logout", use_container_width=True):
        result = st.session_state.supabase.sign_out()
        if result['success']:
            st.session_state.authenticated = False
            st.session_state.user = None
            st.rerun()

def get_current_user() -> Optional[Dict[str, Any]]:
    """Get current authenticated user."""
    return st.session_state.user

def is_authenticated() -> bool:
    """Check if user is authenticated."""
    return st.session_state.authenticated

def require_auth():
    """Decorator-like function to require authentication."""
    if not is_authenticated():
        show_auth_page()
        st.stop()
    return True
