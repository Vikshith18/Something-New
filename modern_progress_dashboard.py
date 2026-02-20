import streamlit as st
import pandas as pd
from datetime import date
import os

st.set_page_config(page_title="Smart Progress Dashboard", layout="wide")

# Modern CSS Styling
st.markdown("""
<style>

body {
background-color: #f0f2f6;
}

h1 {
text-align:center;
color:white;
}

.header {
background: linear-gradient(90deg,#4A90E2,#6A5ACD);
padding:20px;
border-radius:15px;
text-align:center;
margin-bottom:20px;
}

.card {
background:white;
padding:20px;
border-radius:15px;
box-shadow: 0px 4px 10px rgba(0,0,0,0.1);
text-align:center;
}

.sidebar .sidebar-content {
background-color:#fafafa;
}

</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<div class="header"><h1>📊 Smart Daily Progress Dashboard</h1></div>', unsafe_allow_html=True)

FILE = "progress_data.csv"

# Load Data
if os.path.exists(FILE):
    df = pd.read_csv(FILE)
else:
    df = pd.DataFrame(columns=["Date","Task","Hours","Status"])


# Sidebar
st.sidebar.title("➕ Add Progress")

task = st.sidebar.text_input("Task")

hours = st.sidebar.number_input("Hours",0,12)

status = st.sidebar.selectbox(
"Status",
["Completed","In Progress","Missed"]
)

today = date.today()

if st.sidebar.button("Save"):

    new_data = pd.DataFrame({
        "Date":[today],
        "Task":[task],
        "Hours":[hours],
        "Status":[status]
    })

    df = pd.concat([df,new_data])

    df.to_csv(FILE,index=False)

    st.sidebar.success("Saved ✅")


# Statistics

st.subheader("📈 Dashboard Statistics")

col1,col2,col3 = st.columns(3)

total_hours = df["Hours"].sum()
completed = len(df[df["Status"]=="Completed"])
entries = len(df)

col1.metric("Total Hours", total_hours)
col2.metric("Completed Tasks", completed)
col3.metric("Total Entries", entries)


# Goal Section

st.subheader("🎯 Daily Goal")

goal = st.number_input("Set Goal (hours)",1,12,4)

today_hours = df[df["Date"]==str(today)]["Hours"].sum()

st.metric("Today's Hours", today_hours)

if today_hours >= goal:
    st.success("🔥 Goal Achieved!")

else:
    st.warning("Keep Working 💪")


# Streak Counter

st.subheader("🔥 Study Streak")

try:
    df["Date"] = pd.to_datetime(df["Date"])
    unique_dates = df["Date"].dt.date.unique()

    streak = len(unique_dates)

    st.metric("Days Active", streak)

except:
    st.write("No data yet")


# Table

st.subheader("📋 Progress History")

st.dataframe(df,use_container_width=True)


# Charts

st.subheader("📊 Study Hours Trend")

if len(df) > 0:
    chart = df.groupby("Date")["Hours"].sum()
    st.line_chart(chart)