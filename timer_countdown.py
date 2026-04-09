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

def game_countdown_display():
  COUNTDOWN_TEXT=['Ready','Set','Go!']
  HGame.Font = pygame.font.SysFont('mono', 80, bold=True)  
  HGame.TextOutMiddle(COUNTDOWN_TEXT[beginGameTimer.count],color=RGB_GREEN)
  HGame.Font = pygame.font.SysFont('mono', 20, bold=True)   


def game_begin_callback(timer):
  HGame.Begin()

beginGameTimer=Timer(period=1000, end_callback=game_begin_callback,iterations=3,paused=True)

def begin_countdown():
  HGame.ShowCountdown=True
  beginGameTimer.restart()        


