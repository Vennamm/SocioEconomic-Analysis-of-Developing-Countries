import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.subplots as sp

st.set_page_config(layout="wide")
# Load the dataset beforehand
file_path = 'working_df.csv'  # Change this to the path of your dataset
data = pd.read_csv(file_path)

# Title of the app
st.title("Data Dashboard")


# Navigation Sidebar
st.sidebar.title("Navigation")
view = st.sidebar.radio("Select a View:", ["Country View", "Stats View", "Sandbox Mode", "Documentation"])

if view == "Country View":
    # Country View
    st.subheader("Country View")

    # Year selector
    year = st.selectbox("Select a Year:", data['year'].unique())

    # Country selector
    country = st.selectbox("Select a Country:", data['country'].unique())

    # Filter data for the selected country and year
    filtered_data = data[(data['country'] == country) & (data['year'] == year)]

    # First Row: Key Metrics
    st.subheader("Key Metrics")
    if not filtered_data.empty:
        metrics = {
            "GDP per Capita (USD)": filtered_data['gdp_per_capita_usd'].values[0],
            "Population (Millions)": filtered_data['population_millions'].values[0],
            "Life Expectancy (Years)": filtered_data['life_expectancy_years'].values[0]
        }

        # Create blue squares with white text for key metrics
        cols = st.columns(3)
        for i, (metric_name, metric_value) in enumerate(metrics.items()):
            with cols[i]:
                st.markdown(f"<div style='background-color: blue; color: white; padding: 20px; border-radius: 5px; text-align: center;'>{metric_name}: {metric_value}</div>", unsafe_allow_html=True)

    # Second Row: Line Charts for Trends Over Years
    st.subheader("Trends Over Years")
    trend_cols = st.columns(3)

    # Line chart for GDP per Capita
    with trend_cols[0]:
        gdp_line_fig = px.line(data[data['country'] == country], x='year', y='gdp_per_capita_usd', 
                                title="GDP per Capita (USD) Over Years")
        st.plotly_chart(gdp_line_fig, use_container_width=True)

    # Line chart for Population
    with trend_cols[1]:
        population_line_fig = px.line(data[data['country'] == country], x='year', y='population_millions', 
                                       title="Population (Millions) Over Years")
        st.plotly_chart(population_line_fig, use_container_width=True)

    # Line chart for Life Expectancy
    with trend_cols[2]:
        life_expectancy_line_fig = px.line(data[data['country'] == country], x='year', y='life_expectancy_years', 
                                            title="Life Expectancy (Years) Over Years")
        st.plotly_chart(life_expectancy_line_fig, use_container_width=True)

    # Third Row: Pie Charts
    st.subheader("Distribution Insights")
    pie_cols = st.columns(3)

    # First Pie Chart for Energy Consumption
    with pie_cols[0]:
        energy_fig = px.pie(values=[filtered_data['energy_consumption_twh'].values[0] * (1 - filtered_data['renewable_energy_share'].values[0] / 100),
                                     filtered_data['energy_consumption_twh'].values[0] * (filtered_data['renewable_energy_share'].values[0] / 100)],
                                 names=['Non-Renewable', 'Renewable'],
                                 title="Energy Consumption",
                                 hole=0.3)  # Make it a donut chart
        energy_fig.update_traces(textposition='inside', textinfo='percent+label', textfont_size=12, showlegend=False)
        st.plotly_chart(energy_fig, use_container_width=True)

    # Second Pie Chart for Education Expenditure
    with pie_cols[1]:
        education_fig = px.pie(values=[filtered_data['gdp_trillions_usd'].values[0] * (1 - filtered_data['education_expenditure_gdp'].values[0] / 100),
                                        filtered_data['gdp_trillions_usd'].values[0] * (filtered_data['education_expenditure_gdp'].values[0] / 100)],
                                  names=['Non-Education', 'Education Expenditure'],
                                  title="Education Expenditure",
                                  hole=0.3)  # Make it a donut chart
        education_fig.update_traces(textposition='inside', textinfo='percent+label', textfont_size=12, showlegend=False)
        st.plotly_chart(education_fig, use_container_width=True)

    # Third Pie Chart for Healthcare Expenditure
    with pie_cols[2]:
        healthcare_expenditure = filtered_data['healthcare_expenditure_per_capita_usd'].values[0]
        gdp_per_capita = filtered_data['gdp_per_capita_usd'].values[0]
        healthcare_fig = px.pie(values=[healthcare_expenditure, gdp_per_capita - healthcare_expenditure],
                                 names=['Healthcare Expenditure', 'Remaining GDP per Capita'],
                                 title="Healthcare Expenditure",
                                 hole=0.3)  # Make it a donut chart
        healthcare_fig.update_traces(textposition='inside', textinfo='percent+label', textfont_size=12, showlegend=False)
        st.plotly_chart(healthcare_fig, use_container_width=True)

    # Fourth Row: Side-by-Side Bar Chart for Internet and Smartphone Adoption
    st.subheader("Internet and Smartphone Adoption Over Years")
    adoption_data = data[data['country'] == country].groupby('year')[['internet_penetration', 'smartphone_adoption']].sum().reset_index()
    bar_fig = px.bar(adoption_data, x='year', y=['internet_penetration', 'smartphone_adoption'], 
                     title="Internet Penetration and Smartphone Adoption Over Years",
                     barmode='group')

    # Set the maximum value of the y-axis for Smartphone Adoption to 100
    bar_fig.for_each_trace(lambda t: t.update(yaxis='y2') if t.name == 'smartphone_adoption' else ())

    # Create a second y-axis for smartphone adoption
    bar_fig.update_layout(
        yaxis2=dict(
            title='Smartphone Adoption',
            overlaying='y',
            side='right',
            range=[0, 100]  # Set the maximum value of the y-axis for smartphone adoption to 100
        )
    )

    st.plotly_chart(bar_fig)

    # Fifth Row: Line Chart for Various Indices
    st.subheader("HDI and Various Indices Over Years")

    # Filter the data for the selected country
    country_data = data[data['country'] == country]

    # Create the first figure for HDI and Gender Equality Index
    hdi_fig = px.line(country_data, 
                       x='year', 
                       y=['hdi', 'gender_equality_index'], 
                       title="HDI and Gender Equality Index Over Years",
                       labels={'value': 'Index Value'},
                       color_discrete_sequence=['blue', 'orange'])  # Custom colors for HDI and Gender Equality Index

    # Create the second figure for Corruption Perception Index and Freedom of Press Index
    indices_fig = px.line(country_data, 
                           x='year', 
                           y=['corruption_perception_index', 'freedom_of_press_index'], 
                           title="Corruption Perception Index and Freedom of Press Index Over Years",
                           labels={'value': 'Index Value'},
                           color_discrete_sequence=['green', 'red']) 
    st.plotly_chart(hdi_fig)
    st.plotly_chart(indices_fig)
