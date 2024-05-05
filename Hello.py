import streamlit as st
import pandas as pd
import plotly.express as px

# Page Configuration
st.set_page_config(page_title='Death Rate Dashboard', layout='wide')

# Load the data
@st.cache_data
def load_data():
    df = pd.read_csv('data/Death_rate.csv')
    # Normalize column names: remove spaces, convert to lowercase
    df.columns = [x.strip().replace(' ', '_').lower() for x in df.columns]
    # Rename 'entity' to 'Country' for better readability
    df.rename(columns={'entity': 'country'}, inplace=True)
    return df

data = load_data()

# Sidebar - User Inputs
st.sidebar.header('Filter Data')
try:
    # Range selector for years using a slider
    years = st.sidebar.slider("Select Year Range", min_value=int(data['year'].min()), 
                              max_value=int(data['year'].max()), value=(int(data['year'].min()), int(data['year'].max())))
    
    # Multiple country selection for comparative analysis, starts empty
    selected_countries = st.sidebar.multiselect('Select Countries', options=sorted(data['country'].unique()), 
                                                default=[])
except Exception as e:
    st.error(f"An error occurred: {e}")

# Filter data based on user selection
try:
    filtered_data = data[(data['year'] >= years[0]) & (data['year'] <= years[1]) & 
                         (data['country'].isin(selected_countries))]
except KeyError as e:
    st.error(f"Column not found: {e}")
    st.stop()

# Main page layout
st.title('Global Death Rates Due To Water Contaminants')
st.markdown("Between The Years 1990 And 2019")
if filtered_data.empty:
    st.write("Choose Data From The Selected Filters.")
else:
    if selected_countries:
        st.write(f"Data for {', '.join(selected_countries)} from {years[0]} to {years[1]}")
    else:
        st.write("Select one or more countries to display data.")

    # Visualization of Death Rate Trends over time
    st.header('Death Rate Over Time')
    if selected_countries and st.checkbox('Show Trend Chart', True):
        fig = px.line(filtered_data, x='year', y='unsafe_water_death_rate_per_100k', color='country',
                      labels={'unsafe_water_death_rate_per_100k': 'Unsafe water death rates per 100k'},
                      title='Unsafe Water Death Rate per 100k Trends')
        st.plotly_chart(fig, use_container_width=True)

    # Death Rate Visualization
    st.header('Unsafe Water Death Rate per 100k Comparison')
    if selected_countries and st.checkbox('Show Scatter Plot', True):
        fig2 = px.scatter(filtered_data, x='year', y='unsafe_water_death_rate_per_100k', color='country',
                          labels={'unsafe_water_death_rate_per_100k': 'Unsafe water death rates per 100k'},
                          title='Yearly Unsafe Water Death Rate per 100k Comparison')
        st.plotly_chart(fig2, use_container_width=True)

    # Regional Map Visualization
    st.header('Regional Death Rate Map')
    if selected_countries:
        map_fig = px.choropleth(filtered_data, locations="country", locationmode="country names",
                                color="unsafe_water_death_rate_per_100k",
                                hover_name="country", projection="natural earth",
                                labels={'unsafe_water_death_rate_per_100k': 'Unsafe water death rates per 100k'},
                                title="Regional Unsafe Water Death Rate per 100k")
        st.plotly_chart(map_fig, use_container_width=True)

    # Recommendations for Improving Global Death Rates
    st.header('Recommendations for Improving Global Death Rates')
    st.markdown("""
    - **Improved Water Infrastructure**: Invest in modernizing water supply and sanitation systems, especially in underdeveloped and developing regions. This includes the construction of new water treatment plants, renovation of old pipelines, and introduction of efficient sewage disposal systems to prevent water source contamination.
    - **Strict Regulation and Monitoring**: Implement strict water quality regulations and enforce them rigorously. This includes regular monitoring of water sources, treatment plants, and distribution systems to ensure compliance with safety standards.
    - **Community-Based Water Solutions**: Support and promote community-managed water systems which are often more sustainable and effective at a local level. This involves training local communities to manage their own water resources effectively, including testing and maintenance.
    - **Technology and Innovation**: Encourage the adoption of new technologies that can purify water more efficiently and cost-effectively. Innovations like portable water filters, solar desalination units, and chemical water treatment methods can provide safe drinking water in remote areas.
    - **Public Health Campaigns**: Increase awareness about the importance of safe drinking water and proper sanitation through public health campaigns. Educate communities about the dangers of water-borne diseases and promote behaviors that reduce risk, such as boiling water and proper handwashing.
    - **International Aid and Cooperation**: Foster international cooperation to fund and implement water safety projects in high-risk areas. Partnerships between governments, NGOs, and private sectors can mobilize resources necessary to address water contamination on a global scale.
    - **Research and Data Collection**: Conduct research to better understand the sources and types of water contamination and their health impacts. Use this data to tailor interventions more effectively and to track progress over time.
    """)

# Feedback # extra step :)
feedback = st.text_input("Leave Your Feedback")
if st.button("Submit Feedback"):
    with open("feedback.txt", "a") as f:
        f.write(f"{feedback}\n")
    st.success("Thank you for your feedback! Have a nice day")
