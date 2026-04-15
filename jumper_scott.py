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
import config
from svp_modules.game.gmod.gm import HGame
from svp_modules.game.gmod.gm_const import *
from svp_modules.game.gmod.gm_helper import *
from svp_modules.game.gmod.gm_spritemap import SpriteMap
from svp_modules.game.gmod.gm_timer import Timer
from jumper import Jumper

from consts import *

class Scott(Jumper):
  """Sprite for main jumper character"""
  
  def __init__(self, player_id=2):
    '''Jumper construction, now since we have separated the jumper from the game
    the game object must be available for referencing, so we pass it along in the init, 
    as a parameter, every time we construct the Jumper'''
    super().__init__(SCOTT_SPRITES, color_key=(46,255,130), player_id=player_id)
    #initialize additional behaviour
    self.ducking=False
    self.duckSpriteImage=self.smap.load_one(SCOTT_SPRITES['duck_sprite'],color_key=(46,255,130))
 
  def start_ducking(self):
    '''Ramona can shoot foam'''
    if not self.dead and not self.ducking:
      self.ducking=True      
      
  def redraw_ducking(self):
    HGame.TextOutMiddle("Ducking...")    
    self.image=self.duckSpriteImage    
    self.rect=self.image.get_rect()
    self.rect.midbottom = (self.posX,self.posY+10)    
     
  def update(self,lkey,rkey,downkey):
    '''
    Scott moves, ducks,
    and redraw herself in new poses/position
    '''
    self.update_immunity_counter()
    if not self.dead:
      if downkey and self.velocityX<=0.1 and self.posY>=(HGame.Height-self.rect.height-10):
        self.start_ducking()        
      else:
        self.ducking=False

      self.move(lkey,rkey)

      if self.ducking:              
        self.redraw_ducking()
      else:# normal redraw
        self.redraw()