elif view == "Stats View":
    st.subheader("Stats View")
    
    # Country Multiselector for Stats View
    all_countries = data['country'].unique()
    selected_countries = st.multiselect("Select Countries:", options=all_countries, default=all_countries)
    
    # Year slider
    min_year, max_year = int(data['year'].min()), int(data['year'].max())
    selected_years = st.slider("Select Year Range:", min_value=min_year, max_value=max_year, value=(min_year, max_year))

    # Filter data based on selections
    filtered_data = data[(data['country'].isin(selected_countries)) & 
                         (data['year'].between(selected_years[0], selected_years[1]))]

    # First Row: Unemployment Graphs
    st.subheader("Unemployment Insights")
    unemployment_cols = st.columns(2)

    # Population Growth Rate vs Unemployment Rate
    with unemployment_cols[0]:
        fig_pop_unemp = px.scatter(filtered_data, x='population_growth_rate', y='unemployment_rate', 
                                    color='country', title="Population Growth Rate vs Unemployment Rate")
        fig_pop_unemp.update_layout(width=600, height=400)
        st.plotly_chart(fig_pop_unemp)

    # Poverty Rate vs Unemployment Rate
    with unemployment_cols[1]:
        fig_pov_unemp = px.scatter(filtered_data, x='poverty_rate', y='unemployment_rate', 
                                    color='country', title="Poverty Rate vs Unemployment Rate")
        fig_pov_unemp.update_layout(width=600, height=400)
        st.plotly_chart(fig_pov_unemp)

    # Second Row: CO2 Emissions Insights
    st.subheader("CO2 Emissions Insights")
    co2_cols = st.columns(2)

    # CO2 Emissions vs Forest Coverage
    with co2_cols[0]:
        fig_co2_forest = px.scatter(filtered_data, x='co2_emissions_million_metric_tons', y='forest_coverage', 
                                     color='country', title="CO2 Emissions vs Forest Coverage")
        st.plotly_chart(fig_co2_forest)

    # CO2 Emissions vs Energy Consumption
    with co2_cols[1]:
        fig_co2_energy = px.scatter(filtered_data, x='co2_emissions_million_metric_tons', y='energy_consumption_twh', 
                                     color='country', title="CO2 Emissions vs Energy Consumption")
        st.plotly_chart(fig_co2_energy)

    # Third Row: Poverty Rate Insights
    st.subheader("Poverty Rate Insights")
    poverty_cols = st.columns(2)

    # Poverty Rate vs Military Expenditure
    with poverty_cols[0]:
        fig_pov_military = px.scatter(filtered_data, x='poverty_rate', y='military_expenditure_billion_usd', 
                                       color='country', title="Poverty Rate vs Military Expenditure")
        fig_pov_military.update_yaxes(type='log')  # Log scale for Military Expenditure
        st.plotly_chart(fig_pov_military)

    # Poverty Rate vs Inflation Rate (moved to third row)
    with poverty_cols[1]:
        fig_pov_inf = px.scatter(filtered_data, x='poverty_rate', y='inflation_rate', 
                                 color='country', title="Poverty Rate vs Inflation Rate")
        st.plotly_chart(fig_pov_inf)

    # Fourth Row: Corruption and Voting Participation
    st.subheader("Corruption Insights")
    corruption_cols = st.columns(2)

    # Corruption Perception Index vs Freedom of Press Index
    with corruption_cols[0]:
        fig_corruption = px.scatter(filtered_data, x='corruption_perception_index', y='freedom_of_press_index', 
                                     color='country', title="Corruption Perception Index vs Freedom of Press Index")
        st.plotly_chart(fig_corruption)

    # Average Voting Participation Rate
    avg_voting_data = (data[data['year'].between(selected_years[0], selected_years[1])]
                       .groupby('country')['voting_participation_rate'].mean().reset_index())

    avg_voting_data = avg_voting_data.sort_values(by='voting_participation_rate', ascending=False)  # Sort by average participation

    with corruption_cols[1]:
        avg_voting_fig = px.bar(avg_voting_data, x='country', y='voting_participation_rate', 
                                 title="Average Voting Participation Rate by Country",
                                 color='voting_participation_rate',
                                 color_continuous_scale='Blues')  # Different shades of blue
        st.plotly_chart(avg_voting_fig)

