import streamlit as st
import json
import matplotlib.pyplot as plt
import pandas as pd

import google.generativeai as genai

st.title("Environment Impact Analyzer🌿")
st.write("Welcome to Environment Impact Analyzer! This app provides analysis and recommendations based on environmental data.")

def load_data(file_name):
    with open(file_name, 'r') as json_file:
        return json.load(json_file)

with open("climate_data.json", "r") as f:
    climate_data = json.load(f)

with open("air_data.json", "r") as f:
    air_data = json.load(f)

with open("soil_data.json", "r") as f:
    soil_data = json.load(f)

# Load water quality data
with open("water_distance.json", "r") as f:
    water_data = json.load(f)

# Function to fetch climate data for a specific city
def fetch_climate_data(city):
    return climate_data.get(city, {})

# Function to filter climate data by variable
def filter_climate_by_variable(city_data, variable):
    filtered_data = {date: values[variable] for date, values in city_data.items()}
    return filtered_data

# Function to fetch air quality data for a specific city
def fetch_air_data(city):
    return air_data.get(city, {})

# Function to filter air quality data by variable
def filter_air_by_variable(city_data, variable):
    filtered_data = {date: values[variable] for date, values in city_data.items()}
    return filtered_data

# Function to create soil type visualization
def visualize_soil_data(soil_data):
    soil_types = {}
    for city, data in soil_data.items():
        soil_type = data.get("Soil Type", "Unknown")
        soil_types[soil_type] = soil_types.get(soil_type, 0) + 1

    labels = list(soil_types.keys())
    sizes = list(soil_types.values())

    # Plot pie chart
    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    st.subheader("Soil Type Distribution")
    st.pyplot(fig)

# Function to fetch water quality data for a specific city
def fetch_water_data(city):
    return water_data.get(city, {})
# Function to search for city details in the BST
def search_city_in_bst(city, bst):
    city_details = bst.search(city)
    single_line_output = ""
    formatted_output = ""
    if city_details:
        for data in city_details:
            # Extract key-value pairs and join them into a single line
            single_line_details = ', '.join([f"{key}:{value}" for key, value in data.items()])
            single_line_output += single_line_details + ", "
            # Add formatted JSON data
            formatted_output += json.dumps(data, indent=4) + "\n"
    else:
        single_line_output = f"No data found for {city} in the BST."
        formatted_output = single_line_output
    # Remove the trailing comma and space from the single line output
    single_line_output = single_line_output[:-2]
    return single_line_output, formatted_output

# Create a BST class for efficient searching
class TreeNode:
    def __init__(self, city):
        self.city = city
        self.data = []
        self.left = None
        self.right = None

class BST:
    def __init__(self):
        self.root = None

    def insert(self, city, data):
        self.root = self._insert(self.root, city, data)

    def _insert(self, node, city, data):
        if node is None:
            return TreeNode(city)
        if city < node.city:
            node.left = self._insert(node.left, city, data)
        elif city > node.city:
            node.right = self._insert(node.right, city, data)
        else:
            # Append the data to the existing list
            node.data.append(data)
        return node

    def search(self, city):
        return self._search(self.root, city)

    def _search(self, node, city):
        if node is None or node.city == city:
            return node.data
        if city < node.city:
            return self._search(node.left, city)
        else:
            return self._search(node.right, city)

# Function to format the output
def format_output(city_details):
    formatted_output = ""
    if city_details:
        for data in city_details:
            # Add formatted JSON data
            formatted_output += json.dumps(data, indent=4) + "\n"
    else:
        formatted_output = f"No data found for {city} in the BST."
    return formatted_output

# Sidebar inputs
with st.sidebar:
    st.header("Navigation")
    page = st.radio("Go to", ("Home", "Analysis", "Visualization"))

# Main page content
if page == "Home":
    st.write("The Environmental Impact Analyzer (EIA) app is a software tool designed to assess the potential environmental consequences of proposed projects or developments. It evaluates various factors such as air and water quality, pollution data, soil type, and social impacts to provide insights into the overall environmental footprint of the project. By analyzing data and simulating scenarios, the EIA app helps decision-makers identify potential risks, mitigate adverse effects, and make informed choices to promote sustainable development practices.")
