import test_data
import sys
import json

#Creates and returns a GameLibrary object(defined in test_data) from loaded json_data
def make_game_library_from_json(json_data):
    #Initialize a new GameLibrary
    game_library = test_data.GameLibrary()

    #Loop through the json_data
        #Create a new Game object from the json_data
        #Add that Game object to the game_library

    #Return the completed game_library
    return game_library

