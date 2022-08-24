import random
import math


class Asteroid:
    """
    This class represent the Asteroid.
    it has the constructor,
    and "get" ,"set" functions
    for the needed attributes.

    in addition the function has_intersection that check if some object
    (ship or torpedo) crashed into an asteroid.
    """
    def __init__(self, x_loc, y_loc, size):
        """
        constructor.set the initial values for the asteroid
        """
        self.x_loc = x_loc
        self.y_loc = y_loc
        self.x_speed = random.choice([-4, -3, -2, -1, 1, 2, 3, 4])
        self.y_speed = random.choice([-4, -3, -2, -1, 1, 2, 3, 4])
        self.size = size
        self.radius = size * 10 - 5

    def get_radius(self):
        """
        :return: radius
        """
        return self.radius

    def get_loc_x(self):
        """
        :return: location of x
        """
        return self.x_loc

    def get_loc_y(self):
        """
        :return: location of y
        """
        return self.y_loc

    def get_x_speed(self):
        """
        :return: speed of x
        """
        return self.x_speed

    def get_y_speed(self):
        """
        :return: speed of y
        """
        return self.y_speed

    def set_loc(self, new_x, new_y):
        """
        sets a new location for the asteroid
        """
        self.x_loc = new_x
        self.y_loc = new_y

    def set_x_speed(self, new_x_speed):
        """
        sets a new speed on x for the asteroid
        """
        self.x_speed = new_x_speed
        return

    def set_y_speed(self, new_y_speed):
        """
        sets a new speed on y for the asteroid
        """
        self.y_speed = new_y_speed
        return

    def has_intersection(self, obj):
        """
        check if this asteroid collides into some other object
        :returns:True if collision happened.False if not
        """
        dis = math.sqrt((obj.get_loc_x()-self.get_loc_x())**2 +
                        (obj.get_loc_y()-self.get_loc_y())**2)
        if dis <= (self.get_radius()+ obj.get_radius()):
            return True
        return False

    def get_size(self):
        """
        :return: size
        """
        return self.size

    def set_size(self, new_size):
        """
        sets a new size for the asteroid
        """
        self.size = new_size