elif view == "Sandbox Mode":
    st.subheader("Sandbox Mode")

    # Country selection
    countries = data['country'].unique()
    selected_countries = st.multiselect("Select Countries:", countries, default=countries)

    # Year slider
    year_range = data['year'].unique()
    start_year, end_year = st.slider("Select Year Range:", min_value=int(year_range.min()), max_value=int(year_range.max()), 
                                       value=(int(year_range.min()), int(year_range.max())))

    # Metric selection
    all_metrics = [
        'gdp_per_capita_usd', 'population_millions', 'life_expectancy_years', 
        'healthcare_expenditure_per_capita_usd', 'energy_consumption_twh', 
        'gdp_trillions_usd', 'internet_penetration', 'smartphone_adoption', 
        'military_expenditure_billion_usd', 'co2_emissions_million_metric_tons',
        'corruption_perception_index', 'freedom_of_press_index', 'voting_participation_rate',
        'tourism_revenue_billion_usd', 'exports_millions_usd', 'imports_millions_usd'
    ]

    selected_metrics = st.multiselect("Select Metrics:", all_metrics)

    # Log scale option
    log_scale = st.checkbox("Apply Log Scale")

    # Filter data based on selected countries and years
    filtered_data = data[(data['country'].isin(selected_countries)) & 
                         (data['year'].between(start_year, end_year))]

    # Check if any metrics are selected
    if selected_metrics:
        if len(selected_metrics) == 1:
            metric = selected_metrics[0]
            # Line chart for the selected metric over the years
            line_fig = px.line(filtered_data, x='year', y=metric, color='country', 
                               title=f"{metric.replace('_', ' ').title()} Over Years")
            st.plotly_chart(line_fig, use_container_width=True)

            # Average value pie chart
            avg_value = filtered_data.groupby('country')[metric].mean().reset_index()
            pie_fig = px.pie(avg_value, values=metric, names='country', 
                              title=f"Average {metric.replace('_', ' ').title()} in Selected Years", hole=0.3)
            pie_fig.update_traces(textposition='inside', textinfo='percent+label', textfont_size=12, showlegend=False)
            st.plotly_chart(pie_fig, use_container_width=True)

        elif len(selected_metrics) == 2:
            # Scatter plot for the selected metrics
            scatter_fig = px.scatter(filtered_data, x=selected_metrics[0], y=selected_metrics[1], 
                                     color='country', title=f"{selected_metrics[0].replace('_', ' ').title()} vs {selected_metrics[1].replace('_', ' ').title()}")
            if log_scale:
                scatter_fig.update_yaxes(type='log')
            st.plotly_chart(scatter_fig, use_container_width=True)

        elif len(selected_metrics) == 3:
            # 3D scatter plot for the selected metrics
            scatter_3d_fig = px.scatter_3d(filtered_data, x=selected_metrics[0], 
                                             y=selected_metrics[1], z=selected_metrics[2], 
                                             color='country',
                                             title=f"{selected_metrics[0].replace('_', ' ').title()}, {selected_metrics[1].replace('_', ' ').title()}, and {selected_metrics[2].replace('_', ' ').title()} in 3D")
            st.plotly_chart(scatter_3d_fig, use_container_width=True)

