# planet_models.py
# Zachary Mayle
# 5/29/16

"""This module contains all of the models for the Planets game-- ship, planets,
wormholes."""

from planet_constants import *
from game2d import *


class Ship(GImage):
    """The spaceship that the player controls. The player gives it thrust by
    pressing the arrow keys to help it reach the finish point.
    
    This class contains methods to move the ship, accelerate the ship in the
    x direction, accelerate the ship in the y direction, switch the ship's
    frame to thrust, and switch the ship's frame to no thrust.
    
    ATTRIBUTES:
    
        _mass   [int or float>=0] the ship's mass
        _xv     [int or float>=0] the ship's x velocity
        _yv     [int or float>=0] the ship's y velocity
        _teleporting    [Boolean] True if ship is currently teleporting, False
            otherwise
    """
    
    def __init__(self, xpos, ypos):
        """Initializer: Creates a new ship at the starting point of the level.
        """
        GImage.__init__(self, width=SHIP_WIDTH, height=SHIP_HEIGHT, x=xpos, y=ypos, source=SHIP_IMAGE)
        self._mass = SHIP_MASS
        self._xv = 0.0
        self._yv = 0.0
        self._teleporting = False
    
    
    def get_mass(self):
        return self._mass
    
    
    def get_xv(self):
        return self._xv
    
    
    def get_yv(self):
        return self._yv
    
    
    def get_teleport(self):
        return self._teleporting
    
    
    def set_xv(self, v):
        """Sets the ship's x velocity to v.
        """
        self._xv = v
    
    
    def set_yv(self, v):
        """Sets the ship's y velocity to v.
        """
        self._yv = v
    
    
    def set_teleport(self, fact):
        """Sets the ship's teleporting attribute to fact.
            fact must be a boolean"""
        self._teleporting = fact
    
    
    def move_ship(self):
        """Adds the ship's current x velocity to its x position and its y velocity
        to its y position.
        """
        self.x += self._xv
        self.y += self._yv
    
    
    def accel_ship(self, x_accel, y_accel):
        """Adds x_accel to the ship's x velocity and adds y_accel to the ship's y
        velocity.
        """
        self._xv += x_accel
        self._yv += y_accel
    
    
    
class Planet(GImage):
    """A planet that helps populate the level and pulls the ship toward it.
    
    This class contains methods to determine the distance between the planet and
    a different object (the ship, usually) and to detect for collisions with
    other objects.
    
    ATTRIBUTES:
        _mass [int or float>=0] the planet's mass
        _radius [float>=0] the planet's radius; always equal to half the width
            (same as half the height)
    """
    
    def __init__(self, xpos, ypos, m, r, src):
        """Initializer: Creates a planet with radius r, mass m, position (xpos,ypos),
        and source image src.
        """
        GImage.__init__(self, width=2*r, height=2*r, x=xpos, y=ypos, source=src)
        self._mass = m
        self._radius = r
    
    
    def get_mass(self):
        return self._mass
    
    
    def p_distance(self, obj):
        """Returns the distance between the planet and the GImage object obj.
        """
        x1 = self.x
        y1 = self.y
        x2 = obj.x
        y2 = obj.y
        dx = abs(x2 - x1)
        dy = abs(y2 - y1)
        d = ((dx**2.0) + (dy**2.0))**0.5
        return d
    
    
    def collision_check(self, obj):
        """Returns True if the GImage object obj is within the planet's radius.
        """
        dist = self.p_distance(obj)
        if dist < self._radius:
            return True
        else:
            return False
    
    
    def get_trig(self, obj):
        """Returns a list containing cos(A) and sin(A), where A is the angle between
        the x-axis and the line connecting the planet to the GImage object obj. The
        planet is taken to be the origin.
        """
        x1 = self.x
        y1 = self.y
        x2 = obj.x
        y2 = obj.y
        dx = x2 - x1
        dy = y2 - y1
        dz = (dx**2.0 + dy**2.0)**0.5
        cos = dx / dz
        sin = dy / dz
        return [cos, sin]
    
    
class Wormhole(GImage):
    """A wormhole that teleports the ship to its sister wormhole when the ship
    enters the first wormhole. Always come in pairs. When ship teleports, it
    retains its velocity.
    
    This class contains methods for calculating the distance between the
    wormhole and another object, for pairing wormholes,
    and for detecting an entering ship.
    
    ATTRIBUTES:
        _sister [Wormhole object] represents this wormhole's sister
        _radius [int or float > 0] the wormhole's radius
    """
    
    def __init__(self, xpos, ypos):
        GImage.__init__(self, width=WORM_D, height=WORM_D, x=xpos, y=ypos, source=WORMHOLE)
        self._sister = None
        self._radius = 0.5*WORM_D
    
    
    def get_sister(self):
        return self._sister
    
    
    def w_distance(self, obj):
        """Returns the distance between the wormhole and the GImage object obj.
        """
        x1 = self.x
        y1 = self.y
        x2 = obj.x
        y2 = obj.y
        dx = abs(x2 - x1)
        dy = abs(y2 - y1)
        d = ((dx**2.0) + (dy**2.0))**0.5
        return d
    
    
    def warp_check(self, obj):
        """Returns True if the GImage object obj is within the wormhole's radius.
        """
        dist = self.w_distance(obj)
        if dist < self._radius:
            return True
        else:
            return False
    
    
    def sister(self, worm2):
        """Sets the _sister attribute of self to the Wormhole object worm2.
        If you want to pair two wormholes together, you must call this method
        for each one separately.
        """
        self._sister = worm2
    
    
    
# Additional Helper Function for planet_play.py File:
def pair(worm1, worm2):
    """Pairs the Wormhole objects worm1 and worm2 together.
    """
    worm1.sister(worm2)
    worm2.sister(worm1)