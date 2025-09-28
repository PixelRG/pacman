import math
"""
page1:
- The scalar always has to be on the right side.  So something like 'Vector * 5' and not '5 * Vector'."""

class Vector():
    def __init__(self,x = 0, y = 0):
        self.x = x
        self.y = y
        self.thresh = 0.0001 # this is only used by the equality method. 
        """ the purpose of thresh is to verify if two vectors are close to being equal to each other"""

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)

    def __neg__(self):
        return Vector(-self.x, -self.y)

    def __mul__(self, scalar):
        return Vector(self.x * scalar, self.y * scalar)

    def __truediv__(self, scalar):
        if scalar != 0:
            return Vector(self.x / float(scalar), self.y / float(scalar))
        return None

    def __eq__(self,other): # check if two vectors are equal within a certain range
        if abs(self.x - other.x) < self.thresh:
            if abs(self.y - other.y) <self.thresh:
                return True
        return False
    
    
    def magnitudeSquared(self): # We're going to use this more often
        return self.x**2 + self.y**2
    def magnitude(self):
        return math.sqrt(self.x**2 + self.y**2)
    def asTuple(self):
        return self.x, self.y

    def asInt(self):
        return int(self.x), int(self.y)

    def copy(self):
            return Vector(self.x, self.y)