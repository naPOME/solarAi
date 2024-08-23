import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# Page Configuration
st.set_page_config(page_title="Solar and Weather Data Dashboard",
                   page_icon=":sun_with_face:",
                   layout="wide")

st.title("Solar and Weather Data Dashboard")

@st.cache_data
def load_data(file):
    # Check the file type and read accordingly
    if file.name.endswith('.xlsx'):
        data = pd.read_excel(file, engine='openpyxl')  # Use openpyxl for reading Excel files
    elif file.name.endswith('.csv'):
        data = pd.read_csv(file)  # Use read_csv for CSV files
    else:
        st.error("Unsupported file format. Please upload a CSV or Excel file.")
        st.stop()
    return data

# Sidebar for file upload
with st.sidebar:
    upload_file = st.file_uploader("Choose a file", type=["csv", "xlsx"])

    if upload_file is None:
        st.info("Please upload a file", icon="ℹ️")
        st.stop()

# Load the data
df = load_data(upload_file)

# Normalize column names to lowercase for easier comparison
df.columns = df.columns.str.lower()

# Display the first few rows of the dataframe for manual inspection
st.write("Preview of uploaded data:")
st.dataframe(df.head())

# Check for missing values
st.write("Missing values per column:")
st.write(df.isnull().sum())

# Calculate and display summary statistics for numeric columns
st.write("Summary Statistics:")
st.write(df.describe())

# Data Quality Check
st.write("Data Quality Check:")
for col in ['ghi', 'dni', 'dhi', 'moda', 'modb', 'ws', 'wsgust']:
    if col in df.columns:
        st.write(f"Checking column: {col}")
        st.write(f"Number of negative values in {col}:", (df[col] < 0).sum())
        st.write(f"Number of missing values in {col}:", df[col].isnull().sum())
        st.write(f"Outliers in {col} (values beyond 1.5*IQR):", df[(df[col] > (df[col].quantile(0.75) + 1.5 * (df[col].quantile(0.75) - df[col].quantile(0.25)))) | 
                                                                 (df[col] < (df[col].quantile(0.25) - 1.5 * (df[col].quantile(0.75) - df[col].quantile(0.25))))].shape[0])

# Time Series Analysis
st.write("Time Series Analysis:")
if 'timestamp' in df.columns:
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df.set_index('timestamp', inplace=True)

    # Plot GHI, DNI, DHI, and Tamb over time
    for col in ['ghi', 'dni', 'dhi', 'tamb']:
        if col in df.columns:
            st.subheader(f"{col.upper()} Over Time")
            fig = px.line(df, x=df.index, y=col, title=f"{col.upper()} Over Time")
            st.plotly_chart(fig, use_container_width=True)

# Evaluate the impact of cleaning on sensor readings
if 'cleaning' in df.columns and 'moda' in df.columns and 'modb' in df.columns:
    st.write("Impact of Cleaning on Sensor Readings:")
    cleaned_df = df[df['cleaning'] == 1]
    non_cleaned_df = df[df['cleaning'] == 0]

    for col in ['moda', 'modb']:
        if col in df.columns:
            st.subheader(f"Impact of Cleaning on {col.upper()}")
            fig = px.box([cleaned_df[col], non_cleaned_df[col]], labels={'variable': 'Cleaning Status', 'value': col.upper()})
            st.plotly_chart(fig, use_container_width=True)

# Correlation Analysis
st.write("Correlation Analysis:")
if {'ghi', 'dni', 'dhi', 'tmoda', 'tmodb'}.issubset(df.columns):
    correlation_matrix = df[['ghi', 'dni', 'dhi', 'tmoda', 'tmodb']].corr()
    st.write("Correlation Matrix:")
    st.write(correlation_matrix)
    fig = plt.figure(figsize=(10, 8))
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm')
    st.pyplot(fig)

# Wind Analysis
st.write("Wind Analysis:")
if {'ws', 'wsgust', 'wd'}.issubset(df.columns):
    st.subheader("Wind Speed and Direction Analysis")
    fig = px.scatter_polar(df, r='ws', theta='wd', color='wsgust', size='wsgust', title='Wind Speed and Direction Polar Plot')
    st.plotly_chart(fig, use_container_width=True)

# Temperature Analysis
st.write("Temperature Analysis:")
if {'rh', 'tamb'}.issubset(df.columns):
    st.subheader("Relative Humidity vs. Temperature")
    fig = px.scatter(df, x='rh', y='tamb', title='Relative Humidity vs. Temperature')
    st.plotly_chart(fig, use_container_width=True)

# Histograms
st.write("Histograms:")
for col in ['ghi', 'dni', 'dhi', 'ws', 'tamb']:
    if col in df.columns:
        st.subheader(f"Histogram of {col.upper()}")
        fig = px.histogram(df, x=col, title=f"Histogram of {col.upper()}")
        st.plotly_chart(fig, use_container_width=True)

# Z-Score Analysis
st.write("Z-Score Analysis:")
from scipy import stats

z_scores = pd.DataFrame()
for col in ['ghi', 'dni', 'dhi', 'ws', 'tamb']:
    if col in df.columns:
        df[f'z_{col}'] = np.abs(stats.zscore(df[col].dropna()))
        st.write(f"Z-Scores for {col}:")
        st.write(df[[col, f'z_{col}']].head())

# Bubble Charts
st.write("Bubble Charts:")
if {'ghi', 'tamb', 'ws', 'rh'}.issubset(df.columns):
    st.subheader("GHI vs. Tamb vs. WS with Bubble Size Representing RH")
    fig = px.scatter(df, x='ghi', y='tamb', size='rh', color='ws', title='GHI vs. Tamb vs. WS', labels={'ghi': 'GHI', 'tamb': 'Temperature', 'rh': 'Relative Humidity'})
    st.plotly_chart(fig, use_container_width=True)


st.write("Data Cleaning:")
if 'comments' in df.columns:
    st.write("Comments column data:")
    st.write(df['comments'].value_counts())
    df.dropna(subset=['comments'], inplace=True)


st.write("Cleaned Data Preview:")
st.dataframe(df.head())
