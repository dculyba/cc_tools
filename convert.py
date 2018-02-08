import cc_dat_utils
import example_data
import example_json_utils
import json

#Part 1
#Use cc_data_utils.make_cc_data_from_dat() to load pfgd_test.dat
# cc_dat = cc_dat_utils.make_cc_data_from_dat("data/pfgd_test.dat")
# print(cc_dat)
#print the resulting data


#Part 2 Example
#Making the data structure manually
myFam = example_data.Family()
myFam.parent1 = "Dave"
myFam.parent2 = "Sabrina"

myKid = example_data.Kid()
myKid.name = "Hazel"
myKid.age = 4
myFam.add_kid(myKid)
print("Family made in code:")
print(myFam)
print("")

#Loading the data from a json file
example_json_file = "data/example_json.json"
with open(example_json_file, "r") as reader:
    family_data = json.load(reader)
print("JSON data:")
print(family_data)
print("")

myFamFromJson = example_json_utils.make_family_from_json(family_data)
print("Family loaded from JSON:")
print(myFamFromJson)
#End Part 2 Example


#Part 2
input_json_file = "data/test_data.json"

### Begin Add Code Here ###
#Open the file specified by input_json_file
#Use the json module to load the data from the file
#Use make_game_library_from_json(json_data) to convert the data to GameLibrary data
#Print out the resulting GameLibrary data using print()
### End Add Code Here ###


#Part 3
#Load your custom JSON file
#Convert JSON data to cc_data
#Save converted data to DAT file