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
from svp_modules.game.gmod.gm_helper import *
from svp_modules.game.gmod.gm_sprite import SimpleSprite


class LittlePlatform(SimpleSprite):
  '''The platform/floor is just a rectangle, but it could be any sprite
  collision with rectangle objects is so easy, built-into pygame'''
  FLOOR_HEIGHT  =20

  def __init__(self):
    super().__init__()
    self.image = pygame.Surface((100, LittlePlatform.FLOOR_HEIGHT))
    self.image.fill((255,0,0))
    self.rect = self.image.get_rect(center = (HGame.Width/2, HGame.Height - 100))  # LittlePlatform.FLOOR_HEIGHT//2
    #although there is only one platform, it still needs to be added to a sprite group for collision detection purposes
    self.spriteGroup = pygame.sprite.Group()
    self.spriteGroup.add(self) 

  def check_collisions_with(self,obj):        
    plaform_hits = pygame.sprite.spritecollide(obj, self.spriteGroup, False)
    if obj.velocityY > 0:
      if plaform_hits:
        # when hitting the platform/floor, stop the Y movement (i.e., Y velocity becomes zero)
        obj.velocityY = 0.0 
        obj.posY = plaform_hits[0].rect.top + 1
