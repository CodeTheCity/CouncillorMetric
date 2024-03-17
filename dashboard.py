import streamlit as st
import pandas as pd

# Load the CSV Data
@st.cache_data  # Caching the data load for efficiency 
def load_data():
    df = pd.read_csv("councillorsAttendance.csv")
        # Assuming you have 'Present' and 'Expected' columns:
    df['Attendance Percentage'] = (df['Present'] / df['Expected']) * 100
    df['Present Percent'] = df['Present Percent'].str.rstrip('%').astype(float)  # Remove %, convert to float
    df['Apologies Percent'] = df['Apologies Percent'].str.rstrip('%').astype(float)
    df['Absent Percent'] = df['Absent Percent'].str.rstrip('%').astype(float)
    return df

# Load the data once using caching
councillor_data = load_data()

# Dashboard header
st.title("Councillor Performance Dashboard")



# Display each councillor's information in a table
for index, row in councillor_data.iterrows():
    st.subheader(row["Name"])
    cols = st.columns(2)
    with cols[0]:
        st.image(row["Image"])
    with cols[1]:
        st.metric("Attendance Percentage", row["Attendance Percentage"], delta=None)
        st.write(row["Party"])
        st.write(row["Ward"])
        st.write("Date Running:", row["Date"])  
    attendance_data = {
        'Expected': row['Expected'],
        'Present': row['Present'],
        'Present Percent': f"{row['Present Percent']:.1f}%",  # Format with one decimal 
        'Apologies': row['Apologies'],
        'Apologies Percent': f"{row['Apologies Percent']:.1f}%",
        'Absent': row['Absent'],
        'Absent Percent': f"{row['Absent Percent']:.1f}%"
    }
    st.table(pd.DataFrame(attendance_data, index=[0]))  # Index added for clean display


