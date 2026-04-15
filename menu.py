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

def set_difficulty(selected, index):
    text, value = selected 

    if text == 'Easy':
        HGame.Difficulty = 'easy'
    elif text == 'Hard':
        HGame.Difficulty = 'hard'
        
def make_menu(start_countdown):
    mytheme = Theme(
    background_color=(128, 128, 128, 200),

    title_font=pygame_menu.font.FONT_8BIT,  
    title_font_size=35,                      

    widget_font_size=16,
    widget_font_color=RGB_BLACK,

    cursor_color=(255, 0, 255),
    focus_background_color=(0, 0, 0,200),
    title_background_color=(0, 0, 128,200)
)
    HGame.Menu=pygame_menu.Menu('Cyber Infection', 600, 200,theme=mytheme)    
    HGame.Menu.add.label('Controls: LEFT, RIGHT, UP-jump, DOWN-hover/duck, Delete-Shoot \n \
        F2 - music toggle, F4 - switch characters, SPACE - pause toggle')
    #HGame.Menu.add.text_input('Name:', default='')
    HGame.Menu.add.selector('Difficulty:', [('Hard', 1), ('Easy', 2)], onchange=set_difficulty)
    HGame.Menu.add.button('Play', start_countdown)
    HGame.Menu.add.button('Controls', controls_menu())
    HGame.Menu.add.button('Quit', pygame_menu.events.EXIT)


def controls_menu():
    controls = pygame_menu.Menu('Controls', 600, 400)

    controls.add.label('Player 1 (Ramona)')
    controls.add.label('A / D - Move left/right')
    controls.add.label('W - Jump')
    controls.add.label('S - Hover')
    controls.add.label('F - Shoot')

    controls.add.label('')

    controls.add.label('Player 2 (Scott)')
    controls.add.label('Left Arrow / Right Arrow - Move')
    controls.add.label('Up Arrow - Jump')
    controls.add.label('Down Arrow - Duck')
    controls.add.button('Back', pygame_menu.events.BACK)

    return controls