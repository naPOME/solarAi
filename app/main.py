import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
from scipy import stats

st.set_page_config(page_title="Solar and Weather Data Dashboard",
                   page_icon=":sun_with_face:",
                   layout="wide")

st.title("Solar and Weather Data Dashboard")

@st.cache_data
def load_data(file):
    if file.name.endswith('.xlsx'):
        data = pd.read_excel(file, engine='openpyxl')  
    elif file.name.endswith('.csv'):
        data = pd.read_csv(file)  
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

df.columns = df.columns.str.lower()

# Display data preview
st.write("Preview of uploaded data:")
st.dataframe(df.head())

# Display missing values per column
st.write("Missing values per column:")
st.write(df.isnull().sum())

# Display summary statistics 
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

# Dashboard Metrics
st.write("### Dashboard Metrics")
col1, col2, col3, col4 = st.columns(4)

# Displaying Total GHI
if 'ghi' in df.columns:
    total_ghi = df['ghi'].sum()
    col1.metric("Total GHI", f"{total_ghi:.2f} kWh/m²")

# Displaying Total DNI
if 'dni' in df.columns:
    total_dni = df['dni'].sum()
    col2.metric("Total DNI", f"{total_dni:.2f} kWh/m²")

# Displaying Total DHI
if 'dhi' in df.columns:
    total_dhi = df['dhi'].sum()
    col3.metric("Total DHI", f"{total_dhi:.2f} kWh/m²")

# Displaying Average Temperature
if 'tamb' in df.columns:
    avg_temp = df['tamb'].mean()
    col4.metric("Avg Temperature", f"{avg_temp:.2f} °C")

# Additional columns for other metrics
col5, col6 = st.columns(2)

# Displaying Average Wind Speed
if 'ws' in df.columns:
    avg_ws = df['ws'].mean()
    col5.metric("Avg Wind Speed", f"{avg_ws:.2f} m/s")

# Displaying Total Cleaning Events
if 'cleaning' in df.columns:
    total_cleaning = df['cleaning'].sum()
    col6.metric("Total Cleaning Events", f"{total_cleaning}")

# Time Series Analysis
st.write("### Time Series Analysis:")
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
    st.write("### Impact of Cleaning on Sensor Readings:")
    cleaned_df = df[df['cleaning'] == 1]
    non_cleaned_df = df[df['cleaning'] == 0]

    for col in ['moda', 'modb']:
        if col in df.columns:
            st.subheader(f"Impact of Cleaning on {col.upper()}")
            fig = plt.figure(figsize=(10, 6))
            sns.boxplot(data=[cleaned_df[col], non_cleaned_df[col]], palette="Set2")
            plt.title(f'Impact of Cleaning on {col.upper()}')
            plt.xlabel('Cleaning Status')
            plt.ylabel(col.upper())
            st.pyplot(fig)

# Correlation Analysis
st.write("### Correlation Analysis:")
if {'ghi', 'dni', 'dhi', 'tmoda', 'tmodb'}.issubset(df.columns):
    correlation_matrix = df[['ghi', 'dni', 'dhi', 'tmoda', 'tmodb']].corr()
    st.write("Correlation Matrix:")
    st.write(correlation_matrix)
    fig = plt.figure(figsize=(10, 8))
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm')
    st.pyplot(fig)

# Wind Analysis
st.write("### Wind Analysis:")
if {'ws', 'wsgust', 'wd'}.issubset(df.columns):
    st.subheader("Wind Speed and Direction Analysis")
    fig = plt.figure(figsize=(10, 6))
    ax = fig.add_subplot(111, polar=True)
    ax.scatter(df['wd'], df['ws'], c=df['wsgust'], s=df['wsgust'], cmap='viridis', alpha=0.75)
    ax.set_title('Wind Speed and Direction Polar Plot')
    st.pyplot(fig)

# Temperature Analysis
st.write("### Temperature Analysis:")
if {'rh', 'tamb'}.issubset(df.columns):
    st.subheader("Relative Humidity vs. Temperature")
    fig = px.scatter(df, x='rh', y='tamb', title='Relative Humidity vs. Temperature')
    st.plotly_chart(fig, use_container_width=True)

# Histograms
st.write("### Histograms:")
for col in ['ghi', 'dni', 'dhi', 'ws', 'tamb']:
    if col in df.columns:
        st.subheader(f"Histogram of {col.upper()}")
        fig = plt.figure(figsize=(10, 6))
        sns.histplot(df[col], kde=True, color='blue')
        plt.title(f'Histogram of {col.upper()}')
        plt.xlabel(col.upper())
        plt.ylabel('Frequency')
        st.pyplot(fig)

# Z-Score Analysis
st.write("### Z-Score Analysis:")
z_scores = pd.DataFrame()
for col in ['ghi', 'dni', 'dhi', 'ws', 'tamb']:
    if col in df.columns:
        df[f'z_{col}'] = np.abs(stats.zscore(df[col].dropna()))
        st.write(f"Z-Scores for {col}:")
        st.write(df[[col, f'z_{col}']].head())

# Bubble Charts
st.write("### Bubble Charts:")
if {'ghi', 'tamb', 'ws', 'rh'}.issubset(df.columns):
    st.subheader("GHI vs. Tamb vs. WS with Bubble Size Representing RH")
    fig = px.scatter(df, x='ghi', y='tamb', size='rh', color='ws', title='GHI vs. Tamb vs. WS', labels={'ghi': 'GHI', 'tamb': 'Temperature', 'rh': 'Relative Humidity'})
    st.plotly_chart(fig, use_container_width=True)

# Data Cleaning
st.write("### Data Cleaning:")
if 'comments' in df.columns:
    st.write("Comments column data:")
    st.write(df['comments'].value_counts())
    df.dropna(subset=['comments'], inplace=True)

# Final cleaned dataframe preview
st.write("### Cleaned Data Preview:")
st.dataframe(df.head())
