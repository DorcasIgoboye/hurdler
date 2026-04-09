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

import pygame as pygame
from pygame.locals import *

import config
from svp_modules.game.gmod.gm import HGame
from svp_modules.game.gmod.gm_const import *
from svp_modules.game.gmod.gm_timer import Timer

from consts import *

def game_reset_callback(timer):
  '''The callback from the end game timer that resets the game after displaying the dramatic ending'''
  HGame.Reset()

#this is the timer object that waits for the display of end game background and sad music
#after the 7200 milliseconds period it callsback the game reset game_reset_callback() function
#which in turn, resets the game
endGameTimer=Timer(period=7200,end_callback=game_reset_callback,iterations=1,paused=True)

def gameover_display():
  HGame.BGImgLoad(GAME_OVER_BACKGROUNG_IMAGE)
  HGame.Music=False #stop current background music, if any
  HGame.BGMusicLoad(SAD_MUSIC_FILE)
  HGame.Music=True # start sad music
  endGameTimer.restart()