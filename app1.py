import json
import pathlib
import textwrap
import google.generativeai as genai

# Or use `os.getenv('GOOGLE_API_KEY')` to fetch an environment variable.
GOOGLE_API_KEY='AIzaSyB3A0ISHESt50kC5avmRmyV3XyJwXHrb0U'

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

# Load data from a sorted JSON file
def load_data(file_name):
    with open(file_name, 'r') as json_file:
        return json.load(json_file)

# List of specified sorted JSON files
specified_sorted_files = ['air_data.json','sorted_air_data_average.json','sorted_climate_data_average.json', 'sorted_soil_data.json', 'sorted_water_distance.json']

# Create a BST and insert data from each specified JSON file
bst = BST()
for file_name in specified_sorted_files:
    data = load_data(file_name)
    for city, city_data in data.items():
        bst.insert(city, city_data)

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

# Get input as city name
city_name = input("Enter the city name: ")
business = input("Enter the business/activity: ")
start_d = input("Enter date range(start) YYYY-MM-DD: ")
end_d = input("Enter date range(end) YYYY-MM-DD: ")
# Search for city details in the BST and store the outputs
single_line_output, formatted_output = search_city_in_bst(city_name, bst)

# Output the single-line output

# Output the formatted output
print("\nAverage Environmental values for {} from {} to {} :".format(city_name,start_d,end_d))
print(formatted_output)


genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-pro')

response = model.generate_content("First understand the format for the output(sample) provide atleast 6-7 points under all topic: **Analysis of environment for starting Dye Industry in Coimbatore**  **Air Quality Index (AQI):** 4.2549 (Good) **Carbon Monoxide (CO):** 984.8654 mg/m³ (Good) **Nitrogen Oxides (NOx):** 3.6462 mg/m³ (Good) **Nitrogen Dioxide (NO2):** 24.8472 mg/m³ (Good) **Ozone (O3):** 31.0794 mg/m³ (Good) **Sulfur Dioxide (SO2):** 17.1078 mg/m³ (Good) **Particulate Matter (PM2.5):** 80.1122 µg/m³ (Moderate) **Particulate Matter (PM10):** 95.6116 µg/m³ (Moderate) **Ammonia (NH3):** 6.8263 mg/m³ (Good)  **Precautionary Measures(#6-7 points dont-print this text inside bracket)** * Regularly monitor air quality and take appropriate measures to reduce emissions if necessary.(0.4)  *  * Use low-emission technologies in the dyeing process to minimize air pollution.(0.2) * Control wastewater discharge to prevent contamination of water bodies.(0.1)  * Ensure proper waste management and disposal to prevent environmental hazards.(0.1)  **Recommendations for {}(#6-7 points-dont display the text inside bracket) **  * Invest in renewable energy sources to reduce carbon footprint.(0.4)   * Implement water conservation measures to minimize water usage and discharge.(0.3)  ** Establish partnerships with local environmental organizations to support sustainability initiatives.(0.2)  *  * Explore the use of sustainable dyes and materials to reduce environmental impact.(0.1)  **Additional Considerations(6-7 points)**  * **Alluvial soil:** Requires proper drainage to prevent waterlogging and pollution.  * **Inland location:** Less susceptible to coastal pollution but may experience temperature inversions that trap pollutants.  * **Primary water source (Noyyal):** Available at 41.26690226312544  **Conclusion**  The environmental data for Coimbatore indicates good overall air quality but moderate levels of particulate matter. The precautionary measures and recommendations outlined above can help mitigate potential environmental impacts of a dye industry while promoting sustainability. # also some of the recommendations for business type provided. Now I want to start a {} in {}, you provide me the analysis of the given values, precautionary measures and recommendations for my business(add weights for each of the measures and recommendations based on their usefulness) in the same format above, using the environmental data for {} as it is given as follows: {}".format(business,business,city_name,city_name,single_line_output))
output = response.text
print(output)


print("--------------------------------------------------")
res2 = model.generate_content("In the following text of 6-7 points, you choose 3-4 points in each topic and give in detail, also give conclusion, also retain the title, {}".format(output))
print(res2.text)




