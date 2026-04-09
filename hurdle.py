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

CORONA_SPRITES=[      
    {'name':"virus variant 1",  'location':(18,66), 'dimension':(118,114)},
    {'name':"virus variant 2",  'location':(221,64), 'dimension':(109,111)},
    {'name':"virus variant 3",  'location':(135,22), 'dimension':(73,79)},
    {'name':"virus variant 3",  'location':(257,241), 'dimension':(73,79)}]

class Hurdle(SimpleSprite):
  '''The hurdle is just a rectangle, but it could be any sprite
  collision with rectangle objects is dead easy, built-into pygame'''

  def __init__(self):
    super().__init__()

    #create a sprite group for hurdle
    #this is necessary to get access to the built-in sprite collision function spritecollide
    self.spriteGroup = pygame.sprite.Group()
    self.spriteGroup.add(self)

    self.sm=SpriteMap(getSpriteFile('corona/0ef191bf29bb89631d5527f681735e03.png'))
    self.image_list=self.sm.load_many(CORONA_SPRITES,color_key=RGB_WHITE)

    self.dead=False
    self.reset()

  def check_collisions_with(self,obj):     
    hurdle_hit = pygame.sprite.spritecollide(obj, self.spriteGroup, False)
    if hurdle_hit:
      # when coliding with other object, stop the jumper X movement, exacly at the X position where it got hit
      # also make them dead
      obj.velocityX = 0.0
      obj.posX = hurdle_hit[0].rect.left #there is only one hurdle in this group, hence hurdle_hit[0] will always work      
      obj.die()#always, deadly collision! :( - reconsider? health? stamina?, damage model?, broken bones? healthcare healing prizes?
  
  def mutate(self):
    image_index=rand.randint(0,len(self.image_list)-1)
    self.image=self.image_list[image_index]
    self.rect = self.image.get_rect()    
    random_Y_pos=rand.randint(self.rect.height,HGame.Height)    
    self.rect.midbottom = (HGame.Width,random_Y_pos)
    
  def reset(self):
    '''resets the position to the right side of the screen and, velocity to HURDLE_VELOCITY'''
    self.mutate()
    self.posX=HGame.Width-self.rect.width//2
    self.velocityX=HURDLE_VELOCITY
    self.accelX=0
    self.dead=False
    self.posX = HGame.Width
    

  def redraw(self):
    if self.posX < -self.rect.width // 2:      
      self.reset()
    self.rect.x = self.posX

  def move(self):
    '''Hurdle moves, or is it the Jumper that runs? Whatever your point of view,
    for now, X accelleration is zero, but one can imagine a hurdle slowing down or speeding up for various reasons'''
    self.accelX = 0#ACCELERATION_CONST
    self.posX -= self.velocityX + MOVE_TIME_CONST * self.accelX
    
    if self.posX > HGame.Width:
      self.posX = 0 #wrap around

  def die(self):
    self.dead=True
    #dramatic explosion?
    self.reset()

  def update(self):
    if not self.dead:
      self.move()
      self.redraw()

