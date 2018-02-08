import sys
import json
import example_data

#Creates and returns a Family object(defined in example_data) from loaded json_data
def make_family_from_json(json_data):
    #Initialize a new family
    new_family = example_data.Family()
    #Set the parents
    #Spelling important here!
    #We used Parent1 and Parent2 as the keys in the json file
    #To get that data from the json data we need to use those exact keys
    new_family.parent1 = json_data["Parent1"]
    new_family.parent2 = json_data["Parent2"]
    #Loop through the kids_data and make a new Kid for each entry in the kids_data
    #Note: this is how to loop through data in python
    #One thing to note is "kid_data" is a variable that is declared as part of the loop
    for kid_data in json_data["Kids"]:
        #  The loop steps through each element in the list (here the list is kids_data)
        #  and the variable kid_data represents the current element in the list
        #Make a new Kid
        kid = example_data.Kid()
        # Get the data from from the current kid in the kids_data list
        kid.name = kid_data["Name"]
        kid.age = kid_data["Age"]
        #Add the Kid to the new_family
        new_family.add_kid(kid)
    #We're done making and adding all the kids, so return the finished Family
    return new_family
