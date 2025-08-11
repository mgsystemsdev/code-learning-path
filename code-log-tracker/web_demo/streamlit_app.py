# web_demo/streamlit_app.py
import os
from pathlib import Path
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Learning Tracker (Demo)", layout="wide")
st.title("Learning Tracker – Demo View")

# --- Paths ---
HERE = Path(__file__).resolve().parent
DATA_PATH = HERE / "demo_data.csv"

# --- Ensure demo_data.csv exists ---
def try_export_from_db(limit=1000) -> bool:
    """
    Try to export from SQLite using scripts/export_demo_data.py.
    Returns True if file was created, else False.
    """
    try:
        # Add repo root to path and import exporter
        repo_root = HERE.parent
        import sys
        if str(repo_root) not in sys.path:
            sys.path.insert(0, str(repo_root))
        from scripts.export_demo_data import export  # type: ignore
        export(limit=limit)  # writes to web_demo/demo_data.csv by default
        return DATA_PATH.exists()
    except Exception as e:
        st.info(f"Could not export from DB automatically ({e}). Using seeded demo data.")
        return False

def seed_demo_csv():
    """Create a small, valid CSV so the app can render even without a DB."""
    cols = [
        "ID","Date","Type","Exercise Name","Project Name","Activity Name",
        "Notes","Status","Hours","Tags","Difficulty","Topic","Points","Progress %"
    ]
    demo = pd.DataFrame([
        [1,"2025-08-01","Exercise","Loops","","","Practiced for/while loops","Completed",1.5,"python,basic","Beginner","Python Basics",1.5, ""],
        [2,"2025-08-02","Project","","Compliance MVP","Auth flow","Built login w/ JWT","In Progress",2.0,"fastapi,auth","Intermediate","APIs",3.0, 12.5],
    ], columns=cols)
    demo.to_csv(DATA_PATH, index=False)

def ensure_csv():
    if DATA_PATH.exists():
        return
    # 1) Try real export from DB
    if try_export_from_db():
        return
    # 2) Fall back to seeded sample
    seed_demo_csv()

# Sidebar actions
with st.sidebar:
    st.header("Data")
    if st.button("Regenerate from DB"):
        if try_export_from_db():
            st.success("Exported from DB.")
        else:
            st.warning("DB export unavailable; seeded demo retained.")
    st.caption("If deploying on Streamlit Cloud without your SQLite DB, the app will show seeded demo data.")

# Ensure we have a CSV to load
ensure_csv()

@st.cache_data
def load_data() -> pd.DataFrame:
    try:
        df = pd.read_csv(DATA_PATH)
        # Coerce dtypes for safety
        df["Hours"] = pd.to_numeric(df.get("Hours", 0), errors="coerce").fillna(0.0)
        df["Points"] = pd.to_numeric(df.get("Points", 0), errors="coerce").fillna(0.0)
        if "Progress %" in df.columns:
            df["Progress %"] = pd.to_numeric(df["Progress %"], errors="coerce").fillna(0.0)
        return df
    except Exception as e:
        st.error(f"Failed to load {DATA_PATH.name}: {e}")
        return pd.DataFrame()

df = load_data()

# KPIs
col1, col2, col3, col4 = st.columns(4)
if not df.empty:
    total_hours = float(df["Hours"].sum())
    proj = df[df["Type"] == "Project"]
    avg_progress = float(proj["Progress %"].mean()) if not proj.empty and "Progress %" in proj else 0.0
    ex = df[df["Type"] == "Exercise"]
    exercises_done = int((ex["Exercise Name"].fillna("") != "").sum())
else:
    total_hours = avg_progress = exercises_done = 0.0

col1.metric("Total Hours Logged", f"{total_hours:.1f}")
col2.metric("Projects Avg Progress", f"{avg_progress:.1f}%")
col3.metric("Exercises Logged", f"{exercises_done}")
col4.metric("Rows", f"{len(df)}")

st.divider()

# Filters
c1, c2, c3 = st.columns(3)
types = ["All"] + (sorted(df["Type"].dropna().unique().tolist()) if not df.empty else [])
sel_type = c1.selectbox("Type", types, index=0)

projects = ["All"]
if not df.empty and "Project Name" in df:
    projects += sorted([p for p in df["Project Name"].dropna().unique() if str(p).strip()])
sel_project = c2.selectbox("Project", projects, index=0)

domains = ["All"]
if not df.empty and "Topic" in df:
    domains += sorted([d for d in df["Topic"].dropna().unique() if str(d).strip()])
sel_domain = c3.selectbox("Topic Area", domains, index=0)

# Apply filters
view = df.copy()
if sel_type != "All":
    view = view[view["Type"] == sel_type]
if sel_project != "All":
    view = view[view["Project Name"] == sel_project]
if sel_domain != "All":
    view = view[view["Topic"] == sel_domain]

st.subheader("Activity Log")
st.dataframe(view, use_container_width=True)

# Charts
if not view.empty:
    st.subheader("Hours by Type")
    st.bar_chart(view.groupby("Type")["Hours"].sum())

    if "Topic" in view and "Points" in view:
        st.subheader("Points by Topic")
        st.bar_chart(view.groupby("Topic")["Points"].sum())
