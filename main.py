
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from src.preprocessing import get_cleaned_data

# Page Config
st.set_page_config(page_title="Expense Tracker", layout="wide")
st.title("💰 Expense Tracker & Financial Analytics")

# Load Data
df = get_cleaned_data()

# --- SIDEBAR FILTERS ---
st.sidebar.header("🔍 Filters")
category_list = df['Category'].unique().tolist()
selected_cat = st.sidebar.multiselect("Select Categories", category_list, default=category_list)
type_filter = st.sidebar.selectbox("Transaction Type", ["All", "Expense", "Income"])

# Filter Logic
filtered_df = df[df['Category'].isin(selected_cat)]
if type_filter != "All":
    filtered_df = filtered_df[filtered_df['Type'] == type_filter]

# --- KEY METRICS ---
col1, col2, col3 = st.columns(3)
total_inc = filtered_df[filtered_df['Type'] == 'Income']['Amount'].sum()
total_exp = filtered_df[filtered_df['Type'] == 'Expense']['Amount'].sum()
col1.metric("Total Income", f"₹{total_inc}")
col2.metric("Total Expense", f"₹{total_exp}")
col3.metric("Balance", f"₹{total_inc - total_exp}")

# --- VISUALIZATIONS ---
st.write("---")
row1_col1, row1_col2 = st.columns(2)

with row1_col1:
    st.subheader("📊 Category-wise Spending")
    cat_data = filtered_df[filtered_df['Type'] == 'Expense'].groupby('Category')['Amount'].sum()
    if not cat_data.empty:
        st.bar_chart(cat_data)
    else:
        st.write("No data found.")

with row1_col2:
    st.subheader("🍕 Expense Distribution")
    if not cat_data.empty:
        fig, ax = plt.subplots()
        ax.pie(cat_data, labels=cat_data.index, autopct='%1.1f%%', startangle=140)
        st.pyplot(fig)
    else:
        st.write("No data found.")

st.write("---")
st.subheader("📈 Monthly Trend")
monthly_trend = filtered_df.groupby('Month')['Amount'].sum()
st.line_chart(monthly_trend)

# --- DATA TABLE ---
if st.checkbox("Show Raw Data"):
    st.dataframe(filtered_df)