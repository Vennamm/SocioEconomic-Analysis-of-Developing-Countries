import streamlit as st
import pandas as pd
from pandas.api.types import is_numeric_dtype
import streamlit.components.v1 as components
import hiplot as hip
import plotly.express as px
import plotly.subplots as sp 

st.set_page_config(layout="wide")
file_path = 'https://raw.githubusercontent.com/Vennamm/SocioEconomic-Analysis-of-Developing-Countries/main/working_df.csv' 
data = pd.read_csv(file_path)

st.title("Socio-Economic Trend Analysis in Developing Countries")

st.sidebar.title("Navigation")
view = st.sidebar.radio("Select a View:", ["Country View", "Stats View", "Sandbox Mode", "Documentation"])

if view == "Country View":
    st.subheader("Country View")
    year = st.selectbox("Select a Year:", data['year'].unique())
    country = st.selectbox("Select a Country:", data['country'].unique())

    filtered_data = data[(data['country'] == country) & (data['year'] == year)]

    st.subheader("Key Metrics")
    if not filtered_data.empty:
        metrics = {
            "GDP per Capita (USD)": filtered_data['gdp_per_capita_usd'].values[0],
            "Population (Millions)": filtered_data['population_millions'].values[0],
            "Life Expectancy (Years)": filtered_data['life_expectancy_years'].values[0],
            "CO2 Emissions (Metric Tons)": filtered_data['co2_emissions_million_metric_tons'].values[0]
        }

        cols = st.columns(4)
        for i, (metric_name, metric_value) in enumerate(metrics.items()):
            with cols[i]:
                st.markdown(f"<div style='background-color: blue; color: white; padding: 20px; border-radius: 5px; text-align: center;'>{metric_name}: {metric_value}</div>", unsafe_allow_html=True)

    # # Second Row: Line Charts for Trends Over Years
    # st.subheader("Trends Over Years")
    # trend_cols = st.columns(3)

    # # Line chart for GDP per Capita
    # with trend_cols[0]:
    #     gdp_line_fig = px.line(data[data['country'] == country], x='year', y='gdp_per_capita_usd', 
    #                             title="GDP per Capita (USD) Over Years")
    #     st.plotly_chart(gdp_line_fig, use_container_width=True)

    # # Line chart for Population
    # with trend_cols[1]:
    #     population_line_fig = px.line(data[data['country'] == country], x='year', y='population_millions', 
    #                                    title="Population (Millions) Over Years")
    #     st.plotly_chart(population_line_fig, use_container_width=True)

    # # Line chart for Life Expectancy
    # with trend_cols[2]:
    #     life_expectancy_line_fig = px.line(data[data['country'] == country], x='year', y='life_expectancy_years', 
    #                                         title="Life Expectancy (Years) Over Years")
    #     st.plotly_chart(life_expectancy_line_fig, use_container_width=True)

    st.subheader("Distribution Insights")
    pie_cols = st.columns(3)

    with pie_cols[0]:
        energy_fig = px.pie(values=[filtered_data['energy_consumption_twh'].values[0] * (1 - filtered_data['renewable_energy_share'].values[0] / 100),
                                     filtered_data['energy_consumption_twh'].values[0] * (filtered_data['renewable_energy_share'].values[0] / 100)],
                                 names=['Non-Renewable', 'Renewable'],
                                 title="Energy Consumption",
                                 hole=0.3)  # Make it a donut chart
        energy_fig.update_traces(textposition='inside', textinfo='percent+label', textfont_size=12, showlegend=False)
        st.plotly_chart(energy_fig, use_container_width=True)

    with pie_cols[1]:
        education_expenditure = filtered_data['gdp_per_capita_usd'].values[0] * (filtered_data['education_expenditure_gdp'].values[0] / 100)
        healthcare_expenditure = filtered_data['healthcare_expenditure_per_capita_usd'].values[0]
        gdp_per_capita = filtered_data['gdp_per_capita_usd'].values[0]
        remaining_gdp_per_capita = gdp_per_capita - (education_expenditure + healthcare_expenditure)

        combined_fig = px.pie(values=[remaining_gdp_per_capita, education_expenditure, healthcare_expenditure],
                               names=['Remaining GDP per Capita', 'Education Expenditure', 'Healthcare Expenditure'],
                               title="Education and Healthcare Expenditure",
                               hole=0.3)  # Make it a donut chart
        combined_fig.update_traces(textposition='inside', textinfo='percent+label', textfont_size=12, showlegend=False)
        
        st.plotly_chart(combined_fig, use_container_width=True)

    with pie_cols[2]:
        agriculture_percentage = filtered_data['agriculture_hunting_forestry_fishing_pct_gross'].values[0]
        industry_percentage = filtered_data['industry_pct_gross'].values[0]
        services_percentage = filtered_data['services_pct_gross'].values[0]
        
        sectors_fig = px.pie(values=[agriculture_percentage, industry_percentage, services_percentage],
                              names=['Agriculture', 'Industry', 'Services'],
                              title="Economic Sectors Distribution",
                              hole=0.3)  # Make it a donut chart
        sectors_fig.update_traces(textposition='inside', textinfo='percent+label', textfont_size=12, showlegend=False)
        
        st.plotly_chart(sectors_fig, use_container_width=True)
    
    adoption_data = data[data['country'] == country].groupby('year')[['internet_penetration', 'smartphone_adoption']].sum().reset_index()

    
    bar_fig = px.bar(adoption_data, x='year', y=['internet_penetration', 'smartphone_adoption'], 
                     title="Internet Penetration and Smartphone Adoption Over Years",
                     barmode='group')

    bar_fig.for_each_trace(lambda t: t.update(yaxis='y2') if t.name == 'smartphone_adoption' else ())

    bar_fig.update_layout(
        title="Internet Penetration and Smartphone Adoption Over Time",
        xaxis_title="Year",
        barmode='group', 
        height=500, 
        legend_title="",
        template='plotly_white',
        yaxis=dict(
            title='',   
            range=[0, 100] 
        ),
        yaxis2=dict(
            title='',      
            overlaying='y',
            side='left',
            range=[0, 100]
        ),
        
        legend=dict(
            x=0.5,           
            y=1.1,           
            orientation='h', 
            xanchor='center' 
        )
    )

    imp_exp_data = data[data['country'] == country].groupby('year')[['imports_millions_usd', 'exports_millions_usd']].sum().reset_index()
    imports_exports_fig = px.bar(
        imp_exp_data,
        x='year',
        y=['imports_millions_usd', 'exports_millions_usd'],  
        title="Imports vs Exports Over Time",
        labels={'value': 'Value (in Millions USD)', 'year': 'Year'},
        barmode='group', 
    )
    
    imports_exports_fig.update_layout(
        xaxis_title="Year",
        yaxis_title="Value (in Millions USD)",
        legend_title="",
        width=1000,      
        height=500,
        template='plotly_white',
        legend=dict(
            x=0.5,            
            y=1.1,            
            orientation='h', 
            xanchor='center'  
        )
    )

    col1, col2 = st.columns(2)

    with col1:
        st.plotly_chart(bar_fig, use_container_width=True)
    with col2:
        st.plotly_chart(imports_exports_fig, use_container_width=True)

    st.subheader("HDI and Various Indices Over Years")

    country_data = data[data['country'] == country]

    hdi_fig = px.line(country_data, 
                       x='year', 
                       y=['hdi', 'gender_equality_index'], 
                       title="HDI and Gender Equality Index Over Years",
                       # labels={'value': },
                       color_discrete_sequence=['blue', 'orange'])  

    hdi_fig.update_layout(
        xaxis_title="Year",
        yaxis_title="",
        legend_title="",
        legend=dict(
            x=0.5,         
            y=1.1,           
            orientation='h', 
            xanchor='center' 
        )
    )
    
    indices_fig = px.line(country_data, 
                           x='year', 
                           y=['corruption_perception_index', 'freedom_of_press_index'], 
                           title="Corruption Perception Index and Freedom of Press Index Over Years",
                           labels={'value': 'Index Value'},
                           color_discrete_sequence=['green', 'red']) 
    indices_fig.update_layout(
        xaxis_title="Year",
        yaxis_title="",
        legend_title="",
        legend=dict(
            x=0.5,         
            y=1.1,         
            orientation='h',  
            xanchor='center'
        )
    )
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(hdi_fig, use_container_width=True)
    with col2:
        st.plotly_chart(indices_fig, use_container_width=True)
