import json

# read file
#with open('story_data.json', 'r') as myfile:
#   data=myfile.read()

# parse file
#scenes = json.loads(data)

# Loop through different scenes
#for data in scenes:
#   print(scenes[data]['intro'])
#   print(scenes[data]['story'])
#   print("END OF ", data)

file_path = 'data.json'

try:
    with open(file_path, 'r') as file:
        content = file.read()
except FileNotFoundError as e:
    print(f"FileNotFoundError: {e}")

print(content)