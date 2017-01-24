# planets.py
# Zachary Mayle
# 5/29/16

from planet_constants import *
from game2d import *
from planet_play import *
import random


class Planets(GameApp):
    """Instance is the primary controller for the Planets app.
        Method start begins the application.
        
        Method update either changes the state or updates the Play object
        
        Method draw displays the Play object and any other elements on screen
        
        
    INSTANCE ATTRIBUTES:
        view    [Immutable instance of GView; it is inherited from GameApp]:
                the game view, used in drawing (see examples from class)
        input   [Immutable instance of GInput; it is inherited from GameApp]:
                the user input, used to control the paddle and change state
        _game   [Play, or None if there is no game currently active]: 
                the controller for a single game, which manages the paddle, ball, and bricks
        _background [GImage, or None if there is no background to display]
        _last_keys [int>=0]: the number of keys pressed last frame
        _state  [int between 0 and 6]: TITLE_SCREEN, NEW_GAME, READY, ACTIVE,
                FAIL, COMPLETE
        _level  [int>=0, <=highest level]: the game's current level, 0 if still at
                the title screen
        _msgs   [None or list of GLabel objects]: the messages to display on screen
        _sound  [Sound object or None]: the sound currently playing
        _stime  [int or float>=0]: amount of time in seconds since the current
                song started playing
        _songs  [None or list of Sound objects]: wav files, list of songs to be played,
                the index corresponds to the level number
    """
    
    
    def start(self):
        """Initializes the application.
        
        This method is distinct from the built-in initializer __init__ (which you 
        should not override or change). This method is called once the game is running. 
        You should use it to initialize any game specific attributes.
        """
        self._game = None
        self._background = GImage(x=0.5*GAME_WIDTH,y=0.5*GAME_HEIGHT,width=GAME_WIDTH,height=GAME_HEIGHT,source=None)
        self._last_keys = 0
        self._state = TITLE_SCREEN
        self._level = 0
        self._msgs = None
        self._sound = None
        self._stime = 0.0
    
    
    def update(self,dt):
        """Animates a single frame in the game."""
        if self._state == TITLE_SCREEN:
            self._title(dt)
        elif self._state == NEW_GAME:
            self._new_game()
        elif self._state == READY:
            self._ready(dt)
        elif self._state == ACTIVE:
            self._active(dt)
        elif self._state == FAIL:
            self._fail(dt)
        elif self._state == COMPLETE:
            self._complete(dt)
        self._check_keys()
        self._song_timer(dt)
    
    
    def _title(self,dt):
        """Helper to the method update.
        Manages the game's tasks on the title screen.
        """
        self._game = None
        self._msgs = [TITLE_1, TITLE_2, TITLE_3, TITLE_4]
        self._background.source = TITLE_BACKGROUND
        if self._last_keys == 0:
            if self.input.is_key_down('1'):
                self._level = 1
                self._state = NEW_GAME
            elif self.input.is_key_down('2'):
                self._level = 2
                self._state = NEW_GAME
            elif self.input.is_key_down('3'):
                self._level = 3
                self._state = NEW_GAME
            elif self.input.is_key_down('4'):
                self._level = 4
                self._state = NEW_GAME
            elif self.input.is_key_down('5'):
                self._level = 5
                self._state = NEW_GAME
            elif self.input.is_key_down('6'):
                self._level = 6
                self._state = NEW_GAME
            elif self.input.is_key_down('7'):
                self._level = 7
                self._state = NEW_GAME
            elif self.input.is_key_down('8'):
                self._level = 8
                self._state = NEW_GAME
            elif self.input.is_key_down('9'):
                self._level = 9
                self._state = NEW_GAME
            elif self.input.is_key_down('a'):
                self._level = 10
                self._state = NEW_GAME
            elif self.input.is_key_down('b'):
                self._level = 11
                self._state = NEW_GAME
            elif self.input.is_key_down('c'):
                self._level = 12
                self._state = NEW_GAME
            elif self.input.is_key_down('d'):
                self._level = 13
                self._state = NEW_GAME
            elif self.input.is_key_down('x'):
                self._level = 14
                self._state = NEW_GAME
            elif self.input.is_key_down('y'):
                self._level = 15
                self._state = NEW_GAME
            #ADD MORE IF STATEMENTS HERE AFTER ADDING NEW LEVELS!!!
    
    
    def _new_game(self):
        self._background.source = BACKGROUNDS[self._level]
        self._game = LEVELS[self._level]
        self._game.reset()
        self._state = READY
    
    
    def _ready(self,dt):
        self._msgs = [READY_1]
        if self._last_keys == 0:
            up = self.input.is_key_down('up')
            down = self.input.is_key_down('down')
            right = self.input.is_key_down('right')
            left = self.input.is_key_down('left')
            space = self.input.is_key_down('spacebar')
            if up or down or right or left or space:
                self._state = ACTIVE
    
    
    def _active(self,dt):
        self._msgs = None
        self._game.update_ship(self.input)
        self._game.teleport()
        if self._game.finish():
            self._state = COMPLETE
        elif self._game.planet_collide():
            self._state = FAIL
    
    
    def _fail(self,dt):
        self._msgs = [FAIL_1,FAIL_2]
        if self._last_keys == 0:
            if self.input.is_key_down('spacebar'):
                self._state = READY
                self._game.reset()
            elif self.input.is_key_down('m'):
                self._state = TITLE_SCREEN
                self._level = 0
    
    
    def _complete(self,dt):
        self._msgs = [COMPLETE_1,COMPLETE_2]
        if self._last_keys == 0:
            if self.input.is_key_down('spacebar'):
                if self._level < MAX_LEVEL:
                    self._level += 1
                    self._state = NEW_GAME
                else:
                    self._level = 0
                    self._state = TITLE_SCREEN
            elif self.input.is_key_down('m'):
                self._level = 0
                self._state = TITLE_SCREEN
    
    
    def _check_keys(self):
        """Records the number of keys currently being pressed in the attribute
        _last_keys. Must call this method at the end of every frame."""
        current_keys = self.input.key_count
        self._last_keys = current_keys
    
    
    def _song_timer(self, dt):
        """Plays the game's music and keeps track of how long each song has been playing.
        When a song ends, this method begins the next song.
        """
        if self._sound == None:
            song = SONGS[0]
            index = SONGS.index(song)
            self._sound = Sound(song)
            self._sound.volume = SOUND_VOLUME[index]
            self._stime = SOUND_LENGTH[index]
            self._sound.play()
        else:
            index = SONGS.index(self._sound.source)
            self._stime -= dt
            if self._stime <= 0.0:
                index += 1
                if index >= len(SONGS):
                    index = 0
                self._sound = Sound(SONGS[index])
                self._sound.volume = SOUND_VOLUME[index]
                self._stime = SOUND_LENGTH[index]
                self._sound.play()
    
    
    def draw(self):
        """Draws the game objects to the view.
        
        Every single thing you want to draw in this game is a GObject.  To draw a GObject 
        g, simply use the method g.draw(self.view).  It is that easy!
        
        Many of the GObjects (such as the paddle, ball, and bricks) are attributes in Play. 
        In order to draw them, you either need to add getters for these attributes or you 
        need to add a draw method to class Play.  We suggest the latter.  See the example 
        subcontroller.py from class.
        """
        if self._background.source != None:
            self._background.draw(self.view)
        if self._game != None:
            self._game.draw(self.view)
        if self._msgs != None:
            for i in self._msgs:
                i.draw(self.view)