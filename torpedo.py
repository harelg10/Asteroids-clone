import math

LIFE_TIME = 400
RADIUS = 4
SCREEN_MIN_X = -500
SCREEN_MIN_Y = -500
SCREEN_MAX_X = 500
SCREEN_MAX_Y = 500
a = []


class Torpedo:
    """
    This class represent the torpedos.
    it has the constructor based on the ship who shoot it,
    and "get" ,"set" functions
    for the needed attributes.
    """

    def __init__(self, ship,screen = None):
        """
        constructor. set the initial values of a torpedo
        :param ship: the ship who fired the torpedo
        """
        self.screen= screen
        self.x_loc = ship.get_loc_x()
        self.y_loc = ship.get_loc_y()
        self.heading_of_move = ship.get_heading()
        radian_heading = math.radians(self.heading_of_move)
        self.x_speed = ship.get_x_speed() + 2 * math.cos(
            radian_heading)
        self.y_speed = ship.get_y_speed() + 2 * math.sin(
            radian_heading)
        self.init_x = self.x_speed
        self.init_y = self.y_speed
        self.lifetime = LIFE_TIME
        self.radius = RADIUS
        self.locked = None

    def get_radius(self):
        """
        :return: radius of the torpedo
        """
        return self.radius

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

    def get_heading(self):
        """
        :return: heading of the torpedo
        """
        return self.heading_of_move


    def set_x_speed(self,speed):
        """
        :return: speed of x
        """
        self.x_speed = speed

    def set_y_speed(self,speed):
        """
        :return: speed of y
        """
        self.y_speed = speed

    def set_loc(self, new_x, new_y):
        """
        sets a new location for the torpedo
        """
        self.lifetime -= 1  # every movement we reduce the lifetime
        self.x_loc = new_x
        self.y_loc = new_y

    def get_lifetime(self):
        """
        :return: time left for the torpedo's life
        """
        return self.lifetime

    def set_heading(self, new_heading):
        self.heading_of_move = new_heading

    def direct(self,heading):
        # self.set_heading(heading)
        h = self.get_heading()
        radian_heading = math.radians(h)
        change = 0
        gap = h - heading
        print(gap)
        if h > heading:
            change = 0.5
            if h - heading > 8:
                change = 1.2
        elif h < heading:
            change = -0.5
            if heading - h > 8:
                change = -1.2
        self.set_heading(h + change)

        self.x_speed = self.init_x + 2 * math.cos(radian_heading)
        self.y_speed = self.init_y + 2 * math.sin(radian_heading)

        print(self.get_heading())



    def tracking(self, asteroids):
        # if self.locked not in asteroids:
        min = 500
        for ast in asteroids:
            d = dist(self.x_loc, self.y_loc, ast.get_loc_x(),
                     ast.get_loc_y())
            gap = math.atan2(
                math.radians(ast.get_loc_x() - self.x_loc),
                math.radians(ast.get_loc_y() - self.y_loc))
            if math.fabs(d) < min:
                min = d
                self.locked = ast


        if self.locked in asteroids:
            d = dist(self.x_loc + SCREEN_MAX_X, self.y_loc + SCREEN_MAX_Y, self.locked.get_loc_x() +SCREEN_MAX_X,
                     self.locked.get_loc_y()+ SCREEN_MAX_Y)
            dx = self.locked.get_loc_x() - self.x_loc  # +2*SCREEN_MAX_X
            dy = self.locked.get_loc_y() - self.y_loc  # +2*SCREEN_MAX_Y

            gap = math.degrees(
                math.atan2(dy, dx)) - self.heading_of_move
            if dx > 0 and dy > 0:
                gap += 180
            if d > 0.6:
                # gap = math.radians(math.acos(x / d)) * 3.2*math.sqrt(d)
                factor = maprange(gap)
                print(gap,factor)

                if -1.5 < factor < 1.5:
                    self.set_heading(
                        self.heading_of_move + sign(factor)) # + 0.07*math.sqrt(d))

                    radian_heading = math.radians(self.heading_of_move)
                    self.x_speed = self.init_x + 2 * math.cos(
                        radian_heading)
                    self.y_speed = self.init_y + 2 * math.sin(
                        radian_heading)


    def mousecoords(self):
        rawMouseX, rawMouseY = self.screen.get_root().winfo_pointerx(), self.screen.get_root().winfo_pointery()
        return rawMouseX - self.screen.get_root().winfo_rootx(), rawMouseY - self.screen.get_root().winfo_rooty()


def maprange(s):
    if s > 360:
        s = 360
    elif s < -360:
        s = -360
    (b1, b2) = (-1.2,1.2)
    (a1, a2) = (-180, 180)
    return b1 + ((s - a1) / (a2 - a1) * (b2 - b1))



def dist(x1, y1, x2, y2):
    x = x2 - x1
    x = math.pow(x, 2)
    y = y2 - y1
    y = math.pow(y, 2)
    return math.sqrt(x + y)



def avg():
    return sum(a)/len(a)


def sign(x):
    if x > 0:
        return x+0.3
    elif x == 0:
        return x
    return x-0.3