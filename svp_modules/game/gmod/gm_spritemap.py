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
import pygame as pg
import random as rand
from pygame.locals import *
import gm_const as gm_const

class SpriteMap():  
  def __init__(self,spritesheet_file):    
    self.spritesheet=pg.image.load(spritesheet_file)

  def load_one(self,sprite,color_key=gm_const.RGB_WHITE):
    location=sprite.get('location',(0,0))
    dim=sprite.get('dimension',(0,0))
    print('SpriteMap: loading sprite',sprite['name'])
    image=self.spritesheet.subsurface((location[0],location[1],dim[0],dim[1]))
    image.set_colorkey(color_key)      
    return image

  def load_many(self,sprite_list=[],color_key=gm_const.RGB_WHITE):
    images=[]
    for sprite in sprite_list:
      pose_image=self.load_one(sprite,color_key)
      images.append(pose_image.convert_alpha())
    return images

            
