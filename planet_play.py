# planet_play.py
# Zachary Mayle
# 5/29/16

from planet_constants import *
from game2d import *
from planet_models import *
import random


class Play(object):
    """An instance controls a single game of planets.
    
    This subcontroller animates the game by moving the ship and by influencing
    the ship with the planets' gravity. When the game is failed or won, it stops
    animating. To start a new game of planets, you should create a new Play object.
    
    ATTRIBUTES:
        _ship [Ship object] the player's ship for the current game
        _planets [list of Planet objects or None] a list of the planets in the current game
        _start [GImage object] starting point for the player's ship
        _finish [Gimage object] finish point for the player's ship
        _wormholes [list of Wormhole objects or None] list of the two wormholes in the
            current game (they should be paired)
    
    This class contains methods for updating the ship, drawing all of the game objects,
    determining if the ship collides with a planet, checking if the ship enters a wormhole,
    and checking if the ship has reached the finish line.
    """
    
    def __init__(self, startx, starty, finishx, finishy, worm1=None, worm2=None, planets=None):
        """Initializer: Creates a Play object that controls the current game.
        
        PARAMETERS:
            startx [int>=0] x position of the start point
            starty [int>=0] y position of the start point
            finishx [int>=0] x position of the finish point
            finishy [int>=0] y position of the start point
            worm1 [Wormhole object or None]
            worm2 [Wormhole object or None] must be different from worm1
            planets [list of planet objects or None] list of planet objects in the level
            """
        self._start = GImage(x=startx, y=starty, width=START_WIDTH, height= START_HEIGHT,\
                             source=START_PIC)
        self._finish = GImage(x=finishx, y=finishy, width=FINISH_WIDTH, height= FINISH_HEIGHT,\
                             source=FINISH_PIC)
        self._wormholes = None
        if worm1 != None and worm2 != None:
            pair(worm1, worm2)
            self._wormholes = [worm1, worm2]
        self._ship = Ship(self._start.x, self._start.y)
        self._planets = planets
    
    
    def update_ship(self, inp):
        ship = self._ship
        ship.move_ship()
        self._gravity()
        self._thrust_ship(inp)
        self._in_bounds()
    
    
    def _gravity(self):
        """Helper to the method update_ship.
        This method accelerates the ship with gravity from each planet in the
        game. If there are no planets, this method does nothing.
        """
        if self._planets != None:
            for i in self._planets:
                m1 = i.get_mass()
                m2 = self._ship.get_mass()
                r = i.p_distance(self._ship)
                force = (G * m1 * m2) / (r**2.0)
                cos, sin = i.get_trig(self._ship)
                fx = -force * cos   #I added negatives to this expression to ensure force
                fy = -force * sin   #is in the correct direction
                ax = fx / self._ship.get_mass()
                ay = fy / self._ship.get_mass()
                self._ship.accel_ship(ax, ay)
    
    
    def _thrust_ship(self, inp):
        """Helper to the method update_ship.
        This method accelerates the ship if the player presses any of the arrow
        keys. It also rotates the ship to the correct orientation based on which
        arrow keys are pressed.
        """
        ship = self._ship
        if inp.is_key_down('up') and inp.is_key_down('right'):
            ship.angle = 315
            ship.accel_ship(SHIP_ACCEL_2, SHIP_ACCEL_2)
        elif inp.is_key_down('up') and inp.is_key_down('left'):
            ship.angle = 45
            ship.accel_ship(-SHIP_ACCEL_2, SHIP_ACCEL_2)
        elif inp.is_key_down('down') and inp.is_key_down('left'):
            ship.angle = 135
            ship.accel_ship(-SHIP_ACCEL_2, -SHIP_ACCEL_2)
        elif inp.is_key_down('down') and inp.is_key_down('right'):
            ship.angle = 225
            ship.accel_ship(SHIP_ACCEL_2, -SHIP_ACCEL_2)
        elif inp.is_key_down('up'):
            ship.angle = 0
            ship.accel_ship(0, SHIP_ACCEL_1)
        elif inp.is_key_down('down'):
            ship.angle = 180
            ship.accel_ship(0, -SHIP_ACCEL_1)
        elif inp.is_key_down('right'):
            ship.angle = 270
            ship.accel_ship(SHIP_ACCEL_1, 0)
        elif inp.is_key_down('left'):
            ship.angle = 90
            ship.accel_ship(-SHIP_ACCEL_1, 0)
    
    
    def _in_bounds(self):
        """Helper to the method update_ship.
        This method negates the ship's x velocity if it exceeds the game's x bounds
        and negates the ship's y velocity if it exceeds the game's y bounds.
        """
        ship = self._ship
        x = ship.x
        y = ship.y
        if x < 0 or x > GAME_WIDTH:
            ship.set_xv(-ship.get_xv())
        if y < 0 or y > GAME_HEIGHT:
            ship.set_yv(-ship.get_yv())
    
    
    def draw(self, view):
        """Draws the game objects into view, where view is an instance of GView.
        Draws the objects in the following order:
            planets
            finish point
            start point
            ship
            wormholes
        """
        if self._planets != None:
            for i in self._planets:
                i.draw(view)
        self._finish.draw(view)
        self._start.draw(view)
        self._ship.draw(view)
        if self._wormholes != None:
            for j in self._wormholes:
                j.draw(view)
    
    
    def planet_collide(self):
        """Returns True if the ship collides with a planet. False otherwise.
        """
        verdict = False
        if self._planets != None:
            for j in self._planets:
                check = j.collision_check(self._ship)
                verdict = verdict or check
        width = self._ship.x > GAME_WIDTH or self._ship.x < 0
        height = self._ship.y>GAME_HEIGHT or self._ship.y < 0
        return verdict or width or height
    
    
    def teleport(self):
        """This function handles everything involved with teleporting the ship
        throught the wormholes.
            1) If there are no wormholes, this method does nothing.
            2) If the ship touches a wormhole and the ship's teleport attribute
                is False, then the ship is moved to that wormhole's sister. The
                ship's teleport attribute is then set to True.
            3) If the ship touches a wormhole and its teleport attribute is True,
                then nothing happens.
            4) If the ship is not touching a wormhole, then this method sets the ship's
                teleport attribute to True.
        """
        if self._wormholes != None:
            spaceship = self._ship
            total_warp = False        #total_warp=whether ship is touching any wormholes
            for i in self._wormholes:       #checking for each wormhole
                warp = i.warp_check(spaceship)  #check if ship enters wormhole
                total_warp = total_warp or warp #recording if ship is touching any wormhole
                if warp and (not spaceship.get_teleport()):
                    spaceship.set_teleport(True)
                    spaceship.x = i.get_sister().x
                    spaceship.y = i.get_sister().y
            if not total_warp:
                spaceship.set_teleport(False)
    
    
    def finish(self):
        """Returns True if the ship reaches the finish area. False otherwise.
        """
        end = self._finish
        if end.contains(self._ship.x, self._ship.y):
            return True
        else:
            return False
    
    
    def reset(self):
        """Resets the level so that the ship is back at the starting point.
        """
        self._ship.x = self._start.x
        self._ship.y = self._start.y
        self._ship.set_xv(0.0)
        self._ship.set_yv(0.0)
        self._ship.angle = 0


