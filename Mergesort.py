import json

def merge_sort(arr):
    if len(arr) > 1:
        mid = len(arr) // 2
        left_half = arr[:mid]
        right_half = arr[mid:]

        merge_sort(left_half)
        merge_sort(right_half)

        i = j = k = 0
        while i < len(left_half) and j < len(right_half):
            if left_half[i]['city'] < right_half[j]['city']:
                arr[k] = left_half[i]
                i += 1
            else:
                arr[k] = right_half[j]
                j += 1
            k += 1

        while i < len(left_half):
            arr[k] = left_half[i]
            i += 1
            k += 1

        while j < len(right_half):
            arr[k] = right_half[j]
            j += 1
            k += 1

# Load data from JSON files
def load_json(file_name):
    with open(file_name, 'r') as json_file:
        return json.load(json_file)


#air_data_average = load_json('air_data_average.json')
#climate_data_average = load_json('climate_data_average.json')
#soil_data = load_json('soil_data.json')
water_distance = load_json('water_distance.json')

# Convert data to a list of dictionaries for sorting
def convert_to_list(data):
    return [{'city': city, 'data': data} for city, data in data.items()]

# Apply merge sort to each data list
data_lists = {
    
    #'air_data_average': convert_to_list(air_data_average),
    #'climate_data_average': convert_to_list(climate_data_average),
    #'soil_data': convert_to_list(soil_data),
    'water_distance': convert_to_list(water_distance),
}

sorted_data = {}
for key, data_list in data_lists.items():
    merge_sort(data_list)
    sorted_data[key] = {item['city']: item['data'] for item in data_list}

# Example: Print sorted data for each JSON file
for key, data in sorted_data.items():
    print(f"Sorted {key}:")
    for city, value in data.items():
        print(f"{city}: {value}")

# Optionally, save sorted data to new JSON files
for key, data in sorted_data.items():
    with open(f'sorted_{key}.json', 'w') as sorted_file:
        json.dump(data, sorted_file, indent=4)