elif view == "Stats View":
    st.subheader("Stats View")
    
    all_countries = data['country'].unique()
    selected_countries = st.multiselect("Select Countries:", options=all_countries, default=all_countries)
    
    min_year, max_year = int(data['year'].min()), int(data['year'].max())
    selected_years = st.slider("Select Year Range:", min_value=min_year, max_value=max_year, value=(min_year, max_year))

    filtered_data = data[(data['country'].isin(selected_countries)) & 
                         (data['year'].between(selected_years[0], selected_years[1]))]

    st.subheader("Unemployment Insights")
    unemployment_cols = st.columns(2)

    with unemployment_cols[0]:
        fig_pop_unemp = px.scatter(filtered_data, x='population_growth_rate', y='unemployment_rate', 
                                    color='country', title="Population Growth Rate vs Unemployment Rate")
        fig_pop_unemp.update_layout(width=600, height=400)
        st.plotly_chart(fig_pop_unemp)

    with unemployment_cols[1]:
        fig_pov_unemp = px.scatter(filtered_data, x='poverty_rate', y='unemployment_rate', 
                                    color='country', title="Poverty Rate vs Unemployment Rate")
        fig_pov_unemp.update_layout(width=600, height=400)
        st.plotly_chart(fig_pov_unemp)

    st.subheader("CO2 Emissions Insights")
    co2_cols = st.columns(2)

    with co2_cols[0]:
        fig_co2_forest = px.scatter(filtered_data, x='co2_emissions_million_metric_tons', y='forest_coverage', 
                                     color='country', title="CO2 Emissions vs Forest Coverage")
        st.plotly_chart(fig_co2_forest, use_container_width=True)

    with co2_cols[1]:
        fig_co2_energy = px.scatter(filtered_data, x='co2_emissions_million_metric_tons', y='energy_consumption_twh', 
                                     color='country', title="CO2 Emissions vs Energy Consumption")
        st.plotly_chart(fig_co2_energy, use_container_width=True)

    st.subheader("Poverty Rate Insights")
    poverty_cols = st.columns(2)

    with poverty_cols[0]:
        fig_pov_military = px.scatter(filtered_data, x='poverty_rate', y='military_expenditure_billion_usd', 
                                       color='country', title="Poverty Rate vs Military Expenditure")
        fig_pov_military.update_yaxes(type='log')  # Log scale for Military Expenditure
        st.plotly_chart(fig_pov_military)

    with poverty_cols[1]:
        fig_pov_inf = px.scatter(filtered_data, x='poverty_rate', y='inflation_rate', 
                                 color='country', title="Poverty Rate vs Inflation Rate")
        st.plotly_chart(fig_pov_inf)

    st.subheader("Corruption Insights")
    corruption_cols = st.columns(2)
    
    with corruption_cols[0]:
        fig_corruption = px.scatter(filtered_data, x='corruption_perception_index', y='freedom_of_press_index', 
                                     color='country', title="Corruption Perception Index vs Freedom of Press Index")
        st.plotly_chart(fig_corruption)

    avg_voting_data = (data[data['year'].between(selected_years[0], selected_years[1])]
                       .groupby('country')['voting_participation_rate'].mean().reset_index())

    avg_voting_data = avg_voting_data.sort_values(by='voting_participation_rate', ascending=False) 

    with corruption_cols[1]:
        avg_voting_fig = px.bar(avg_voting_data, x='country', y='voting_participation_rate', 
                                 title="Average Voting Participation Rate by Country",
                                 color='voting_participation_rate',
                                 color_continuous_scale='Blues') 
        st.plotly_chart(avg_voting_fig)