# List of levels
L0 = None
L1 = Play(50, 50, GAME_WIDTH-50, GAME_HEIGHT-50)

P21 = Planet(0.5*GAME_WIDTH,0.5*GAME_HEIGHT,m=1.0,r=100.0,src="mars.png")
L2 = Play(50, 50, GAME_WIDTH-50, GAME_HEIGHT-50, planets=[P21])

P31 = Planet(0.2*GAME_WIDTH,0.8*GAME_HEIGHT,m=1.0,r=100.0,src="mars.png")
P32 = Planet(0.5*GAME_WIDTH,0.2*GAME_HEIGHT,m=3.0,r=300.0,src="jupiter.png")
P33 = Planet(0.8*GAME_WIDTH,0.9*GAME_HEIGHT,m=5.0,r=50.0,src="black_hole.png")
L3 = Play(50, 50, GAME_WIDTH-50, GAME_HEIGHT-50, planets=[P31, P32, P33])

P41 = Planet(0.2*GAME_WIDTH, 0.3*GAME_HEIGHT, m=1.0, r=100.0, src="mars.png")
P42 = Planet(0.6*GAME_WIDTH, 0.3*GAME_HEIGHT, m=1.0, r=100.0, src="neptune.png")
P43 = Planet(0.4*GAME_WIDTH, 0.7*GAME_HEIGHT, m=1.0, r=100.0, src="neptune.png")
P44 = Planet(0.8*GAME_WIDTH, 0.7*GAME_HEIGHT, m=1.0, r=100.0, src="mars.png")
L4 = Play(50, 50, GAME_WIDTH-50, GAME_HEIGHT-50, planets=[P41, P42, P43, P44])

