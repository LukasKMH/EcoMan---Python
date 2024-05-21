import math

class Vector2(object):
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
        self.limiar = 0.000001

    def __add__(self, outro):
        return Vector2(self.x + outro.x, self.y + outro.y)

    def __sub__(self, outro):
        return Vector2(self.x - outro.x, self.y - outro.y)

    def __neg__(self):
        return Vector2(-self.x, -self.y)

    def __mul__(self, escalar):
        return Vector2(self.x * escalar, self.y * escalar)

    def __div__(self, escalar):
        if escalar != 0:
            return Vector2(self.x / float(escalar), self.y / float(escalar))
        return None

    def __truediv__(self, escalar):
        return self.__div__(escalar)

    def __eq__(self, outro):
        if abs(self.x - outro.x) < self.limiar:
            if abs(self.y - outro.y) < self.limiar:
                return True
        return False

    def magnitude_quadrada(self):
        return self.x**2 + self.y**2

    def magnitude(self):
        return math.sqrt(self.magnitude_quadrada())

    def copy(self):
        return Vector2(self.x, self.y)

    def forma_tupla(self):
        return self.x, self.y

    def forma_inteiro(self):
        return int(self.x), int(self.y)

    def __str__(self):
        return "<"+str(self.x)+", "+str(self.y)+">"

