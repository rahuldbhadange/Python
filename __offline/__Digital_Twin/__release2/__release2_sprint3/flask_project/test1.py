import json
input_file = open('mock-data.json', 'r')
mock_data = json.load(input_file)
print(mock_data)