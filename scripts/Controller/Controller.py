import os
import time
import json

# Create the Json library
json_array = []
i = 1
dictionary = {}
while i < 200:
    dictionary["name"] = "dsadasd"
    json_array.append(dictionary.copy())
    dictionary.clear()
    i=i+1
with open('gameLibrary.json', 'w') as games:
    json.dump(json_array, games)
