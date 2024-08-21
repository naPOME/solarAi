import streamlit as st
import pandas as pd

st.title('Solar Radiation Analysis')

# Load data
df1 = pd.read_csv('/home/pom/solar/data/sierraleone-bumbuna.csv')

# Display data
st.write(df1.head())

# Plot
st.line_chart(df1['GHI'])
selected_column = st.selectbox('Select a column to visualize', df1.columns)
st.line_chart(df1[selected_column])