elif page == "Analysis":
    st.header("Analysis")
    # Inputs for analysis
    city_name = st.text_input("Enter the city name:")
    business = st.text_input("Enter the business/activity:")
    start_d = st.text_input("Enter date range(start) YYYY-MM-DD:")
    end_d = st.text_input("Enter date range(end) YYYY-MM-DD:")
    fetch_data = st.button("Fetch Data")

    # Check if the Fetch Data button is clicked and all inputs are provided
    if fetch_data and city_name and business and start_d and end_d:
        # Load specified sorted JSON files
        specified_sorted_files = ['air_data.json','sorted_air_data_average.json','sorted_climate_data_average.json', 'sorted_soil_data.json', 'sorted_water_distance.json']

        # Create a BST and insert data from each specified JSON file
        bst = BST()
        for file_name in specified_sorted_files:
            data = load_data(file_name)
            for city, city_data in data.items():
                bst.insert(city, city_data)

        # Search for city details in the BST
        single_line_output, formatted_output = search_city_in_bst(city_name, bst)

        # Display formatted output
        st.subheader("Analysis Results")
        st.write(f"Average Environmental values for {city_name} from {start_d} to {end_d} :")
        st.code(formatted_output, language='json')

        # Configure Google Generative AI
        genai.configure(api_key='AIzaSyB3A0ISHESt50kC5avmRmyV3XyJwXHrb0U')
        model = genai.GenerativeModel('gemini-pro')

        # Generate content using Google Generative AI
        response = model.generate_content("First understand the format for the output(sample) provide atleast 6-7 points under all topic and also provide a para which contains what are all the impact that happens in the environment if the company has not taken any measures(have title as 'Impact in environment'): **Analysis of environment for starting Dye Industry in Coimbatore**  **Air Quality Index (AQI):** 4.2549 (Good) **Carbon Monoxide (CO):** 984.8654 mg/m³ (Good) **Nitrogen Oxides (NOx):** 3.6462 mg/m³ (Good) **Nitrogen Dioxide (NO2):** 24.8472 mg/m³ (Good) **Ozone (O3):** 31.0794 mg/m³ (Good) **Sulfur Dioxide (SO2):** 17.1078 mg/m³ (Good) **Particulate Matter (PM2.5):** 80.1122 µg/m³ (Moderate) **Particulate Matter (PM10):** 95.6116 µg/m³ (Moderate) **Ammonia (NH3):** 6.8263 mg/m³ (Good)  **Precautionary Measures(#6-7 points dont-print this text inside bracket)** * Regularly monitor air quality and take appropriate measures to reduce emissions if necessary.(0.4)  *  * Use low-emission technologies in the dyeing process to minimize air pollution.(0.2) * Control wastewater discharge to prevent contamination of water bodies.(0.1)  * Ensure proper waste management and disposal to prevent environmental hazards.(0.1)  **Recommendations for {}(#6-7 points-dont display the text inside bracket) **  * Invest in renewable energy sources to reduce carbon footprint.(0.4)   * Implement water conservation measures to minimize water usage and discharge.(0.3)  ** Establish partnerships with local environmental organizations to support sustainability initiatives.(0.2)  *  * Explore the use of sustainable dyes and materials to reduce environmental impact.(0.1)  **Additional Considerations(6-7 points)**  * **Alluvial soil:** Requires proper drainage to prevent waterlogging and pollution.  * **Inland location:** Less susceptible to coastal pollution but may experience temperature inversions that trap pollutants.  * **Primary water source (Noyyal):** Available at 41.26690226312544 Conclusion The environmental data for Coimbatore indicates good overall air quality but moderate levels of particulate matter. The precautionary measures and recommendations outlined above can help mitigate potential environmental impacts of a dye industry while promoting sustainability. # also some of the recommendations for business type provided. Now I want to start a {} in {}, you provide me the analysis of the given values, precautionary measures, and recommendations for my business (add weights for each of the measures and recommendations based on their usefulness) in the same format above, using the environmental data for {} as it is given as follows: {}".format(business, business, city_name, city_name, single_line_output))
        output = response.text
            # Display generated content
        st.subheader("Generated Recommendations")
        st.write(output)

        # Design separator
        st.markdown("---")

        # Generate Efficient Recommendations
        res2 = model.generate_content("In the following text of 6-7 points, you choose 3-4 points in each topic and give in detail, also give conclusion, also retain the title, Efficient recommendations and also provide a para which contains what are all the impact that happens in the environment if the company has not taken any measures(have title as 'Impact in environment') {}".format(output))
        efficient_recommendations = res2.text

        # Display efficient recommendations
        st.subheader("Efficient Recommendations")
        st.write(efficient_recommendations)

    elif fetch_data:
        st.error("Please fill in all the details.")
