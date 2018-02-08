import sys
import json
import example_data

#Creates and returns a Family object(defined in example_data) from loaded json_data
def make_family_from_json(json_data):
    #Initialize a new family
    new_family = example_data.Family()
    #Set the parents
    #Loop through the kids_data and make a new Kid for each entry in the kids_data
    #Note: this is how to loop through data in python
    #One thing to note is "kid_data" is a variable that is declared as part of the loop
    #  The loop steps through each element in the list (here the list is kids_data)
    #  and the variable kid_data represents the current element in the list
        #Get the data from from the current kid in the kids_data list
        #Make a new Kid with the data
        #Add the Kid to the new_family
    #We're done making and adding all the kids, so return the finished Family
    return new_family
