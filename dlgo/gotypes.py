import enum 
from collections import namedtuple

#namedtuple to access the coordinates as point.row and point.col 
#instead of point[0] and point[1]
class Point(namedtuple('Point', 'row col')):
    def neighbors(self):
        return [
            Point(self.row - 1, self.col),
            Point(self.row + 1, self.col),
            Point(self.row, self.col - 1),
            Point(self.row, self.col + 1),
        ]

#using enum to represent different color stones. Player instance
class Player(enum.Enum):
    black = 1
    white = 2
    
    #after you place a stone, switch colors by calling method on Player instance
    @property 
    def other(self):
        return Player.black if self == Player.white else Player.white

