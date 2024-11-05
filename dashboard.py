import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(layout="wide")

# Load datasets
df_day = pd.read_csv('data/bike-sharing-day.csv')
df_hour = pd.read_csv('data/bike-sharing-hour.csv')

# Sidebar configuration
with st.sidebar:
    st.image("data/bike-rent.png", width=300)
    st.title("Bike Rent Dashboard")
    st.header("Filters")
    selected_year = st.selectbox("Select Year", [2011, 2012])
    selected_dataset = st.radio("Select Data", ["Daily", "Hourly"])
    st.caption('© Muhammad Farhan Juna 2024')


# Select dataset based on user choice
df = df_day if selected_dataset == "Daily" else df_hour
filtered_df = df[df['year'] == selected_year]

# Calculate total bike rentals
total_rentals = filtered_df['count'].sum()

# Display total rentals at the top
st.title("Bike Sharing Analysis Dashboard")

# Tab layout for different sections
tab1, tab2, tab3, tab4 = st.tabs([
    "Average Rentals by Day of Week",
    "Seasonal Rentals for Casual & Registered Users",
    "Temperature vs. Total Rentals",
    "Humidity vs. Total Rentals"
])
st.markdown(f"### Total Bike Rentals for {selected_dataset} Data in {selected_year}: **{total_rentals:,}**")

with tab1:
    st.header("Average Bike Rentals by Day of the Week")
    day_of_week_rentals = filtered_df.groupby('day_of_week')['count'].mean().reset_index()
    fig, ax = plt.subplots()
    sns.barplot(x='day_of_week', y='count', data=day_of_week_rentals, ax=ax, palette="viridis")
    ax.set_xlabel("Day of the Week")
    ax.set_ylabel("Average Total Rentals")
    st.pyplot(fig)

    st.write("### Data Table")
    st.dataframe(
        day_of_week_rentals.style.set_properties(**{
            'background-color': 'black',
            'color': 'white'
        })
    )

with tab2:
    st.header("Total Bike Rentals by Season for Casual and Registered Users")
    seasonal_user_rentals = filtered_df.groupby('season')[['casual', 'registered']].sum().reset_index()
    fig, ax = plt.subplots()
    sns.barplot(x='season', y='casual', data=seasonal_user_rentals, label='Casual', ax=ax, color='skyblue')
    sns.barplot(x='season', y='registered', data=seasonal_user_rentals, label='Registered', ax=ax, color='salmon')
    ax.set_xlabel("Season")
    ax.set_ylabel("Total Rentals")
    plt.legend()
    st.pyplot(fig)

    st.write("### Data Table")
    st.dataframe(
        seasonal_user_rentals.style.set_properties(**{
            'background-color': 'black',
            'color': 'white'
        })
    )

with tab3:
    st.header("Relationship Between Temperature and Total Bike Rentals")
    fig, ax = plt.subplots()
    sns.scatterplot(x='temp', y='count', data=filtered_df, ax=ax, color='orange', edgecolor="w", linewidth=0.5)
    ax.set_xlabel("Normalized Temperature (temp)")
    ax.set_ylabel("Total Rentals (count)")
    st.pyplot(fig)

with tab4:
    st.header("Relationship Between Humidity and Total Bike Rentals")
    fig, ax = plt.subplots()
    sns.scatterplot(x='humidity', y='count', data=filtered_df, ax=ax, color='cyan', edgecolor="w", linewidth=0.5)
    ax.set_xlabel("Normalized Humidity (humidity)")
    ax.set_ylabel("Total Rentals (count)")
    st.pyplot(fig)
