import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# Set page config
st.set_page_config(
    page_title="My Streamlit App",
    page_icon="📊",
    layout="wide"
)

# Add title and description
st.title("📊 Interactive Data Dashboard")
# Sidebar
st.sidebar.header("Dashboard Settings")

# Sample data
@st.cache_data
def load_data():
    # Generate sample data
    np.random.seed(42)
    dates = pd.date_range(start='2023-01-01', end='2023-12-31', freq='D')
    data = {
        'Date': dates,
        'Sales': np.random.normal(100, 20, len(dates)),
        'Traffic': np.random.normal(500, 100, len(dates)),
        'Category': np.random.choice(['A', 'B', 'C'], len(dates))
    }
    return pd.DataFrame(data)

df = load_data()

# Date range selector
date_range = st.sidebar.date_input(
    "Select Date Range",
    value=(df['Date'].min(), df['Date'].max()),
    min_value=df['Date'].min(),
    max_value=df['Date'].max()
)

# Category filter
selected_categories = st.sidebar.multiselect(
    "Select Categories",
    options=df['Category'].unique(),
    default=df['Category'].unique()
)

# Filter data
mask = (
    (df['Date'].dt.date >= date_range[0]) &
    (df['Date'].dt.date <= date_range[1]) &
    (df['Category'].isin(selected_categories))
)
filtered_df = df[mask]

# Create two columns
col1, col2 = st.columns(2)

with col1:
    st.subheader("Sales Over Time")
    fig_sales = px.line(
        filtered_df,
        x='Date',
        y='Sales',
        color='Category',
        title='Daily Sales by Category'
    )
    st.plotly_chart(fig_sales, use_container_width=True)

    # Summary statistics
    st.subheader("Summary Statistics")
    st.dataframe(
        filtered_df.describe(),
        use_container_width=True
    )

with col2:
    st.subheader("Traffic Analysis")
    fig_traffic = px.scatter(
        filtered_df,
        x='Sales',
        y='Traffic',
        color='Category',
        title='Sales vs Traffic by Category'
    )
    st.plotly_chart(fig_traffic, use_container_width=True)

    # Show raw data
    st.subheader("Raw Data")
    st.dataframe(
        filtered_df,
        use_container_width=True
    )

# Footer
st.markdown("---")
st.markdown("Created with ❤️ using Streamlit")

# Add some interactivity with buttons and text input
st.sidebar.markdown("---")
st.sidebar.subheader("Interactive Features")

if st.sidebar.button("Show Random Sample"):
    st.sidebar.dataframe(filtered_df.sample(5))

user_note = st.sidebar.text_area("Add a Note", "Type your notes here...")
if st.sidebar.button("Save Note"):
    st.sidebar.success("Note saved successfully!")
