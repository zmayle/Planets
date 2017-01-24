# planet_constants.py
# Zachary Mayle
# 5/29/16

from game2d import *

##### Game Specs
#: width of the game display
GAME_WIDTH = 1400
#: height of the game display
GAME_HEIGHT = 750


##### Ship Specs
#: the ship's width
SHIP_WIDTH = 49
#: the ship's height
SHIP_HEIGHT = 50
#: the ship's mass
SHIP_MASS = 1.0
#: ship thrust acceleration when facing a cardinal direction
SHIP_ACCEL_1 = 0.1
#: ship thrust for each cardinal direction when facing diagonal
SHIP_ACCEL_2 = 0.1*(2.0**0.5) / 2.0
#: image for the ship
SHIP_IMAGE = "spaceship.png"


##### Wormhole Specs
#: the wormhole's diameter
WORM_D = 100
#: the wormhole's source image
WORMHOLE = "wormhole.png"


##### Start Point Specs
#: starting point width
START_WIDTH = 100
#: starting point height
START_HEIGHT = 100
#: starting point source image
START_PIC = "start.png"


##### Finish Point Specs
#: finish point width
FINISH_WIDTH = 100
#: finish point height
FINISH_HEIGHT = 100
#: finish point source image
FINISH_PIC = "earth.png"


##### Physics Specs
#: Gravitational Constant
G = 0.7*5000.0   #5000.0


##### State Specs
TITLE_SCREEN = 0
NEW_GAME = 1
READY = 2
ACTIVE = 3
FAIL = 4
CONTINUE = 5
COMPLETE = 6

##### Messages
#: list of title screen messages
clear = colormodel.RGB(0,0,0,0)
gray = colormodel.RGB(0,0,0, a= 100)
TITLE_1 = GLabel(text="PLANETS",font_size=120,font_name="good times rg.ttf",\
                 x=.5*GAME_WIDTH,y=.65*GAME_HEIGHT,linecolor=colormodel.BLUE,fillcolor=clear)
TITLE_2 = GLabel(text="USE DIRECTIONAL PAD TO NAVIGATE YOUR SHIP TO THE FINISH",\
                 font_size=24,font_name="good times rg.ttf",\
                 x=.5*GAME_WIDTH,y=.4*GAME_HEIGHT,linecolor=colormodel.WHITE,fillcolor=gray)
TITLE_3 = GLabel(text="Tap a key to pick a level:",\
                 font_size=24,font_name="good times rg.ttf",\
                 x=.5*GAME_WIDTH,y=.2*GAME_HEIGHT,linecolor=colormodel.WHITE,fillcolor=gray)
TITLE_4 = GLabel(text="1   2   3   4   5   6   7   8   9\nA   B   C   D\nX   Y",\
                 font_size=24,font_name="good times rg.ttf",\
                 x=.5*GAME_WIDTH,y=.1*GAME_HEIGHT,linecolor=colormodel.WHITE,fillcolor=gray)
#: ready state message
READY_1 = GLabel(text="TO INFINITY AND BEYOND!",font_size=48,font_name="good times rg.ttf",\
                 x=.5*GAME_WIDTH,y=.5*GAME_HEIGHT,linecolor=colormodel.WHITE,fillcolor=gray)
#: fail state message
FAIL_1 = GLabel(text="EPIC FAIL",font_size=48,font_name="good times rg.ttf",\
                x=.5*GAME_WIDTH,y=.6*GAME_HEIGHT,linecolor=colormodel.WHITE,fillcolor=gray)
FAIL_2 = GLabel(text="PRESS SPACE TO TRY AGAIN\nPRESS M TO RETURN TO MENU",\
                font_size=36,font_name="good times rg.ttf",\
                x=.5*GAME_WIDTH,y=.3*GAME_HEIGHT,linecolor=colormodel.WHITE,fillcolor=gray)
#: complete state messages
COMPLETE_1 = GLabel(text="YOU WIN!",font_size=72,font_name="good times rg.ttf",\
                x=.5*GAME_WIDTH,y=.6*GAME_HEIGHT,linecolor=colormodel.BLUE,fillcolor=gray)
COMPLETE_2 = GLabel(text="PRESS SPACE TO PROCEED TO NEXT LEVEL\nPRESS M TO RETURN TO MENU",\
                font_size=36,font_name="good times rg.ttf",\
                x=.5*GAME_WIDTH,y=.3*GAME_HEIGHT,linecolor=colormodel.BLUE,fillcolor=gray)

##### Backgrounds
#: title screen background
TITLE_BACKGROUND = "Quasar.jpg"
#: level 1 background
L1_BACKGROUND = "Hubble1.jpg"
#: level 2 background
L2_BACKGROUND = "space1.jpg"

L3_BACKGROUND = "space2.jpg"

L4_BACKGROUND = "space3.jpg"

L5_BACKGROUND = "space4.jpg"
#: background list
BACKGROUNDS = [TITLE_BACKGROUND, L1_BACKGROUND, L2_BACKGROUND, L3_BACKGROUND,\
               L4_BACKGROUND, L5_BACKGROUND, L1_BACKGROUND, L2_BACKGROUND, L3_BACKGROUND,\
               L4_BACKGROUND, L5_BACKGROUND, L1_BACKGROUND, L2_BACKGROUND, L3_BACKGROUND,\
               L4_BACKGROUND, L5_BACKGROUND]


##### Songs
#: list of songs, index corresponds to level
SONGS = ["Nigel_Good_-_It_Starts.wav", "Nigel_Good_-_This_Is_Forever.wav", "An_Adventure.wav", "Stellar.wav"]
#: list of song volumes, each specific to the corresponding song in the above list
SOUND_VOLUME = [1.0, 1.0, 1.0, 1.0]
#: list of the song lengths, in seconds
SOUND_LENGTH = [106.0, 178.0, 111.0, 194.0]