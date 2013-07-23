from __future__ import division, print_function, absolute_import
import pdb
from time import sleep

from random import randint, random, shuffle
import turtle
from time import time

from world import TurtleWorld, PowerTurtle, wrap
import math

class Asteroid(PowerTurtle):
    type = 'asteroid'
    ship = None

    def setup(self):
        self.penup()
        self.color('brown')
        self.shape("rectangle")
        self.size = 0.5 + random() * 4.0
        self.radius = 10 * self.size
        self.shapesize(self.size, self.size)
        hw = self.world.half_width
        hh = self.world.half_height
        x = randint(hw - 100, hw)
        if random() < 0.5:
            x = -x
        y = randint(hh - 100, hh)
        if random() < 0.5:
            y = -y
        self.setpos(x, y)
        self.setheading(self.towards(0, 0) + (random() * 90) - 45)
        self.speed = (random() * 2.0) + 0.1

    def callback(self, world):
        ship = world.ship
        if self.distance(ship) < self.radius:
            ship.die()
        if ship.rocket and self.distance(ship.rocket) < self.radius:
            self.clear()
            world.remove_turtle(self)
            world.remove_turtle(ship.rocket)
            ship.rocket = None
        else:
            self.penup()
            self.forward(self.speed)


class Ship(PowerTurtle):
    type = 'ship'

    def setup(self):
        self.shape('turtle')
        self.fillcolor('green')
        self.setheading(90)
        self.dead = False
        self.rocket = None
        self.__range = 200
        self.state = "shooting"

    def callback(self, world):
        self.penup()
        if not self.dead:
            asteroids = [t for t in world.turtles if t.type == 'asteroid']
            if not asteroids:
                self.write("I WIN, PUNY HUMAN")
                sleep(5)
                bye()
            if self.state != 'shooting':
                self.runaway()
            else:
                distances = [(self.distance(a) - a.radius, a) for a in asteroids]
                distances.sort()
                dangerous =[(d, a) for d, a in distances if d < 70]
                if dangerous:
                    self.run(dangerous)
                else:
                    self.shoot(distances[0][0], distances[0][1], world)

    def shoot(self, distance, a, world):
        diff = self.turn_towards(self.towards(a), 6)
        if distance < self.__range:
            if diff < 1:
                self.fire()
        else:
            self.forward(1)

    def fire(self):
        if self.rocket is None:
            self.rocket = Rocket(w)
            self.rocket.init(self.heading(), self.pos(), self.__range)
            self.world.add_turtle(self.rocket)

    def die(self):
        if not self.dead:
            self.write("GAME OVER")
            self.dead = True

    def run(self, dangerous):
        d, a = dangerous[0]
        lr = -90 if random() > 0.5 else 90
        self._running_heading = self.towards(a) + lr
        self._running_distance = 50
        self.state = "turning"
        self.runaway()

    def runaway(self):
        if self.state == "turning":
            diff = self.turn_towards(self._running_heading, 6)
            if diff < 1.0 or diff > 359.0:
                self.state = "running"
        elif self.state == "running":
            self.forward(2.0)
            self._running_distance -= 2.0
            if self._running_distance <= 1.0:
                self.state = 'shooting'



# turtle.addSensor("left eye", (-10, 10))
# turtle.addSensor("right eye", (10, 10))
#
# def brain
#     if

class Rectangle(PowerTurtle):
    def __init__(self, world, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        super(Rectangle, self).__init__(world)

    def setup(self):
        screen = self.getscreen()
        # x2 = self.w / 2
        # y1 = -self.h / 2
        # y2 = self.h / 2
        # x1 = -self.w / 2

        x1 = 0
        x2 = 1
        y1 = 0
        y2 = 1

        name = "rectangle%d.%d.%d.%d" % (x1, y1, x2, y2)
        screen.register_shape(name, ((x2, y1), (x2, y2), (x1, y2), (x1, y1)))
        self.shape("square")
        self.shapesize(self.w/10.0, self.h/10.0)
        color = (random(), random(), random())
        self.color("black", color)
        self.setpos(self.x, self.y)
        self.ht()

    def contains(self, x, y):
        print(x, y, self.x, self.y, self.x + self.w, self.y + self.h)
        within = (x >= self.x) and (x < (self.x + self.w)) and (y >= self.y) and (y < (self.y + self.h))
        if within: print("in", x, y, self.x, self.y)
        return within


    def callback(self, world):
        pass

class Eye(object):
    def __init__(self, turtle, angle, distance):
        self.turtle = turtle
        self.angle = angle
        self.distance = distance

    def positioninworld(self):
        (x, y) = self.turtle.position()
        newangle = self.turtle.heading() + self.angle

        dx = -math.sin(math.radians(newangle)) * self.distance
        dy = math.cos(math.radians(newangle)) * self.distance

        newpos = (x + dx, y + dy)
        return newpos


class CleverTurtle(PowerTurtle):
    def __init__(self, world, x, y):
        super(CleverTurtle, self).__init__(world)
        self.lefteye = Eye(self, 45, 20)
        self.righteye = Eye(self, -45, 20)
        self.setpos(x, y)

    def setup(self):
        self.shape('turtle')
        self.fillcolor('blue')

    # tick
    def callback(self, world):
        if world.something_at(self.lefteye.positioninworld()):
            self.right(5)
        elif world.something_at(self.righteye.positioninworld()):
            self.left(5)

        self.forward(1)

        # world.somethingAt(self.leftEye)
        pass


dimensions = 600
w = TurtleWorld(dimensions, dimensions, wrap)
w.screen.mode("logo")

for i in range(10):
    w.add_turtle(CleverTurtle(w, randint(0, dimensions) /2, randint(0, dimensions)/2))



#ship = Ship(w)
#w.ship = ship
#w.add_turtle(ship)
for i in range(20):
    w.add_obstacle(Rectangle(w, randint(0, dimensions) - dimensions/2, randint(0, dimensions) - dimensions/2, randint(10, 100), randint(10, 100)))

w.add_obstacle(Rectangle(w, -20, 100, 50, 40))



w.run(-1)

#
# turtle.brain
#
# if (wall.isAhead)
#     self.turnRight