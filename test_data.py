"""
Data structures for working with simple JSON data
Created for the class Programming for Game Designers
"""

## Platforms ##
#This is the Platform class.
#Note that the initializer takes 2 arguments:
#  name
#  launch_year
class Platform:
    def __init__(self, name="Unknown", launch_year=0):
        self.name = name
        self.launch_year = launch_year

#This is the Game class.
#Note that the initializer takes 3 arguments:
#  title
#  platform
#  year
class Game:
    def __init__(self, title="Unknown", platform=None, year=0):
        self.title = title
        self.platform = platform
        self.year = year

#This is the GameLibrary class.
#It is defined by a single piece of data: a list of games
class GameLibrary:
    def __init__(self):
        self.games = []

    def add_game(self, game):
        self.games.append(game)


def print_game_library(game_library_data):
    print("Analyising game library data:")
    game_count = 0
    for game in game_library_data.games:
        print("  Game "+str(game_count))
        print("    Title = "+game.title)
        print("    Year  = "+str(game.year))
        print("    Platform = ")
        print("       Name = "+game.platform.name)
        print("       Launch Year = "+str(game.platform.launch_year))
        game_count += 1

