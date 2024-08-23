Solar and Weather Data Dashboard

Overview
The Solar and Weather Data Dashboard is a web application built using Streamlit, designed to provide interactive visualizations and analysis of solar radiation and weather data. This dashboard allows users to upload CSV or Excel files containing the relevant data, and it offers various analyses, including time series analysis, data quality checks, correlation analysis, and more.

Features
File Upload: Supports uploading data files in CSV or Excel format.
Data Preview: Displays a preview of the uploaded data.
Missing Values Detection: Identifies and reports missing values in the dataset.
Summary Statistics: Provides descriptive statistics for the dataset.
Data Quality Checks: Includes checks for negative values and outliers in specific columns.
Time Series Analysis: Visualizes solar radiation and temperature data over time.
Impact of Cleaning on Sensor Readings: Compares sensor readings before and after cleaning events.
Correlation Analysis: Displays the correlation matrix and heatmap for key variables.
Wind Analysis: Analyzes wind speed and direction using polar plots.
Temperature Analysis: Examines the relationship between relative humidity and temperature.
Histograms: Generates histograms with KDE plots for key variables.
Z-Score Analysis: Calculates and displays Z-scores to identify outliers.
Bubble Charts: Creates bubble charts to visualize relationships between variables.
Data Cleaning: Provides options for cleaning data, including handling of comments.
Getting Started
Prerequisites
Python 3.8 or higher
Virtual environment (recommended)
Installation
Clone the Repository:

bash
Copy code
git clone https://github.com/your-username/solar-weather-dashboard.git
cd solar-weather-dashboard
Create and Activate a Virtual Environment:

bash
Copy code
python3 -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
Install the Required Packages:

bash
Copy code
pip install -r requirements.txt
Run the Dashboard:

bash
Copy code
streamlit run app.py
Usage
Upload Data: On the sidebar, upload your CSV or Excel file containing solar and weather data.
Data Analysis: Use the various sections of the dashboard to perform analyses on the data, such as time series visualization, correlation analysis, and more.
Interactivity: The dashboard is interactive, allowing users to explore different aspects of the data dynamically.
File Format
The uploaded data should be in either CSV or Excel format and should include the following columns (case-insensitive):

timestamp: Date and time of the observation.
ghi: Global Horizontal Irradiance.
dni: Direct Normal Irradiance.
dhi: Diffuse Horizontal Irradiance.
moda, modb: Sensor readings.
ws: Wind speed.
wsgust: Wind gust speed.
wd: Wind direction.
tamb: Ambient temperature.
rh: Relative humidity.
cleaning: Binary column indicating if cleaning was performed.
Customization
To modify the dashboard or add new features, edit the app.py file. You can customize the visualizations, add new analyses, or change the layout as needed.

Project Structure
plaintext
Copy code
solar-weather-dashboard/
│
├── app.py                  # Main Streamlit application
├── requirements.txt        # Python dependencies
├── README.md               # Project documentation
└── .streamlit/
    └── config.toml         # Streamlit configuration file
Configuration
Streamlit can be configured using the config.toml file located in the .streamlit/ directory. You can set options like port number, theme, etc.
