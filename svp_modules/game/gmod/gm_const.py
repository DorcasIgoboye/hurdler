'''
    Copyright (C) 2021-2022 Stefan V. Pantazi (svpantazi@gmail.com)    
    
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see http://www.gnu.org/licenses/.
'''

import pygame
from pygame.locals import *
from pygame import USEREVENT

TIMERS=[] #global storage of timer objects - class defined in gm_timer

#game module constants
RGB_WHITE=(255,255,255)
RGB_BLACK=(0,0,0)
RGB_PURPLE=(255,0,255)
RGB_RED=(255,0,0)
RGB_GREEN=(0,255,0)

DEFAULT_FPS=30
MAX_TIMERS=1000
GLOBAL_TIMER_EVENT  = pygame.USEREVENT + 1000
DEFAULT_PYGAME_WINDOW_CAPTION="Default PyGame window"
DEFAULT_GAME_WINDOW_SIZE=(640,480)
MUSIC_EVENTS=116
MUSIC_END_EVENT = USEREVENT + MUSIC_EVENTS +1

PAUSE_TOGGLE_KEY=pygame.K_SPACE
MUSIC_TOGGLE_KEY=pygame.K_F2
   
ASSET_PATH_IMAGES="assets/images"
ASSET_PATH_SPRITES=ASSET_PATH_IMAGES+"/sprites"
ASSET_PATH_SOUNDS="assets/sounds"
ASSET_PATH_MUSIC=ASSET_PATH_SOUNDS+"/music"

