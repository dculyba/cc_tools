"""
Data structures for working with simple JSON data
Created for the class Programming for Game Designers
"""

## Platforms ##
#This is the base Platform class.
#It defines a platform as having two pieces of information:
#  name
#  launch_year
class Platform:
    def __init__(self):
        self.name = "Unknown"
        self.launch_year = 0

#These classes extend the base Platform class and fill in specific details
class AtariLynx(Platform):
    def __init__(self):
        self.name = "Atari Lynx"
        self.launch_year = 1989


class Windows3_1(Platform):
    def __init__(self):
        self.name = "Windows 3.1"
        self.launch_year = 1992


class Steam(Platform):
    def __init__(self):
        self.name = "Steam"
        self.launch_year = 2003
## End Platforms ##

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