elif view == "Sandbox Mode":
    st.subheader("Sandbox Mode")

    countries = st.multiselect("Select Countries", options=data['country'].unique(), default=data['country'].unique())
    years = st.slider("Select Year Range", min_value=int(data['year'].min()), max_value=int(data['year'].max()), value=(int(data['year'].min()), int(data['year'].max())))
    
    metrics = [col for col in data.columns if is_numeric_dtype(data[col]) and col not in ['year', 'country']]  
    selected_metrics = st.multiselect("Select Metrics", metrics)

    filtered_data = data[(data['country'].isin(countries)) & (data['year'].between(*years))]
    
    if len(selected_metrics) == 1:
        log_scale = st.checkbox("Apply Log Scale to Y-Axis")
        metric = selected_metrics[0]
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig_line = px.line(
                filtered_data, 
                x='year', 
                y=metric, 
                color='country', 
                log_y=log_scale, 
                title=f"{metric} over the Years"
            )
            st.plotly_chart(fig_line, use_container_width=True)
    
        with col2:
            avg_metric = filtered_data.groupby('country')[metric].mean().reset_index()
            fig_pie = px.pie(
                avg_metric, 
                values=metric, 
                names='country', 
                title=f"Average {metric} by Country"
            )
            st.plotly_chart(fig_pie, use_container_width=True)
    
    elif len(selected_metrics) == 2:
        log_scale = st.checkbox("Apply Log Scale to Y-Axis")
        
        x_metric, y_metric = selected_metrics
    
        fig_scatter = px.scatter(filtered_data, x=x_metric, y=y_metric, color='country', log_y=log_scale, title=f"{x_metric} vs {y_metric}")
        fig_scatter.update_layout(height=600, width=900) 
        st.plotly_chart(fig_scatter, use_container_width=True)
    
    elif len(selected_metrics) == 3:
        x_metric, y_metric, z_metric = selected_metrics

        fig_3d = px.scatter_3d(filtered_data, x=x_metric, y=y_metric, z=z_metric, color='country', title=f"3D Plot: {x_metric} vs {y_metric} vs {z_metric}")
        fig_3d.update_layout(height=800, width=900) 
        st.plotly_chart(fig_3d, use_container_width=True)
    
    elif len(selected_metrics) > 3:

        hiplot_data = filtered_data[['country'] + selected_metrics].dropna()

        experiment = hip.Experiment.from_dataframe(hiplot_data)
        # ret_val = experiment.to_streamlit(ret="selected_uids", key="hip").display()

        # st.markdown("hiplot returned " + json.dumps(ret_val))
        st.display(experiments)
        # hip_exp = hip.Experiment.display_st(experiment)

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
    The Country View allows users to explore key performance indicators (KPIs) for each country in a specific year.

    #### Features:
    - **Country Selection**: Users can select a specific country from a dropdown menu.
    - **Year Selection**: A slider is provided to filter data based on the selected year.
    - **KPIs Display**: The following key performance indicators are displayed in square blocks:
      - GDP per Capita
      - Population
      - Life Expectancy
      - CO2 Emissions
    - **Pie Charts**:
      - Energy Consumption - Renewable vs Non-renewable
      - Expenditure - HealthCare vs Education vs Military vs Others
      - Economic Sector Distribution - Gross Contribution. 
    - **Bar Charts**:
      - Internet Penetrations and Smartphone Adoptions
      - Imports vs Exports
    - **Line Graphs**:
      - Comparison of Social Indicators.
    
    ---
    
    ### 2. Stats View
    The Stats View provides an analytical perspective on the relationships between various metrics across selected countries.
    
    #### Features:
    - **Country Selection**: All countries are selected by default, with an option for users to remove any countries from the selection.
    - **Year Slider**: Users can specify a range of years to filter the data.
    - **Predetermined Graphs**: The following relationships are visualized:
      - **First Row**:
        - Population Growth Rate vs. Unemployment Rate
        - Poverty Rate vs. Unemployment Rate 
      - **Second Row**:
        - CO2 Emissions vs. Forest Coverage
        - CO2 Emissions vs. Energy Consumption
      - **Third Row**:
        - Poverty Rate vs. Military Expenditure
        - Poverty Rate vs. Inflation Rate
      - **Fourth Row**:
        - Corruption Perception Index vs. Freedom of Press (Scatter Plot)
        - Average Voting Participation Rate (Bar Chart sorted by average participation)
    
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
      - **More than 3 Metrics**: Displays a parallel plot that allows users to play around with the data. Hue still represents country.
    - **Log Scale Filter**: An option to apply log scaling to the y-axis for better interpretation of data distributions.
    
    ---
    
    ### Conclusion
    This dashboard serves as a valuable tool for exploring and analyzing the complex relationships between various economic and social indicators across different countries and time periods. Users are encouraged to interact with the data and gain insights relevant to their areas of interest.

    #### Authors - Vaibhav Reddy Vennam. 
    
    You can find this whole project on my [GitHub](https://github.com/Vennamm/SocioEconomic-Analysis-of-Developing-Countries/tree/main). Feel free to contact me on GitHub or my [email](mailto:vaibhav.vennam@gmail.com), if you would like me to add more visualizations :)
    """

    st.markdown(doc_text)