elif page == "Visualization":
    st.header("Explore the Trend📈")
    # Climate data section
    st.header("Climate Data🌦️")

    # Select city for climate data
    climate_cities = list(climate_data.keys())
    selected_climate_city = st.selectbox("Select City (Climate Data)", climate_cities)

    # Select variable for climate data
    climate_variables = ["temperature_mean", "temperature_max", "wind_speed_mean", "wind_speed_max",
                         "relative_humidity_mean", "relative_humidity_max", "dew_point_max"]
    selected_climate_variable = st.selectbox("Select Variable (Climate Data)", climate_variables)

    # Fetch and filter climate data
    climate_city_data = fetch_climate_data(selected_climate_city)
    filtered_climate_data = filter_climate_by_variable(climate_city_data, selected_climate_variable)

    # Display climate data
    if filtered_climate_data:
        # Display chart for climate data
        climate_df = pd.DataFrame.from_dict(filtered_climate_data, orient='index', columns=[selected_climate_variable])
        st.subheader("Climate Data Visualization")
        climate_fig, climate_ax = plt.subplots()
        climate_ax.plot(climate_df.index, climate_df[selected_climate_variable])
        climate_ax.set_xlabel("Date")
        climate_ax.set_ylabel(selected_climate_variable.replace("_", " ").title())
        st.pyplot(climate_fig)
    else:
        st.write("No climate data available for the selected city and variable.")

    # Air quality data section
    st.header("Air Quality Data💨")

    # Select city for air quality data
    air_cities = list(air_data.keys())
    selected_air_city = st.selectbox("Select City (Air Quality Data)", air_cities)

    # Select variable for air quality data
    air_variables = ["aqi", "co", "no", "no2", "o3", "so2", "pm2_5", "pm10", "nh3"]
    selected_air_variable = st.selectbox("Select Variable (Air Quality Data)", air_variables)

    # Fetch and filter air quality data
    air_city_data = fetch_air_data(selected_air_city)
    filtered_air_data = filter_air_by_variable(air_city_data, selected_air_variable)

    # Display air quality data
    if filtered_air_data:
        # Display chart for air quality data
        st.subheader("Air Quality Data Visualization")
        air_df = pd.DataFrame.from_dict(filtered_air_data, orient='index', columns=[selected_air_variable])
        fig, ax = plt.subplots()
        ax.bar(air_df.index, air_df[selected_air_variable], color='green')
        ax.set_xlabel("Date")
        ax.set_ylabel(selected_air_variable.upper())
        plt.xticks(rotation=45)
        st.pyplot(fig)
    else:
        st.write("No air quality data available for the selected city and variable.")

    # Soil type data section
    st.header("Soil Type Data🌱")

    # Display soil type visualization
    visualize_soil_data(soil_data)  

    # Water quality data section
    st.header("Water Quality Data💧")

    # Select city for water quality data
    water_cities = list(water_data.keys())
    selected_water_city = st.selectbox("Select City (Water Quality Data)", water_cities)

    # Fetch water quality data
    water_city_data = fetch_water_data(selected_water_city)

    # Display water quality data
    if water_city_data:
        st.subheader("Water Quality Information for {}".format(selected_water_city))
        st.write("Location: ", water_city_data.get("location", "Unknown"))
        st.write("Primary Source: ", water_city_data.get("primary_source", "Unknown"))
        st.write("Secondary Source: ", water_city_data.get("secondary_source", "Unknown"))
        st.write("Primary Source Distance: ", water_city_data.get("primary_source_distance", "Unknown"), " km")
        st.write("Secondary Source Distance: ", water_city_data.get("secondary_source_distance", "Unknown"), " km")
        st.write("Nearest Water Source: ", water_city_data.get("minimum distance", "Unknown"))
    else:
        st.write("No water quality data available for the selected city.")