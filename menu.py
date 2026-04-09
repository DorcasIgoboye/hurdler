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

from svp_modules.game.gmod.gm import HGame
import pygame_menu #https://pygame-menu.readthedocs.io/en/4.0.2/
from pygame_menu import Theme
import pygame as pygame
from pygame.locals import *
from consts import *
from svp_modules.game.gmod.gm_const import *

def set_difficulty(value, difficulty):
    pass

def make_menu(start_countdown):
    mytheme = Theme(background_color=(128, 128, 128, 200), # transparent background
                    #title_shadow=True,
                    #widget_font=pygame_menu.font.FONT_COMIC_NEUE,
                    widget_font_size=16,
                    widget_font_color=RGB_BLACK,
                    #widget_font_shadow=True,
                    cursor_color=(255, 0, 255),
                    cursor_selection_color=(255, 0, 0,0),
                    focus_background_color=(0, 0, 0,200),
                    title_background_color=(0, 0, 128,200)
                    )
    HGame.Menu=pygame_menu.Menu('Hurdler (COVID-19)', 600, 200,theme=mytheme)    
    HGame.Menu.add.label('Controls: LEFT, RIGHT, UP-jump, DOWN-hover/duck, Delete-Shoot \n \
        F2 - music toggle, F4 - switch characters, SPACE - pause toggle')
    #HGame.Menu.add.text_input('Name:', default='')
    #HGame.Menu.add.selector('Difficulty:', [('Hard', 1), ('Easy', 2)], onchange=set_difficulty)
    HGame.Menu.add.button('Play', start_countdown)
    HGame.Menu.add.button('Quit', pygame_menu.events.EXIT)
