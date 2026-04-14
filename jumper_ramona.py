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
from jumper import Jumper
from consts import *

from bullet import Bullet

class Ramona(Jumper):
  """Sprite for main jumper character"""
  
  def __init__(self, player_id=1):
    '''Jumper construction, now since we have separated the jumper from the game
    the game object must be available for referencing, so we pass it along in the init, 
    as a parameter, every time we construct the Jumper'''
    super().__init__(RAMONA_SPRITES, color_key=(203,217,217), player_id=player_id)

    #initialize additional behaviour
    #setting shoot sound
    self.shootSound=pygame.mixer.Sound(getSoundFile("tx0_fire1.wav"))    
    self.shootImages=self.smap.load_many(RAMONA_SHOOT_SPRITE_SEQUENCE['shooting_sprites'],color_key=(203,217,217))
    self.shooting=False
    self.bullet=Bullet()

  def start_shooting(self):
    '''Ramona can shoot foam'''
    if not self.dead and not self.shooting:
      self.shootingStartCounter=0
      self.shooting=True      
      self.shootingPoseIdx=-1       

  def redraw_shooting(self):
    FPI=1
    if self.shootingStartCounter % FPI==0:
      self.shootingPoseIdx=(self.shootingStartCounter // FPI) % len(self.shootImages)

      self.image=self.shootImages[self.shootingPoseIdx]      
      self.rect=self.image.get_rect()    
      self.rect.midbottom = (self.posX,self.posY)        

      if (self.shootingStartCounter // FPI) > len(self.shootImages):
        self.shooting=False
      else:
        if (self.shootingStartCounter // FPI)==10:
          self.shootSound.play()
          #self.bullet.fly(self.posX+self.rect.width,self.posY)            
          self.bullet.start_fly(self.posX+self.rect.width,self.posY)

    #HGame.TextOut("pose:{1}, shoot counter:{0}".format(self.shootingStartCounter,self.shootingPoseIdx),
    #  (self.posX,self.posY-self.rect.height-10))    
    self.shootingStartCounter+=1    

  def hover_move(self):
    '''cause, why not?'''
    self.velocityY =self.velocityY -2*self.posY/HGame.Height

  def update(self,lkey,rkey,downkey):    
    '''
    Ramona moves, executes shoots, hovers, 
    and redraw herself in new poses/position
    also update the bullet she shot
    overrides the generic jumper update()
    '''
    self.update_immunity_counter()    

    self.bullet.update()
    if not self.dead:

      if downkey:
        self.hover_move()

      self.move(lkey,rkey)

      if self.shooting:
        self.redraw_shooting()          
      else:#regular re-draw
        self.redraw()



