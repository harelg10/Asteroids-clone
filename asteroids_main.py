from screen import Screen
from ship import Ship
from asteroid import Asteroid
from torpedo import Torpedo
import sys
import math
import random

DEFAULT_ASTEROIDS_NUM = 5
ASTEROID_SIZE = 2
NUM_OF_TORPEDOS = 10
MISSILE_PRICE = 20
FREEZE_PRICE = 30

class GameRunner:
    """
    The game itself, control the screen and the objects.
    in the constructor Initializing the game,
    and uses functions to maintain the screen and game according to the
    user's instructions.
    """

    def __init__(self, asteroids_amount=DEFAULT_ASTEROIDS_NUM):
        """
        game constructor. Initializing the game
        :param asteroids_amount: the initial number of asteroids in the game
        """
        self.__screen = Screen()
        self.score = 0
        self.__screen_max_x = Screen.SCREEN_MAX_X
        self.__screen_max_y = Screen.SCREEN_MAX_Y
        self.__screen_min_x = Screen.SCREEN_MIN_X
        self.__screen_min_y = Screen.SCREEN_MIN_Y
        self.__ship = Ship(random.randint(self.__screen_min_x,
                                          self.__screen_max_x),
                           random.randint(self.__screen_min_y,
                                          self.__screen_max_y))
        self.draw_update_ship()
        self.asteroids_amount = asteroids_amount
        self.freeze = False
        self.__asteroid_list = []
        self.__torpedo_list = []
        self.missile_list = []
        self.number_of_torpedoes = NUM_OF_TORPEDOS
        self.create_asteroids(self.asteroids_amount, ASTEROID_SIZE)

    def run(self):
        """
        runs the game
        """
        self._do_loop()
        self.__screen.start_screen()

    def _game_loop(self):
        """
        a loop to do for every frame of the game
        """
        self.move_ship()  # moves the ship
        if self.__screen.is_f_pressed():

            if self.freeze is False:
                self.score -= FREEZE_PRICE
                self.__screen.set_score(self.score)
            if self.score >= FREEZE_PRICE:
                self.freeze = True

        else:
            self.freeze = False
        if not self.freeze:
            self.move_asteroids()  # moves the asteroids
        if self.__screen.is_space_pressed():
            self.add_torpedo()  # make a torpedo
        if self.__screen.is_v_pressed():
            self.add_missile()

        self.move_torpedos()  # moves the torpedos
        self.check_intersections()   # check if there was intersection
        # between asteroid and the ship
        self.handle_torpedo_hit_asteroid()
        self.want_exit()  # check if the user press "q"

    def move_torpedos(self):
        """
        handle the actions of the torpedoes  (lifetime, movement, hits)
        """
        left_turn = self.__screen.is_torpedo_left_pressed()
        right_turn = self.__screen.is_torpedo_right_pressed()

        for torpedo in self.missile_list:
            if torpedo.get_lifetime() == 0:
                self.__screen.unregister_torpedo(torpedo)
                self.missile_list.remove(torpedo)
                continue  # go to the next torpedo
            # update the torpedo's location
            # torpedo.tracking(self.__asteroid_list)

            speed = math.sqrt(
                torpedo.get_x_speed() ** 2 + torpedo.get_y_speed() ** 2)
            if speed < 5.3:
                speed += 0.03
            if left_turn:
                torpedo.set_heading(
                    torpedo.get_heading() + 6)
                torpedo.set_x_speed(
                    speed * math.cos(
                        math.radians(torpedo.get_heading())))
                torpedo.set_y_speed(
                    speed * math.sin(
                        math.radians(torpedo.get_heading())))
            if right_turn:
                torpedo.set_heading(
                    torpedo.get_heading() - 6)
                torpedo.set_x_speed(
                    speed * math.cos(
                        math.radians(torpedo.get_heading())))
                torpedo.set_y_speed(
                    speed * math.sin(
                        math.radians(torpedo.get_heading())))

            # update the location of the ship
            # new_x = get_new_spot(self.__ship.get_loc_x(),
            #                      self.__ship.get_x_speed(),
            #                      Screen.SCREEN_MAX_X,
            #                      Screen.SCREEN_MIN_X)
            # new_y = get_new_spot(self.__ship.get_loc_y(),
            #                      self.__ship.get_y_speed(),
            #                      Screen.SCREEN_MAX_Y,
            #                      Screen.SCREEN_MIN_Y)

            x = get_new_spot(torpedo.get_loc_x(),
                             torpedo.get_x_speed(),
                             self.__screen_max_x,
                             self.__screen_min_x)
            y = get_new_spot(torpedo.get_loc_y(),
                             torpedo.get_y_speed(),
                             self.__screen_max_y,
                             self.__screen_min_y)
            torpedo.set_loc(x, y)
            self.__screen.draw_torpedo(torpedo, torpedo.get_loc_x(),
                                       torpedo.get_loc_y(),
                                       torpedo.get_heading())

        for torpedo in self.__torpedo_list:
            if torpedo.get_lifetime() == 0:
                self.remove_torpedo(torpedo)
                continue  # go to the next torpedo
            # update the torpedo's location
            # torpedo.tracking(self.__asteroid_list)

            # speed = math.sqrt(torpedo.get_x_speed()**2 + torpedo.get_y_speed()**2)
            # if speed < 5.3:
            #     speed += 0.03
            # if left_turn:
            #     torpedo.set_heading(
            #         torpedo.get_heading() + 6)
            #     torpedo.set_x_speed(
            #         speed * math.cos(math.radians(torpedo.get_heading())))
            #     torpedo.set_y_speed(
            #         speed * math.sin(math.radians(torpedo.get_heading())))
            # if right_turn:
            #     torpedo.set_heading(
            #         torpedo.get_heading() - 6)
            #     torpedo.set_x_speed(
            #         speed * math.cos(math.radians(torpedo.get_heading())))
            #     torpedo.set_y_speed(
            #         speed * math.sin(math.radians(torpedo.get_heading())))


            # update the location of the ship
        # new_x = get_new_spot(self.__ship.get_loc_x(),
        #                      self.__ship.get_x_speed(),
        #                      Screen.SCREEN_MAX_X,
        #                      Screen.SCREEN_MIN_X)
        # new_y = get_new_spot(self.__ship.get_loc_y(),
        #                      self.__ship.get_y_speed(),
        #                      Screen.SCREEN_MAX_Y,
        #                      Screen.SCREEN_MIN_Y)


            x = get_new_spot(torpedo.get_loc_x(), torpedo.get_x_speed(),
                             self.__screen_max_x, self.__screen_min_x)
            y = get_new_spot(torpedo.get_loc_y(), torpedo.get_y_speed(),
                             self.__screen_max_y, self.__screen_min_y)
            torpedo.set_loc(x, y)
            self.__screen.draw_torpedo(torpedo, torpedo.get_loc_x(),
                                       torpedo.get_loc_y(),
                                       torpedo.get_heading())

    def handle_torpedo_hit_asteroid(self):
        """
        checks if any of the torpedoes has hit any of the asteroids and acts accordingly
        """

        for torpedo in self.__torpedo_list:
            for asteroid in self.__asteroid_list:
                # check if the torpedo is hitting an asteroid
                if asteroid.has_intersection(torpedo):
                    # delete the torpedo and blow the asteroid
                    self.remove_torpedo(torpedo)
                    self.divide_asteroid(asteroid, torpedo)
                    self.no_more_astro()  # check if there isn't
                    # asteroids anymore
                    break  # go to the next torpedo

        for torpedo in self.missile_list:
            for asteroid in self.__asteroid_list:
                # check if the torpedo is hitting an asteroid
                if asteroid.has_intersection(torpedo):
                    # delete the torpedo and blow the asteroid
                    self.__screen.unregister_torpedo(torpedo)
                    self.missile_list.remove(torpedo)
                    self.divide_asteroid(asteroid, torpedo)
                    self.no_more_astro()  # check if there isn't
                    # asteroids anymore
                    break  # go to the next torpedo


    def remove_torpedo(self, torpedo):
        """
        remove a torpedo from the screen and from the list
        """
        self.__screen.unregister_torpedo(torpedo)
        self.__torpedo_list.remove(torpedo)

    def check_intersections(self):
        """
        handle an intersection between a ship and an asteroid
        """
        for asteroid in self.__asteroid_list:
            if asteroid.has_intersection(self.__ship):
                self.__ship.reduce_live()
                self.__screen.remove_life()
                if self.__ship.get_lives() < 1:
                    self.__screen.show_message("You LOST",
                                               "you have no lives,"
                                               "\nyour score was " +
                                               str(self.score))
                    self.__screen.end_game()
                    sys.exit()
                self.__screen.show_message("BOOM", "You crashed into an"
                                    " asteroid and lost life\n\nWATCH OUT!")
                self.__screen.unregister_asteroid(asteroid)
                self.__asteroid_list.remove(asteroid)
                self.no_more_astro()  # check if there isn't asteroids
                # anymore

    def update_score(self, size):
        """
        update the score after blowing an asteroid
        :param size: the size of the asteroid that was blown
        """
        if size == 3:
            self.score += 20
        elif size == 2:
            self.score += 50
        elif size == 1:
            self.score += 100
        self.__screen.set_score(self.score)

    def draw_update_ship(self):
        """
        update the ship in the screen according to its location and heading
        """
        self.__screen.draw_ship(self.__ship.get_loc_x(),
                                self.__ship.get_loc_y(),
                                self.__ship.get_heading())

    def _do_loop(self):
        # You should not to change this method!
        self._game_loop()
        # Set the timer to go off again
        self.__screen.update()
        self.__screen.ontimer(self._do_loop, 5)

    def move_asteroids(self):
        """
        move the asteroids in the game according to their speed
        """
        for asteroid in self.__asteroid_list:
            x = get_new_spot(asteroid.get_loc_x(), asteroid.get_x_speed(),
                             self.__screen_max_x, self.__screen_min_x)
            y = get_new_spot(asteroid.get_loc_y(), asteroid.get_y_speed(),
                             self.__screen_max_y, self.__screen_min_y)
            asteroid.set_loc(x, y)
            self.draw_update_asteroid(asteroid)

    def move_ship(self):
        """
        turn and move the ship according to its speed and the input from the
        player
        """

        # check if the ship needs to turn
        if self.__screen.is_left_pressed():
            self.__ship.set_heading(self.__ship.get_heading() + 7)
        if self.__screen.is_right_pressed():
            self.__ship.set_heading(self.__ship.get_heading() - 7)
        # check if the ship needs to accelerate
        if self.__screen.is_up_pressed():
            self.__ship.set_x_speed(self.__ship.get_x_speed()
                + math.cos(math.radians(self.__ship.get_heading())))
            self.__ship.set_y_speed(self.__ship.get_y_speed()
                + math.sin(math.radians(self.__ship.get_heading())))
        # update the location of the ship
        new_x = get_new_spot(self.__ship.get_loc_x(),
                             self.__ship.get_x_speed(),
                             Screen.SCREEN_MAX_X, Screen.SCREEN_MIN_X)
        new_y = get_new_spot(self.__ship.get_loc_y(),
                             self.__ship.get_y_speed(),
                             Screen.SCREEN_MAX_Y,
                             Screen.SCREEN_MIN_Y)
        self.__ship.set_loc(new_x, new_y)
        self.draw_update_ship()
        # print(self.__ship.get_loc_x()+self.__screen_max_x,self.__ship.get_loc_y()-self.__screen_min_y)

    def create_asteroids(self, asteroids_amount, size):
        """
        adds a number of asteroid to the game
        :param asteroids_amount: the number of items to add
        :param size: the size of the asteroids to add
        """
        for i in range(asteroids_amount):
            while True:   # Make sure the ship's location is not inserted
                x_loc = random.randint(self.__screen_min_x,
                                       self.__screen_max_x)
                y_loc = random.randint(self.__screen_min_y,
                                       self.__screen_max_y)
                if x_loc != self.__ship.get_loc_x() and y_loc != \
                        self.__ship.get_loc_y():
                    break
            new_asteroid = Asteroid(x_loc, y_loc, size)
            self.add_asteroid(new_asteroid, size)

    def add_asteroid(self, new_asteroid, size):
        """
        register, add to the list, and update to the screen a new asteroid
        :param new_asteroid: the asteroid
        :param size: it's size
        """
        self.__screen.register_asteroid(new_asteroid, size)
        self.__asteroid_list.append(new_asteroid)
        self.draw_update_asteroid(new_asteroid)

    def divide_asteroid(self, asteroid, torpedo):
        """
        blows up an asteroid. if the asteroid was big, creates
         2 smaller asteroids
        :param asteroid: the asteroid that was hit
        :param torpedo: the torpedo that hit
        """
        size = asteroid.get_size() - 1  # get the size of the next asteroids
        self.update_score(size + 1)  # add the points for the original asteroid
        if size > 0:  # if the asteroid wasn't the smallest
            # -# divide it to 2 smaller ones
            # get the new asteroids speed in absolute value
            new_speed_x = get_new_speed(torpedo.get_x_speed(),
                                asteroid.get_x_speed(), asteroid.get_y_speed())
            new_speed_y = get_new_speed(torpedo.get_y_speed(),
                                asteroid.get_y_speed(), asteroid.get_x_speed())
            self.split_asteroid(asteroid, new_speed_x, new_speed_y, size)
            # add an asteroid with + speed
            self.split_asteroid(asteroid, new_speed_x, new_speed_y, size, True)
            # add an asteroid with - speed
        # delete the asteroid from the screen and from the list
        self.__screen.unregister_asteroid(asteroid)
        self.__asteroid_list.remove(asteroid)

    def split_asteroid(self, asteroid, speed_x, speed_y, size, is_reverse=False):
        """
        :param asteroid: the original asteroid to be split
        :param speed_x: absolute value of the new speed in x direction
        :param speed_y: absolute value of the new speed in y direction
        :param size: size of the new asteroid
        :param is_reverse: is the speed of the new asteroid going to
         the opposite direction
        """
        if is_reverse:
            # if it's the opposite asteroid to add, flip the speeds
            speed_y = speed_y * -1
            speed_x = speed_x * -1
        # create a smaller asteroid and set its speed
        new_asteroid = Asteroid(asteroid.get_loc_x(), asteroid.get_loc_y(), size)
        new_asteroid.set_x_speed(speed_x)
        new_asteroid.set_y_speed(speed_y)
        self.add_asteroid(new_asteroid, size)

    def draw_update_asteroid(self, asteroid):
        """
        draw an asteroid on the screen
        """
        self.__screen.draw_asteroid(asteroid,
                                asteroid.get_loc_x(), asteroid.get_loc_y())

    def add_torpedo(self):
        """
        fires a torpedo from te ship if possible
        """
        # check if a new torpedo can be added
        if len(self.__torpedo_list) < self.number_of_torpedoes:
            new_torpedo = Torpedo(self.__ship,self.__screen)
            self.__screen.register_torpedo(new_torpedo)
            self.__torpedo_list.append(new_torpedo)

    def add_missile(self):
        """
        fires a torpedo from te ship if possible
        """
        if self.score >= MISSILE_PRICE:
            self.score -= MISSILE_PRICE
            self.__screen.set_score(self.score)
            new_torpedo = Torpedo(self.__ship, self.__screen)
            self.__screen.register_torpedo(new_torpedo)
            self.missile_list.append(new_torpedo)
            

    def no_more_astro(self):
        """
        checks if the game is over because there is no more asteroids to blow
        if the game is over - exit the program
        """
        if len(self.__asteroid_list) == 0:
            self.__screen.show_message("YOU WON", "NO MORE ASTEROID your "
                                                "score was " + str(self.score))
            self.__screen.end_game()
            sys.exit()

    def want_exit(self):
        """
        checks if the game is over because there is no more lives
        or 'Q' was pressed
        if the game is over - exit the program
        :return:
        """
        if self.__screen.should_end():
            self.__screen.show_message("good bye", "see you")
            self.__screen.end_game()
            sys.exit()


def get_new_spot(old_spot, speed, sc_max, sc_min):
    """
    return a new location of an object with a formula
    needs the max and min of the screen,
    and previous location and speed of the object
    """
    return sc_min + (old_spot + speed - sc_min) % (sc_max - sc_min)


def get_new_speed(torp_speed, old_ast_speed_x, old_ast_speed_y):
    """
    return an absolute value of a speed of 2 new asteroids
    that formed from an asteroid that was hit by a torpedo
    needs the speed of the torpedo, and the speed of the big asteroid(x+y
    """
    return (torp_speed+old_ast_speed_x) / math.sqrt((old_ast_speed_x**2)+(
            old_ast_speed_y**2))


def main(amount):
    """
    runs a game of asteroids
    :param amount: number of initial asteroids in the game
    """
    runner = GameRunner(amount)
    runner.run()


if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(int(sys.argv[1]))
    else:
        main(DEFAULT_ASTEROIDS_NUM)
