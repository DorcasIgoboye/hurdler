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
from svp_modules.game.gmod.gm_helper import *

from consts import *

count_images = [
    pygame.image.load(getImageFile('count_3.png')),
    pygame.image.load(getImageFile('count_2.png')),
    pygame.image.load(getImageFile('count_1.png')),
    pygame.image.load(getImageFile('count_go.png'))
]

beep_sound = pygame.mixer.Sound(getSoundFile(COUNTDOWN_BEEP))
go_sound = pygame.mixer.Sound(getSoundFile(COUNTDOWN_GO))


last_index = -1

offsets = [
    (20, 0),     # 3
    (40, 0),   # 2 (tweak if needed)
    (0, 0),     # 1
    (15, 0)    # GO (usually needs more)
]

def game_countdown_display():
    global last_index

    index = beginGameTimer.count

    if index != last_index:
        if index < 3:
            beep_sound.play()
        elif index == 3:
            go_sound.play()
        last_index = index

    if index < 4:
        img = count_images[index]
        ox, oy = offsets[index]

        rect = img.get_rect(center=(HGame.MidX + ox, HGame.MidY + oy))
        HGame.Canvas.blit(img, rect)
def game_begin_callback(timer):
  HGame.Begin()

beginGameTimer=Timer(period=1000, end_callback=game_begin_callback,iterations=4,paused=True)

def begin_countdown():
  HGame.ShowCountdown=True
  beginGameTimer.restart()        


