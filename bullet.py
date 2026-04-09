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

import config
import pygame as pygame
from svp_modules.game.gmod.gm import HGame
from svp_modules.game.gmod.gm_const import *
from svp_modules.game.gmod.gm_helper import *
from svp_modules.game.gmod.gm_spritemap import SpriteMap
from svp_modules.game.gmod.gm_sprite import SimpleSprite

from consts import *
import random as rand

FOAM_SPRITES=[      
      {'name':"foam 1",  'location':(105,86), 'dimension':(82,94)},
      {'name':"foam bullet 2",  'location':(100,0), 'dimension':(90,79)}
    ]     

class Bullet(SimpleSprite):
  '''The bullet collision with rectangle objects, built-into pygame'''

  def __init__(self):
    super().__init__()        
    #create a sprite group
    #this is necessary to get access to the built-in 
    # sprite collision function spritecollide
    self.spriteGroup = pygame.sprite.Group()
    self.spriteGroup.add(self) 

    self.sm=SpriteMap(getSpriteFile('ClipartKey_695317_bubbles_small.png'))
    self._images=self.sm.load_many(FOAM_SPRITES,color_key=(0,0,0))
    self.flying=False
        
  def check_collisions_with(self,obj):     
    if self.flying:
      bullet_hit = pygame.sprite.spritecollide(obj, self.spriteGroup, False)
      if bullet_hit:
        # when coliding with hurdle, stop the object X movement, exactly at the X position where it got hit
        # also make them dead
        obj.velocityX = 0.0
        obj.posX = bullet_hit[0].rect.left #there is only one bullet in this sprite group, hence hurdle_hit[0] will always work      
        obj.die()# die virus die!

  def start_fly(self,posX,posY):
    self.posX=posX 
    self.posY=posY 
    self.velocityX=BULLET_VELOCITY
    self.accelX=0
    self.flying=True
    self.image=self._images[0]
    self.rect=self.image.get_rect()    
    self.rect.midbottom = (HGame.Width,self.posY)    
    HGame.ShowSprite(self)

  def redraw_fly(self):#,posX,posY
    '''
    redraw bullet flying
    '''
    image_index=rand.randint(0,len(self._images)-1)
    self.image=self._images[image_index]
    self.rect=self.image.get_rect()    
    self.rect.midbottom = (self.posX,self.posY)    

  def move(self):
    '''bullet moves,
    for now, X accelleration is zero, but one can imagine objects slowing down or speeding up for various reasons'''
    self.accelX = 0#ACCELERATION_CONST
    self.posX += self.velocityX + MOVE_TIME_CONST * self.accelX
    
    if self.posX > HGame.Width:      
      HGame.HideSprite(self)
      self.flying=False          

  def update(self):
    if self.flying:
      self.move()
      self.redraw_fly()

