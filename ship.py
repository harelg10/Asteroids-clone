# Username : dor_neriya
# ID : 205439920
# Name :  Dor Neriya

START_SPEED = 0
START_HEADING = 0
START_LIVES = 3


class Ship:
    """
    This class is our ship, it has a constructor and "get" ,"set" functions
    for all the attributes.
    """

    def __init__(self, x_loc, y_loc):
        """
        constructor. sets the ship
        """
        self.x_loc = x_loc
        self.y_loc = y_loc
        self.x_speed = START_SPEED
        self.y_speed = START_SPEED
        self.heading = START_HEADING
        self.radius = 1
        self.lives = START_LIVES

    def reduce_live(self):
        """
        remove 1 life
        """
        self.lives -= 1

    def get_lives(self):
        """
        returns lives of the ship
        """
        return self.lives

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

    def set_loc(self, new_x, new_y):
        """
        sets a new location to the ship
        """
        self.x_loc = new_x
        self.y_loc = new_y

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

    def set_x_speed(self, new_x_speed):
        """
        sets speed of x
        """
        self.x_speed = new_x_speed
        return

    def set_y_speed(self, new_y_speed):
        """
        sets speed of y
        """
        self.y_speed = new_y_speed
        return

    def get_heading(self):
        """
        :return: heading of the ship
        """
        return self.heading

    def set_heading(self, new_heading):
        """
        sets a new heading for the ship
        """
        self.heading = new_heading
        return


