import streamlit as st
import pandas as pd
import plotly
import plotly.express as px

# Set page configuration
st.set_page_config(page_title='Death Rate Dashboard', layout='wide')

@st.cache_data

def load_data():
    """Load and preprocess data."""
    try:
        df = pd.read_csv('data/Death_rate.csv')
        df.columns = [x.strip().replace(' ', '_').lower() for x in df.columns]
        df.rename(columns={'entity': 'country'}, inplace=True)
        return df
    except FileNotFoundError:
        st.error("Failed to load data. Check the file path.")
        return pd.DataFrame()

data = load_data()

if not data.empty:
    st.sidebar.header('Filter Data')
    years = st.sidebar.slider("Select Year Range", int(data['year'].min()), int(data['year'].max()), 
                              (int(data['year'].min()), int(data['year'].max())))
    selected_countries = st.sidebar.multiselect('Select Countries', sorted(data['country'].unique()))

    filtered_data = data[(data['year'] >= years[0]) & (data['year'] <= years[1]) & (data['country'].isin(selected_countries))]

    st.title('Global Death Rates Due To Water Contaminants')
    st.markdown("Between The Years 1990 And 2019")

    if not filtered_data.empty:
        if selected_countries:
            st.write(f"Data for {', '.join(selected_countries)} from {years[0]} to {years[1]}")
        else:
            st.write("Select one or more countries to display data.")

        fig = px.line(filtered_data, x='year', y='unsafe_water_death_rate_per_100k', color='country',
                      title='Unsafe Water Death Rate per 100k Trends')
        st.plotly_chart(fig, use_container_width=True)

        map_fig = px.choropleth(filtered_data, locations="country", locationmode="country names",
                                color="unsafe_water_death_rate_per_100k", hover_name="country",
                                title="Regional Unsafe Water Death Rate per 100k")
        st.plotly_chart(map_fig, use_container_width=True)
    else:
        st.write("No data available for the selected filters.")
else:
    st.write("Data is not available or could not be loaded.")

# Feedback section
feedback = st.text_input("Your Feedback")
if st.button("Submit Feedback"):
    with open("feedback.txt", "a") as f:
        f.write(f"{feedback}\n")
    st.success("Thank you for your feedback! Have a nice day")
