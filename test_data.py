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

    def __str__(self):
        return_str = "Analyzing game library data:\n"
        game_count = 0
        for game in self.games:
            return_str += "  Game " + str(game_count) + "\n"
            return_str += "    Title = " + game.title + "\n"
            return_str += "    Year  = " + str(game.year) + "\n"
            return_str += "    Platform = " + "\n"
            return_str += "       Name = " + game.platform.name + "\n"
            return_str += "       Launch Year = " + str(game.platform.launch_year) + "\n"
            game_count += 1
        return return_str

