import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency

sns.set(style='darkgrid')

# Helper functions for data preparation

def create_season_weather_df(df):
    # Group data by season and weather conditions
    season_weather_df = df.groupby(['season', 'weathersit']).agg({
        'cnt': 'mean'
    }).reset_index()
    return season_weather_df

def create_weekday_weekend_df(df):
    # Group data by weekend/weekday
    weekday_weekend_df = df.groupby('weekend')['cnt'].mean().reset_index()
    return weekday_weekend_df

# Load cleaned data
df = pd.read_csv("dashboard/bike_df.csv")
df['dteday'] = pd.to_datetime(df['dteday'])

# Streamlit sidebar for date selection
min_date = df['dteday'].min()
max_date = df['dteday'].max()

with st.sidebar:
    # Date input for filtering
    start_date, end_date = st.date_input(
        label='Date Range', 
        min_value=min_date, 
        max_value=max_date, 
        value=[min_date, max_date]
    )

# Filter data by date range
filtered_df = df[(df['dteday'] >= pd.to_datetime(start_date)) & 
                 (df['dteday'] <= pd.to_datetime(end_date))]

# Prepare dataframes for visualizations
season_weather_df = create_season_weather_df(filtered_df)
weekday_weekend_df = create_weekday_weekend_df(filtered_df)

# Main Title
st.header("Bike Sharing Data Analysis")

# Visualization 1: Bicycle Use by Season and Weather Conditions
st.subheader("Average Bicycle Use by Season and Weather Conditions")

fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(x='season', y='cnt', hue='weathersit', data=season_weather_df, palette='Blues', ax=ax)
ax.set_title('Average Bike Rentals by Season and Weather', fontsize=16)
ax.set_xlabel('Season', fontsize=12)
ax.set_ylabel('Average Count of Rentals', fontsize=12)
st.pyplot(fig)

# Visualization 2: Bicycle Use on Weekdays vs. Weekends
st.subheader("Average Bicycle Use on Weekdays vs. Weekends")

fig, ax = plt.subplots(figsize=(8, 6))
sns.barplot(x='weekend', y='cnt', data=weekday_weekend_df, palette='Purples', ax=ax)
ax.set_title('Average Rentals: Weekdays vs. Weekends', fontsize=16)
ax.set_xlabel('Day Type', fontsize=12)
ax.set_ylabel('Average Count of Rentals', fontsize=12)
st.pyplot(fig)

st.caption("Data sourced from bike-sharing dataset")
