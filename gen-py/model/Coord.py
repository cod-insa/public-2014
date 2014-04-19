from math import sqrt

class Coord:
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
    def __eq__(self, other):
        return self.x == other.get_x() and self.y == other.get_y()
        
    def get_x(self):
        return self.x
    
    def get_y(self):
        return self.y
    
    def set_x(self, x):
        self.x = x
        
    def set_y(self, y):
        self.y = y
    
    def norm(self):
        return sqrt(x**2 + y** 2)
    
    def opposite(self):
        return Coord(-self.x, -self.y)
    
    def dot(self, other):
        return self.x * other.get_x() + self.y() * other.get_y()
    
    def add(self, other, coef=1):
        self.x += other.get_x() * coef
        self.y += other.get_y() * coef
    
    def sub(self, other):
        self.x -= other.get_x()
        self.y -= other.get_y()
    
    def shift(self, shift):
        self.x += shift
        self.y += shift
        
    def mult(self, coef):
        self.x *= coef
        self.y *= coef
        
    def squareDistanceTo(self, other):
        return (self.x - other.get_x())**2 + (self.y - other.get_y())**2
    
    def distanceTo(self, other):
        return sqrt(self.squareDistanceTo(other))
    
    def __str__(self):
        return "Coord("+self.x+", "+self.y+")"
        