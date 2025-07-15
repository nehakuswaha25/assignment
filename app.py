import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns

# Set page configuration
st.set_page_config(layout="wide", page_title="Sleep & Health Lifestyle Dashboard")

# --- Title and Introduction ---
st.title("😴 Sleep & Health Lifestyle Dashboard 💡")
st.markdown("""
Welcome to your personalized dashboard for exploring sleep and health lifestyle data!
Use the sidebar to navigate and filter the data.
""")

# --- Data Loading ---
@st.cache_data # Cache the data loading for better performance
def load_data():
    """Loads the sleep_health.csv dataset."""
    try:
        df = pd.read_csv("sleep_health.csv")
        # Basic data cleaning/preparation: replace spaces with underscores and convert to lowercase
        df.columns = df.columns.str.replace(' ', '_').str.lower()
        return df
    except FileNotFoundError:
        st.error("Error: 'sleep_health.csv' not found. Please ensure the file is in the same directory as the app.")
        return pd.DataFrame() # Return empty DataFrame on error

df = load_data()

if not df.empty:
    st.sidebar.header("Data Filters & Options")

    # --- Sidebar Filters ---
    st.sidebar.subheader("Filter Data")

    # Filter by Gender
    gender_options = df['gender'].unique().tolist()
    selected_gender = st.sidebar.multiselect("Select Gender(s)", gender_options, default=gender_options)

    # Filter by Age Range
    min_age, max_age = int(df['age'].min()), int(df['age'].max())
    age_range = st.sidebar.slider("Select Age Range", min_age, max_age, (min_age, max_age))

    # Filter by BMI Category
    bmi_category_options = df['bmi_category'].unique().tolist()
    selected_bmi_category = st.sidebar.multiselect("Select BMI Category(ies)", bmi_category_options, default=bmi_category_options)

    # Apply filters
    filtered_df = df[
        (df['gender'].isin(selected_gender)) &
        (df['age'] >= age_range[0]) &
        (df['age'] <= age_range[1]) &
        (df['bmi_category'].isin(selected_bmi_category))
    ]

    if filtered_df.empty:
        st.warning("No data matches the selected filters. Please adjust your selections.")
    else:
        # --- Display Filtered Data ---
        st.subheader("Filtered Data Preview")
        st.dataframe(filtered_df.head())
        st.write(f"Displaying {len(filtered_df)} out of {len(df)} records.")

        st.subheader("Descriptive Statistics")
        st.write(filtered_df.describe())

        # --- Visualizations ---
        st.header("Data Visualizations")

        # Plot 1: Sleep Duration Distribution
        st.subheader("1. Sleep Duration Distribution")
        fig1 = px.histogram(filtered_df, x='sleep_duration', nbins=10,
                            title='Distribution of Sleep Duration',
                            labels={'sleep_duration': 'Sleep Duration (hours)'},
                            color_discrete_sequence=px.colors.qualitative.Pastel)
        st.plotly_chart(fig1, use_container_width=True)

        # Plot 2: Stress Level vs. Sleep Duration
        st.subheader("2. Stress Level vs. Sleep Duration")
        fig2 = px.scatter(filtered_df, x='sleep_duration', y='stress_level',
                          color='gender', size='daily_steps', hover_name='occupation',
                          title='Sleep Duration vs. Stress Level (by Gender & Daily Steps)',
                          labels={'sleep_duration': 'Sleep Duration (hours)', 'stress_level': 'Stress Level'},
                          color_discrete_sequence=px.colors.qualitative.Set2)
        st.plotly_chart(fig2, use_container_width=True)

        # Plot 3: Quality of Sleep by Occupation
        st.subheader("3. Quality of Sleep by Occupation")
        # Ensure 'occupation' and 'quality_of_sleep' exist
        if 'occupation' in filtered_df.columns and 'quality_of_sleep' in filtered_df.columns:
            avg_sleep_quality_by_occupation = filtered_df.groupby('occupation')['quality_of_sleep'].mean().sort_values(ascending=False).reset_index()
            fig3 = px.bar(avg_sleep_quality_by_occupation, x='occupation', y='quality_of_sleep',
                          title='Average Quality of Sleep by Occupation',
                          labels={'quality_of_sleep': 'Average Quality of Sleep (1-10)'},
                          color='occupation',
                          color_discrete_sequence=px.colors.qualitative.Vivid)
            st.plotly_chart(fig3, use_container_width=True)
        else:
            st.info("Columns 'occupation' or 'quality_of_sleep' not found for this visualization.")

        # Plot 4: Physical Activity Level by BMI Category
        st.subheader("4. Physical Activity Level by BMI Category")
        if 'physical_activity_level' in filtered_df.columns and 'bmi_category' in filtered_df.columns:
            fig4 = px.box(filtered_df, x='bmi_category', y='physical_activity_level',
                          title='Physical Activity Level by BMI Category',
                          labels={'physical_activity_level': 'Physical Activity Level (minutes)', 'bmi_category': 'BMI Category'},
                          color='bmi_category',
                          color_discrete_sequence=px.colors.qualitative.Bold)
            st.plotly_chart(fig4, use_container_width=True)
        else:
            st.info("Columns 'physical_activity_level' or 'bmi_category' not found for this visualization.")

        # --- Insights/Summary (Optional) ---
        st.header("Key Insights")
        st.write("""
        * **Sleep Duration:** Observe the most common sleep durations and how they vary across different demographics.
        * **Stress & Sleep:** Explore the relationship between reported stress levels and sleep duration. Higher stress often correlates with lower sleep duration or quality.
        * **Occupation Impact:** See if certain occupations tend to have different average sleep quality.
        * **BMI & Activity:** Understand how physical activity levels differ across various BMI categories.
        """)
