import math


class Point:
    def __init__(self, id, x, y):
        self.id = id
        self.x = x
        self.y = y

    def distanceTo(self, p):
        return math.sqrt(math.pow((self.x - p.x), 2) + math.pow((self.y - p.y), 2))

    def __eq__(self, other):
        return self.x==other.x and self.y==other.y
    def __str__(self):
        return f"( {self.x} , {self.y} )"
    def get_id(self):
        return f"{self.id}"