import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import numpy as np
from babel.numbers import format_currency

sns.set(style="dark")

# Menyiapkan daily_rent_df
def create_daily_rent_df(df):
    daily_rent_df = df.groupby(by="date_day").agg({
        "count": "sum"
    }).reset_index()
    return daily_rent_df

# Menyiapkan daily_casual_rent_df
def create_daily_casual_rent_df(df):
    daily_casual_rent_df = df.groupby(by="date_day").agg({
        "casual": "sum"
    }).reset_index()
    return daily_casual_rent_df

# Menyiapkan daily_registered_rent_df
def create_daily_registered_rent_df(df):
    daily_registered_rent_df = df.groupby(by="date_day").agg({
        "registered": "sum"
    }).reset_index()
    return daily_registered_rent_df
    
# Menyiapkan season_rent_df
def create_season_rent_df(df):
    season_rent_df = df.groupby(by="season")[["registered", "casual"]].sum().reset_index()
    return season_rent_df

# Menyiapkan monthly_rent_df
def create_monthly_rent_df(df):
    monthly_rent_df = df.groupby(by="month").agg({
        "count": "sum"
    })
    ordered_months = [
        "Jan", "Feb", "Mar", "Apr", "May", "Jun",
        "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"
    ]
    monthly_rent_df = monthly_rent_df.reindex(ordered_months, fill_value=0)
    return monthly_rent_df

# Menyiapkan weekday_rent_df
def create_weekday_rent_df(df):
    weekday_rent_df = df.groupby(by="weekday").agg({
        "count": "sum"
    }).reset_index()
    return weekday_rent_df

# Menyiapkan workingday_rent_df
def create_workingday_rent_df(df):
    workingday_rent_df = df.groupby(by="workingday").agg({
        "count": "sum"
    }).reset_index()
    return workingday_rent_df

# Menyiapkan holiday_rent_df
def create_holiday_rent_df(df):
    holiday_rent_df = df.groupby(by="holiday").agg({
        "count": "sum"
    }).reset_index()
    return holiday_rent_df

# Menyiapkan weather_rent_df
def create_weather_rent_df(df):
    weather_rent_df = df.groupby(by="weather_category").agg({
        "count": "sum"
    })
    return weather_rent_df

# Load cleaned data
data_df = pd.read_csv("DASHBOARD/day_dataset.csv")

datetime_columns = ["date_day"]
data_df.sort_values(by="date_day", inplace=True)
data_df.reset_index(inplace=True)

for column in datetime_columns:
    data_df[column] = pd.to_datetime(data_df[column])

# Filter data
min_date = data_df["date_day"].min()
max_date = data_df["date_day"].max()

with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("bike_uculs.jpg")
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label="Timeline",min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = data_df[(data_df["date_day"] >= str(start_date)) & (data_df["date_day"] <= str(end_date))]

# Menyiapkan berbagai dataframe
daily_rent_df = create_daily_rent_df(main_df)
daily_casual_rent_df = create_daily_casual_rent_df(main_df)
daily_registered_rent_df = create_daily_registered_rent_df(main_df)
season_rent_df = create_season_rent_df(main_df)
monthly_rent_df = create_monthly_rent_df(main_df)
weekday_rent_df = create_weekday_rent_df(main_df)
workingday_rent_df = create_workingday_rent_df(main_df)
holiday_rent_df = create_holiday_rent_df(main_df)
weather_rent_df = create_weather_rent_df(main_df)

# Dashboard
st.header("Bike Rentals Dashboard🚲:sparkles:")
st.subheader("Daily Rentals")

col1, col2, col3 = st.columns(3)
with col1:
    daily_rent_casual = daily_casual_rent_df["casual"].sum()
    st.metric("Casual User", value= daily_rent_casual)

with col2:
    daily_rent_registered = daily_registered_rent_df["registered"].sum()
    st.metric("Registered User", value= daily_rent_registered)
 
with col3:
    daily_rent_total = daily_rent_df["count"].sum()
    st.metric("Total User", value= daily_rent_total)

##Bike rentals performance 
st.subheader("Bike Rentals Performance")
main_df["month"] = pd.Categorical(main_df["month"], categories=
    ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"],
    ordered=True)

monthly_counts = main_df.groupby(by=["year", "month"], observed=True).agg({
       "count": "sum"
   }).reset_index()