elif view == "Documentation":
    st.subheader("Documentation")
    doc_text = """
    # Dashboard Documentation

    ## Overview
    This dashboard provides a comprehensive view of various indicators across multiple countries over time. Users can explore different metrics, visualize relationships between them, and gain insights into trends and patterns in data.

    ## Navigation
    The dashboard consists of three main views:

    1. **Country View**
    2. **Stats View**
    3. **Sandbox Mode**

    ---

    ### 1. Country View
    The Country View allows users to explore key performance indicators (KPIs) for selected countries over the chosen year range.

    #### Features:
    - **Country Selection**: Users can select a specific country from a dropdown menu, with the option to view data for all countries.
    - **Year Slider**: A slider is provided to filter data based on the selected year range.
    - **KPIs Display**: The following key performance indicators are displayed in square blocks:
      - GDP per Capita
      - Population
      - Life Expectancy
      - Healthcare Expenditure per Capita
      - Internet Penetration
      - Military Expenditure
      - CO2 Emissions
    - **Graphs**: Visualizations include:
      - Line graphs for key metrics over time.
      - Pie charts for healthcare expenditure breakdown.
      - Bar charts and scatter plots for various indicators.
    
    ---
    
    ### 2. Stats View
    The Stats View provides an analytical perspective on the relationships between various metrics across selected countries.
    
    #### Features:
    - **Country Selection**: All countries are selected by default, with an option for users to remove any countries from the selection.
    - **Year Slider**: Users can specify a range of years to filter the data.
    - **Predetermined Graphs**: The following relationships are visualized:
      - **First Row**:
        - Population Growth Rate vs. Unemployment Rate (Scatter Plot)
        - CO2 Emissions vs. Forest Coverage (Scatter Plot)
        - CO2 Emissions vs. Energy Consumption (Scatter Plot)
        - Poverty Rate vs. Military Expenditure (Scatter Plot)
      - **Second Row**:
        - Corruption Perception Index vs. Freedom of Press (Scatter Plot)
        - Average Voting Participation Rate (Bar Chart sorted by average participation)
    - **Customization**: Users can apply a log scale to the y-axis of military expenditure for better visualization.
    
    ---
    
    ### 3. Sandbox Mode
    The Sandbox Mode offers a flexible environment for users to explore multiple metrics simultaneously.
    
    #### Features:
    - **Metric Selection**: Users can select from all available metrics, with the ability to select one, two, or three metrics for analysis.
    - **Country Selection**: Similar to other views, users can select specific countries and a year range.
    - **Visualizations**:
      - **One Metric**: Displays a line chart of the metric over the years and a pie chart showing the average value of the metric for selected years.
      - **Two Metrics**: Shows a scatter plot comparing the two selected metrics, with hue representing the country.
      - **Three Metrics**: Displays a 3D scatter plot of the three selected metrics, again with hue representing the country.
    - **Log Scale Filter**: An option to apply log scaling to the y-axis for better interpretation of data distributions.
    
    ---
    
    ### Conclusion
    This dashboard serves as a valuable tool for exploring and analyzing the complex relationships between various economic and social indicators across different countries and time periods. Users are encouraged to interact with the data and gain insights relevant to their areas of interest.

    Authors - Beyonce, Vaibhav Reddy Vennam.
    """

    # Display the documentation in the Streamlit app
    st.markdown(doc_text)
#    st.write("This section will contain documentation and instructions.")
