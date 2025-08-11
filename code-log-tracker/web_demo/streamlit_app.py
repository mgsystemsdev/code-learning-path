#!/usr/bin/env streamlit run

import pandas as pd
import streamlit as st

st.set_page_config(page_title="Learning Tracker (Demo)", layout="wide")
st.title("Learning Tracker – Demo View")

@st.cache_data
def load():
    try:
        return pd.read_csv("web_demo/demo_data.csv")
    except Exception:
        st.warning("No demo_data.csv found. Generate it via scripts/export_demo_data.py")
        return pd.DataFrame()

df = load()

# Top KPIs
col1, col2, col3, col4 = st.columns(4)
if not df.empty:
    total_hours = df["Hours"].sum()
    proj_rows = df[df["Type"]=="Project"]
    avg_progress = proj_rows["Progress %"].mean() if not proj_rows.empty else 0.0
    ex_rows = df[df["Type"]=="Exercise"]
    exercises_done = (ex_rows["Exercise Name"].notna() & (ex_rows["Exercise Name"].astype(str)!="")).sum()
else:
    total_hours = avg_progress = exercises_done = 0

col1.metric("Total Hours Logged", f"{total_hours:.1f}")
col2.metric("Projects Avg Progress", f"{avg_progress:.1f}%")
col3.metric("Exercises Logged", str(exercises_done))
col4.metric("Rows", str(len(df)))

st.divider()

# Filters
c1, c2, c3 = st.columns(3)
types = ["All"] + sorted(df["Type"].dropna().unique().tolist()) if not df.empty else ["All"]
sel_type = c1.selectbox("Type", types, index=0)

projects = ["All"]
if not df.empty:
    projects += sorted([p for p in df["Project Name"].dropna().unique() if p])
sel_project = c2.selectbox("Project", projects, index=0)

domains = ["All"]
if not df.empty:
    domains += sorted([d for d in df["Topic"].dropna().unique() if d])
sel_domain = c3.selectbox("Topic Area", domains, index=0)

# Apply filters
view = df.copy()
if sel_type != "All": view = view[view["Type"]==sel_type]
if sel_project != "All": view = view[view["Project Name"]==sel_project]
if sel_domain != "All": view = view[view["Topic"]==sel_domain]

# Table
st.subheader("Activity Log")
st.dataframe(view, use_container_width=True)

# Charts
if not view.empty:
    st.subheader("Hours by Type")
    st.bar_chart(view.groupby("Type")["Hours"].sum())

    st.subheader("Points by Topic")
    st.bar_chart(view.groupby("Topic")["Points"].sum())
