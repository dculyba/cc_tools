import json

with open("data/family.json", "r") as reader:
    family_data = json.load(reader)

print(family_data)