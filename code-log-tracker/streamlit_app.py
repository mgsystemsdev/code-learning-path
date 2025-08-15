# streamlit_app.py
"""
Main Streamlit application with Supabase integration.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from typing import Dict, Any, List
from streamlit_option_menu import option_menu
from st_aggrid import AgGrid, GridOptionsBuilder, DataReturnMode, GridUpdateMode

# Import our components
from streamlit_auth import (
    init_session_state, show_auth_page, require_auth, 
    show_logout_button, get_current_user
)
from app.supabase_client import get_supabase_manager

# Page configuration
st.set_page_config(
    page_title="Smart Learning Tracker",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for dark theme
st.markdown("""
<style>
.main-header {
    color: #60a5fa;
    text-align: center;
    padding: 1rem 0;
    border-bottom: 2px solid #475569;
    margin-bottom: 2rem;
}

.metric-card {
    background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
    padding: 1.5rem;
    border-radius: 12px;
    border: 1px solid #475569;
    text-align: center;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.success-message {
    background-color: #059669;
    color: white;
    padding: 0.75rem;
    border-radius: 8px;
    margin: 1rem 0;
}

.error-message {
    background-color: #dc2626;
    color: white;
    padding: 0.75rem;
    border-radius: 8px;
    margin: 1rem 0;
}

.sidebar .sidebar-content {
    background-color: #0f172a;
}

.stSelectbox > div > div {
    background-color: #334155;
    color: white;
}
</style>
""", unsafe_allow_html=True)

def main():
    """Main application entry point."""
    # Initialize session state
    init_session_state()
    
    # Check authentication
    if not st.session_state.authenticated:
        show_auth_page()
        return
    
    # Show main dashboard
    show_dashboard()

def show_dashboard():
    """Show the main dashboard."""
    # Header
    st.markdown('<h1 class="main-header">🎓 Smart Learning Tracker Dashboard</h1>', unsafe_allow_html=True)
    
    # Sidebar navigation
    with st.sidebar:
        # User info
        user = get_current_user()
        if user:
            st.markdown(f"### 👋 Welcome, {user.get('user_metadata', {}).get('first_name', 'User')}!")
        
        # Navigation menu
        selected = option_menu(
            menu_title="Navigation",
            options=["📊 Overview", "📝 Add Session", "📋 Sessions", "📈 Analytics", "⚙️ Settings"],
            icons=["graph-up", "plus-circle", "table", "bar-chart", "gear"],
            menu_icon="cast",
            default_index=0,
            styles={
                "container": {"padding": "0!important", "background-color": "#0f172a"},
                "icon": {"color": "#60a5fa", "font-size": "18px"},
                "nav-link": {"font-size": "16px", "text-align": "left", "margin": "0px", "--hover-color": "#334155"},
                "nav-link-selected": {"background-color": "#1e40af"},
            }
        )
        
        st.divider()
        show_logout_button()
    
    # Main content based on selection
    if selected == "📊 Overview":
        show_overview()
    elif selected == "📝 Add Session":
        show_add_session()
    elif selected == "📋 Sessions":
        show_sessions_table()
    elif selected == "📈 Analytics":
        show_analytics()
    elif selected == "⚙️ Settings":
        show_settings()

def show_overview():
    """Show overview dashboard."""
    st.header("📊 Learning Overview")
    
    # Get data
    supabase = get_supabase_manager()
    sessions = supabase.get_sessions(limit=1000)
    
    if not sessions:
        st.info("No learning sessions found. Start by adding your first session!")
        return
    
    # Convert to DataFrame
    df = pd.DataFrame(sessions)
    
    # Flatten nested item data
    if 'items' in df.columns and len(df) > 0:
        items_df = pd.json_normalize(df['items'])
        df = pd.concat([df.drop('items', axis=1), items_df], axis=1)
    
    # Metrics row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_hours = df['hours_spent'].sum()
        st.markdown(f"""
        <div class="metric-card">
            <h3>⏱️ Total Hours</h3>
            <h2>{total_hours:.1f}h</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        total_sessions = len(df)
        st.markdown(f"""
        <div class="metric-card">
            <h3>📚 Sessions</h3>
            <h2>{total_sessions}</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        avg_session = df['hours_spent'].mean() if len(df) > 0 else 0
        st.markdown(f"""
        <div class="metric-card">
            <h3>📊 Avg Session</h3>
            <h2>{avg_session:.1f}h</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        total_points = df['points_awarded'].sum()
        st.markdown(f"""
        <div class="metric-card">
            <h3>🏆 Points</h3>
            <h2>{total_points:.0f}</h2>
        </div>
        """, unsafe_allow_html=True)
    
    st.divider()
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📈 Daily Learning Hours")
        daily_hours = df.groupby('date')['hours_spent'].sum().reset_index()
        daily_hours['date'] = pd.to_datetime(daily_hours['date'])
        
        fig = px.line(
            daily_hours, 
            x='date', 
            y='hours_spent',
            title="Learning Hours Over Time",
            template="plotly_dark"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("🔧 Skills Distribution")
        if 'language_code' in df.columns:
            lang_hours = df.groupby('language_code')['hours_spent'].sum().reset_index()
            fig = px.pie(
                lang_hours,
                values='hours_spent',
                names='language_code',
                title="Time by Language",
                template="plotly_dark"
            )
            st.plotly_chart(fig, use_container_width=True)

def show_add_session():
    """Show add session form."""
    st.header("📝 Add Learning Session")
    
    supabase = get_supabase_manager()
    
    with st.form("add_session_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            date = st.date_input("📅 Date", datetime.now().date())
            
            # Get languages from Supabase
            languages = supabase.get_languages()
            language_options = {lang['name']: lang['code'] for lang in languages}
            if not language_options:
                language_options = {"Python": "python", "JavaScript": "javascript", "HTML/CSS": "html"}
            
            language_name = st.selectbox("💻 Language", list(language_options.keys()))
            language_code = language_options[language_name]
            
            item_type = st.selectbox("📂 Type", ["Exercise", "Project"])
            work_item = st.text_input("📝 Work Item Name", placeholder="e.g., 'React Todo App' or 'Python Functions'")
            
        with col2:
            hours = st.number_input("🕒 Hours Spent", min_value=0.0, max_value=24.0, step=0.25, format="%.2f")
            status = st.selectbox("📊 Status", ["Planned", "In Progress", "Completed", "Blocked"])
            difficulty = st.selectbox("🎖️ Difficulty", ["Beginner", "Intermediate", "Advanced", "Expert"])
            topic = st.text_input("🎯 Topic", placeholder="e.g., 'Frontend', 'Data Structures'")
        
        tags = st.text_input("🏷️ Tags", placeholder="learning, practice, debugging")
        notes = st.text_area("📋 Notes", placeholder="What did you work on? What challenges did you face?")
        
        submitted = st.form_submit_button("💾 Save Session", use_container_width=True)
        
        if submitted:
            if not work_item or not hours:
                st.error("Please fill in Work Item Name and Hours")
            else:
                session_data = {
                    'date': date.isoformat(),
                    'language_code': language_code,
                    'type': item_type,
                    'canonical_name': work_item,
                    'hours_spent': hours,
                    'status': status,
                    'difficulty': difficulty,
                    'topic': topic,
                    'tags': tags,
                    'notes': notes
                }
                
                with st.spinner("Saving session..."):
                    result = supabase.create_session(session_data)
                
                if result['success']:
                    st.markdown('<div class="success-message">✅ Session saved successfully!</div>', unsafe_allow_html=True)
                    st.balloons()
                else:
                    st.markdown(f'<div class="error-message">❌ Error: {result["error"]}</div>', unsafe_allow_html=True)

def show_sessions_table():
    """Show sessions in an interactive table."""
    st.header("📋 Learning Sessions")
    
    supabase = get_supabase_manager()
    sessions = supabase.get_sessions(limit=500)
    
    if not sessions:
        st.info("No sessions found. Add your first session to get started!")
        return
    
    # Convert to DataFrame
    df = pd.DataFrame(sessions)
    
    # Flatten nested data
    if 'items' in df.columns and len(df) > 0:
        for idx, item_data in enumerate(df['items']):
            if item_data:
                df.loc[idx, 'language'] = item_data.get('language_code', '')
                df.loc[idx, 'type'] = item_data.get('type', '')
                df.loc[idx, 'work_item'] = item_data.get('canonical_name', '')
                df.loc[idx, 'target_hours'] = item_data.get('target_hours', 0)
    
    # Select and reorder columns for display
    display_columns = [
        'id', 'date', 'language', 'type', 'work_item', 
        'hours_spent', 'status', 'difficulty', 'topic', 
        'points_awarded', 'notes'
    ]
    
    # Filter to existing columns
    available_columns = [col for col in display_columns if col in df.columns]
    display_df = df[available_columns].copy()
    
    # Configure AgGrid
    gb = GridOptionsBuilder.from_dataframe(display_df)
    gb.configure_pagination(paginationAutoPageSize=True)
    gb.configure_side_bar()
    gb.configure_selection('single', use_checkbox=True)
    gb.configure_default_column(editable=True, groupable=True)
    
    # Make ID column non-editable
    gb.configure_column('id', editable=False, sort='desc')
    
    gridOptions = gb.build()
    
    # Display grid
    grid_response = AgGrid(
        display_df,
        gridOptions=gridOptions,
        data_return_mode=DataReturnMode.AS_INPUT,
        update_mode=GridUpdateMode.MODEL_CHANGED,
        fit_columns_on_grid_load=False,
        theme='streamlit',
        enable_enterprise_modules=True,
        height=600,
        width='100%'
    )
    
    # Handle updates
    if grid_response['data'] is not None:
        updated_df = pd.DataFrame(grid_response['data'])
        # Find changed rows by comparing to original
        changed_rows = []
        for idx, row in updated_df.iterrows():
            orig_row = display_df.iloc[idx]
            # Only compare editable columns
            editable_cols = [col for col in available_columns if col != 'id']
            changes = {col: row[col] for col in editable_cols if row[col] != orig_row[col]}
            if changes:
                changed_rows.append((row['id'], changes))
        if changed_rows:
            st.info(f"{len(changed_rows)} change(s) detected. Updating database...")
            supabase = get_supabase_manager()
            for session_id, updates in changed_rows:
                result = supabase.update_session(session_id, updates)
                if result.get('success'):
                    st.success(f"Session {session_id} updated.")
                else:
                    st.error(f"Error updating session {session_id}: {result.get('error')}")

def show_analytics():
    """Show analytics and insights."""
    st.header("📈 Learning Analytics")
    
    supabase = get_supabase_manager()
    sessions = supabase.get_sessions(limit=1000)
    
    if not sessions:
        st.info("No data available for analytics. Add some sessions first!")
        return
    
    df = pd.DataFrame(sessions)
    
    # Time-based analytics
    st.subheader("📅 Time Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Weekly progress
        df['date'] = pd.to_datetime(df['date'])
        df['week'] = df['date'].dt.isocalendar().week
        weekly_hours = df.groupby('week')['hours_spent'].sum()
        
        fig = px.bar(
            x=weekly_hours.index,
            y=weekly_hours.values,
            title="Weekly Learning Hours",
            template="plotly_dark",
            labels={'x': 'Week', 'y': 'Hours'}
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Status distribution
        status_counts = df['status'].value_counts()
        fig = px.pie(
            values=status_counts.values,
            names=status_counts.index,
            title="Session Status Distribution",
            template="plotly_dark"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Difficulty analysis
    st.subheader("🎖️ Difficulty Analysis")
    
    difficulty_hours = df.groupby('difficulty')['hours_spent'].sum().reset_index()
    difficulty_points = df.groupby('difficulty')['points_awarded'].sum().reset_index()
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig = px.bar(
            difficulty_hours,
            x='difficulty',
            y='hours_spent',
            title="Hours by Difficulty Level",
            template="plotly_dark"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        fig = px.bar(
            difficulty_points,
            x='difficulty',
            y='points_awarded',
            title="Points by Difficulty Level",
            template="plotly_dark"
        )
        st.plotly_chart(fig, use_container_width=True)

def show_settings():
    """Show settings and configuration."""
    st.header("⚙️ Settings")
    
    user = get_current_user()
    
    if user:
        st.subheader("👤 Profile Information")
        
        col1, col2 = st.columns(2)
        with col1:
            st.text_input("Email", value=user.get('email', ''), disabled=True)
            st.text_input("User ID", value=user.get('id', ''), disabled=True)
        
        with col2:
            created_at = user.get('created_at', '')
            if created_at:
                st.text_input("Account Created", value=created_at[:10], disabled=True)
    
    st.divider()
    
    st.subheader("🗄️ Database Management")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🔄 Refresh Data", use_container_width=True):
            st.cache_data.clear()
            st.success("Data refreshed!")
    
    with col2:
        if st.button("📊 Setup Tables", use_container_width=True):
            supabase = get_supabase_manager()
            result = supabase.create_tables()
            if result['success']:
                st.success("Tables created successfully!")
            else:
                st.error(f"Error: {result['error']}")
    
    with col3:
        if st.button("🔒 Setup Security", use_container_width=True):
            supabase = get_supabase_manager()
            result = supabase.setup_rls_policies()
            if result['success']:
                st.success("Security policies created!")
            else:
                st.error(f"Error: {result['error']}")

if __name__ == "__main__":
    main()
