import streamlit as st
import pandas as pd
from flow import EmailFlow
# Load data
@st.cache_data
def load_data():
    df = pd.read_excel("emails_tracking.xlsx")
    return df

data = load_data()

# Convert date columns
data['Received Time (Application)'] = pd.to_datetime(data['Received Time (Application)'], errors='coerce')
data['Received Time (Rejection/Interview)'] = pd.to_datetime(data['Received Time (Rejection/Interview)'], errors='coerce')

# Sidebar Filters
st.sidebar.header("Filter Data")
start_date = st.sidebar.date_input("Start Date", data['Received Time (Application)'].min())
end_date = st.sidebar.date_input("End Date", data['Received Time (Application)'].max())
# app.py


# Sidebar with button
with st.sidebar:
    st.header("⚙️ Control Panel")
    run_flow = st.button("🔄 Update Emails")


#  Only create and run the flow after button is clicked
if run_flow:
    with st.spinner("Processing emails... Please wait..."):
        flow = EmailFlow()  # <-- created here, only after button press
        flow.kickoff()
    st.success("✅ Email flow completed!")

# Apply filters
filtered_data = data[
    (data['Received Time (Application)'] >= pd.to_datetime(start_date)) &
    (data['Received Time (Application)'] <= pd.to_datetime(end_date))
]
filtered_data_rejection = data[
    (data['Received Time (Application)'] >= pd.to_datetime(start_date)) &
    (data['Received Time (Application)'] <= pd.to_datetime(end_date)) &
    (data['Status'] == "Rejection")
]
filtered_data_acceptance = data[
    (data['Received Time (Application)'] >= pd.to_datetime(start_date)) &
    (data['Received Time (Application)'] <= pd.to_datetime(end_date)) &
    (data['Status']  == "Interview_Invitation")
]
# Show Data Table
st.title("📬 Email Tracker Dashboard")
st.subheader("Data Preview")
st.dataframe(filtered_data)


# Create 3 columns
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(
        f"""
        <div style="text-align: center;">
            <div style="
                width: 100px;
                height: 100px;
                background-color: #2196F3;
                border-radius: 50%;
                display: flex;
                justify-content: center;
                align-items: center;
                color: white;
                font-size: 24px;
                font-weight: bold;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
                margin: auto;
            ">
                {len(filtered_data)}
            </div>
            <p style="margin-top: 10px; color: #2196F3; font-weight: bold;">Applications</p>
        </div>
        """,
        unsafe_allow_html=True
    )

with col2:
    st.markdown(
        f"""
        <div style="text-align: center;">
            <div style="
                width: 100px;
                height: 100px;
                background-color: #f44336;
                border-radius: 50%;
                display: flex;
                justify-content: center;
                align-items: center;
                color: white;
                font-size: 24px;
                font-weight: bold;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
                margin: auto;
            ">
                {len(filtered_data_rejection)}
            </div>
            <p style="margin-top: 10px; color: #f44336; font-weight: bold;">Rejections</p>
        </div>
        """,
        unsafe_allow_html=True
    )

with col3:
    st.markdown(
        f"""
        <div style="text-align: center;">
            <div style="
                width: 100px;
                height: 100px;
                background-color: #4CAF50;
                border-radius: 50%;
                display: flex;
                justify-content: center;
                align-items: center;
                color: white;
                font-size: 24px;
                font-weight: bold;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
                margin: auto;
            ">
                {len(filtered_data_acceptance)}
            </div>
            <p style="margin-top: 10px; color: #4CAF50; font-weight: bold;">Acceptances</p>
        </div>
        """,
        unsafe_allow_html=True
    )