P51 = Planet(0, GAME_HEIGHT, m=5.0, r=300.0, src="neptune.png")
P52 = Planet(GAME_WIDTH, GAME_HEIGHT, m=5.0, r=300.0, src="venus.png")
P53 = Planet(0.55*GAME_WIDTH, 0.3*GAME_HEIGHT, m=1.0, r=100.0, src="mars.png")
P54 = Planet(0.65*GAME_WIDTH, 0.5*GAME_HEIGHT, m=1.0, r=100.0, src="mars.png")
P55 = Planet(0.75*GAME_WIDTH, 0.7*GAME_HEIGHT, m=1.0, r=100.0, src="mars.png")
L5 = Play(0.5*GAME_WIDTH, GAME_HEIGHT-50, GAME_WIDTH-50, 150, planets=[P51, P52, P53, P54, P55])

W61 = Wormhole(0.4*GAME_WIDTH, 50)
W62 = Wormhole(0.6*GAME_WIDTH, GAME_HEIGHT-50)
P61 = Planet(0.5*GAME_WIDTH, 0.8*GAME_HEIGHT, m=1.0, r=100.0, src="mars.png")
P62 = Planet(0.5*GAME_WIDTH, 0.5*GAME_HEIGHT, m=1.0, r=100.0, src="mars.png")
P63 = Planet(0.5*GAME_WIDTH, 0.2*GAME_HEIGHT, m=1.0, r=100.0, src="mars.png")
L6 = Play(50, GAME_HEIGHT-50, GAME_WIDTH-50, 50, worm1=W61, worm2=W62, planets=[P61, P62, P63])

W71 = Wormhole(0.3*GAME_WIDTH, 0.5*GAME_HEIGHT)
W72 = Wormhole(0.7*GAME_WIDTH, 0.5*GAME_HEIGHT)
P71 = Planet(0.5*GAME_WIDTH, 0.5*GAME_HEIGHT, m=10.0, r=200, src="jupiter.png")
P72 = Planet(0.5*GAME_WIDTH, 0.1*GAME_HEIGHT, m=1.0, r=100, src="mars.png")
P73 = Planet(0.5*GAME_WIDTH, 0.9*GAME_HEIGHT, m=1.0, r=100, src="mars.png")
L7 = Play(0.2*GAME_WIDTH, 0.5*GAME_HEIGHT, GAME_WIDTH-50, 50, worm1=W71, worm2=W72, planets=[P71, P72, P73])

W81 = Wormhole(0.25*GAME_WIDTH, 0.6*GAME_HEIGHT)
W82 = Wormhole(0.7*GAME_WIDTH, 0.85*GAME_HEIGHT)
P81 = Planet(0.15*GAME_WIDTH, 0.5*GAME_HEIGHT, m=1.0, r=125, src="venus.png")
P82 = Planet(0.5*GAME_WIDTH, 0.5*GAME_HEIGHT, m=3.0, r=250, src="neptune.png")
P83 = Planet(0.9*GAME_WIDTH, 0.1*GAME_HEIGHT, m=1.0, r=50, src="mars.png")
P84 = Planet(40, 0.5*GAME_HEIGHT, m=0.0, r=40, src="moon.png")
L8 = Play(50, GAME_HEIGHT-50, 50, 50, worm1=W81, worm2=W82, planets=[P81, P82, P83, P84])

W91 = Wormhole(0.65*GAME_WIDTH, 0.6*GAME_HEIGHT)
W92 = Wormhole(0.2*GAME_WIDTH, 0.45*GAME_HEIGHT)
P91 = Planet(0.2*GAME_WIDTH, 0.1*GAME_HEIGHT, m=3.0, r=75, src="jupiter.png")
P92 = Planet(0.5*GAME_WIDTH, 0.2*GAME_HEIGHT, m=1.0, r=50, src="mars.png")
P93 = Planet(0.5*GAME_WIDTH, 0.7*GAME_HEIGHT, m=0.5, r=40, src="venus.png")
P94 = Planet(0.5*GAME_WIDTH, 1.1*GAME_HEIGHT, m=4.0, r=200, src="sun.png")
P95 = Planet(0.8*GAME_WIDTH, 0.6*GAME_HEIGHT, m=3.0, r=100, src="neptune.png")
L9 = Play(GAME_WIDTH-50, GAME_HEIGHT-50, 50, 50, worm1=W91, worm2=W92, planets=[P91, P92, P93, P94, P95])