fig_bike_rentals, ax = plt.subplots(figsize=(24, 10))
sns.lineplot(
    data = monthly_counts,
    x = "month",
    y = "count",
    hue = "year",
    palette = "Paired",
    marker = "o"
)
plt.xlabel(None)
plt.ylabel(None)
plt.xticks(fontsize=18)
plt.yticks(fontsize=18)
plt.title(f"Bike Rental Trends ({start_date} to {end_date})", fontsize=21)
plt.legend(title = "Year", loc = "upper right", fontsize = 16)
plt.gca().xaxis.grid(False)
st.pyplot(fig_bike_rentals)

##User performance
st.subheader("Users Performance")
metric_option = st.selectbox("Select Aggregation Type", ["sum", "max", "min", "mean"])

user_counts = main_df.groupby(by="year").agg({
    "casual": metric_option,
    "registered": metric_option
}).reset_index()

# Set the style
sns.set(style="whitegrid")

# Create a figure and axis
fig_users_performance, ax = plt.subplots(figsize=(24, 10))

# Plot the data using seaborn"s barplot
sns.barplot(data=user_counts, x="year", y="casual", color="skyblue", label="Casual Users")
sns.barplot(data=user_counts, x="year", y="registered", color="pink", label="Registered Users", bottom=user_counts["casual"])

# Add label and title
plt.xlabel(None)
plt.ylabel(None)
plt.xticks(fontsize=18)
plt.yticks(fontsize=18)
plt.title(f"Comparison of Bike Rentals between Casual and Registered Users ({metric_option})", fontsize=21)

# Add a legend
plt.legend(title = "User Type", loc = "upper right", fontsize = 16)

plt.grid(False)
st.pyplot(fig_users_performance)

##Weekday Rentals
st.subheader("Weekday Rentals")
weekday_counts = main_df.groupby(by="weekday").agg({
    "count": "sum",
}).reset_index()
weekday_counts_sorted = weekday_counts.sort_values(by="count", ascending=False)

sns.set(style="whitegrid")

fig_weekday, ax = plt.subplots(figsize=(24, 10))

sns.barplot(data = weekday_counts_sorted, x = "weekday", y = "count", color = "lightcoral")
plt.title("Total of Bike Rentals by Weekday", fontsize=21)
plt.xlabel(None)
plt.ylabel(None)
plt.xticks(fontsize=18)
plt.yticks(fontsize=18)

plt.grid(False)
st.pyplot(fig_weekday)

##Workingday and Holiday Rentals
st.subheader("Workingday and Holiday Rentals")
fig_work_holiday, ax = plt.subplots(nrows=1, ncols=2, figsize=(24, 10))

# Berdasarkan workingday
workingday_labels = ["Non-Workingday", "Workingday"]
ax[0].pie(main_df.groupby("workingday")["count"].sum(), 
          labels= workingday_labels,
          autopct='%1.1f%%',
          colors=["skyblue", "pink"],
          textprops={'fontsize': 18})
ax[0].set_title("Percentage of Bike Rental by Workingday", fontsize=21)
ax[0].set_xlabel(None)
ax[0].set_ylabel(None)

# Berdasarkan holiday
holiday_labels = ["Non-Holiday", "Holiday"]
ax[1].pie(main_df.groupby("holiday")["count"].sum(), 
          labels= holiday_labels, 
          autopct='%1.1f%%',
          colors=["skyblue", "pink"],
          textprops={'fontsize': 18})
ax[1].set_title("Percentage of Bike Rental by Holiday", fontsize=21)
ax[1].set_xlabel(None)
ax[1].set_ylabel(None)

plt.tight_layout()
st.pyplot(fig_work_holiday)

##Season and Weather Rentals
st.subheader("Season and Weather Rentals")
fig_season_weather, ax = plt.subplots(figsize=(24, 10))
sns.barplot(
    x="season",
    y="count",
    hue="weather_category",
    palette = "Paired",
    data = main_df)

plt.title("Bike Rentals Based on Weather Conditions and Seasons", fontsize = 21)
plt.xlabel(None)
plt.ylabel(None)
plt.xticks(fontsize=18)
plt.yticks(fontsize=18)
plt.legend(fontsize = 16)

st.pyplot(fig_season_weather)

##Correlation
st.subheader("Correlation")
fig_correlation, ax = plt.subplots(figsize=(24, 10))

correlation = main_df.corr(numeric_only=True)
mask = np.triu(np.ones_like(correlation, dtype=bool))

sns.heatmap(
    correlation,
    annot=True,
    mask=mask,
    cmap="mako",
    center=0,
    annot_kws={"size": 16},
    fmt=".2f")
plt.title("Correlation Heatmap", fontsize = 21)

st.pyplot(fig_correlation)