WA1 = Wormhole(0.3*GAME_WIDTH, 0.5*GAME_HEIGHT)
WA2 = Wormhole(0.3*GAME_WIDTH, 0.9*GAME_HEIGHT)
PA1 = Planet(0.3*GAME_WIDTH, 0.35*GAME_HEIGHT, m=7.0, r=30, src="black_hole.png")
LA = Play(0.3*GAME_WIDTH, 0.8*GAME_HEIGHT, 0.8*GAME_WIDTH, 0.2*GAME_HEIGHT, worm1=WA1, worm2=WA2, planets=[PA1])

WB1 = Wormhole(0.55*GAME_WIDTH,0.5*GAME_HEIGHT)
WB2 = Wormhole(0.75*GAME_WIDTH,0.5*GAME_HEIGHT)
PB1 = Planet(0.41*GAME_WIDTH, 0.5*GAME_HEIGHT, m=4.0, r=150, src="jupiter.png")
PB2 = Planet(0.65*GAME_WIDTH, 0.5*GAME_HEIGHT, m=3.0, r=80, src="neptune.png")
PB3 = Planet(0.05*GAME_WIDTH, 0.6*GAME_HEIGHT, m=0, r=70, src="mars.png")
PB4 = Planet(0.15*GAME_WIDTH, 0.55*GAME_HEIGHT, m=0, r=70, src="moon.png")
PB5 = Planet(0.25*GAME_WIDTH, 0.5*GAME_HEIGHT, m=0, r=70, src="mars.png")
PB6 = Planet(0.93*GAME_WIDTH, 0.27*GAME_HEIGHT, m=0, r=90, src="venus.png")
LB = Play(50, GAME_HEIGHT-50, 50, 0.45*GAME_HEIGHT, worm1=WB1, worm2=WB2, planets=[PB1, PB2, PB3, PB4, PB5, PB6])

PC1 = Planet(0.35*GAME_WIDTH, 0.65*GAME_HEIGHT, m=3.0, r=150, src="jupiter.png")
PC2 = Planet(0.65*GAME_WIDTH, 0.35*GAME_HEIGHT, m=1.0, r=75, src="moon.png")
LC = Play(50, 50, GAME_WIDTH-50, GAME_HEIGHT-50, planets=[PC1, PC2])

PD1 = Planet(0.5*GAME_WIDTH, -0.1*GAME_HEIGHT, m=5.0, r=350, src="sun.png")
PD2 = Planet(0.5*GAME_WIDTH, 1.1*GAME_HEIGHT, m=3.0, r=200, src="neptune.png")
LD = Play(50, 50, GAME_WIDTH-50, GAME_HEIGHT-50, planets=[PD1, PD2])

PX1 = Planet(0.5*GAME_WIDTH, 0.5*GAME_HEIGHT, m=10.0, r=200, src="black_hole.png")
LX = Play(50, 0.5*GAME_HEIGHT, GAME_WIDTH-50, 0.5*GAME_HEIGHT, planets=[PX1])

PY1 = Planet(0.35*GAME_WIDTH, 0.65*GAME_HEIGHT, m=3.0, r=100, src="mars.png")
PY2 = Planet(0.65*GAME_WIDTH, 0.65*GAME_HEIGHT, m=3.0, r=100, src="venus.png")
PY3 = Planet(0.5*GAME_WIDTH, -0.1*GAME_HEIGHT, m=1.0, r=250, src="sun.png")
LY = Play(0.5*GAME_WIDTH, 0.5*GAME_HEIGHT, 50, GAME_HEIGHT-50, planets=[PY1, PY2, PY3])


LEVELS = [L0, L1, L2, LC, LD, LX, LY, L5, L4, L3, L6, L9, L7, L8, LA, LB]
MAX_LEVEL = len(LEVELS) - 1