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
from svp_modules.game.gmod.gm_sprite import SimpleSprite
from svp_modules.game.gmod.gm_spritemap import SpriteMap

from consts import *

from bullet import Bullet

class Jumper(SimpleSprite):
  """Sprite for main jumper character"""
  
  def __init__(self,sprite_map,color_key=None):
    '''Jumper construction, now since we have separated the jumper from the game
    the game object must be available for referencing, so we pass it along in the init, 
    as a parameter, every time we construct the Jumper'''
    super().__init__()    

    #setting Jumper sounds
    self.jumpSound=pygame.mixer.Sound(getSoundFile("jump.wav"))
    self.failSound=pygame.mixer.Sound(getSoundFile("fail.wav"))
    
    #setting Jumper sprites
    #first create a SpriteMap object
    self.smap=SpriteMap(getSpriteFile(sprite_map['file']))

    #then use the load many method to load the sprites in the image list
    #the color key is the special color that allows for transparency in the sprites images
    self._Rimages=self.smap.load_many(sprite_map['left_right_move_sprites'],color_key=color_key)

    #for the left direction images can be horizonally flipped
    #so no need for additional set of sprites - one direction is sufficient
    self._Limages=[]
    for image in self._Rimages:             
      flipped_image=pygame.transform.flip(image,True,False)
      self._Limages.append(flipped_image)

    self.deadSpriteImage=self.smap.load_one(sprite_map['dead_sprite'],color_key=color_key)
    
  def reset(self):
    self.lives=LIVES_COUNT

  def live(self,XPosOffset=0):
    '''Jumper lives, i.e., has position and is NOT dead;
    for now, just one life, but there could be 9 of them, just like cats'''
    self.image=self._Rimages[IDLE_POSE_INDEX] #neutral pose index    
    self.rect=self.image.get_rect() #the bounding box around the character    
    self.posX=HGame.Width//2-self.rect.width//2+XPosOffset
    self.posY=HGame.Height//2-self.rect.height//2
    self.velocityX=0
    self.velocityY=0
    self.accelX=0
    self.accelY=0    
    self.dead=False
    #HGame.BGImgLoad(BACKGROUND_IMAGE_FILE)    
    self.immune=True
    self.immunity_counter=0
    
  def move(self,lkey,rkey):
    '''Jumper moves, has velocities and accelerations in X and Y directions,
    changes position according to the laws of physics, as we define them in the game'''
    self.accelX=0.0 #if no left-right key pressed, X axis acceleration is 0.0
    self.accelY=ACCELERATION_CONST #gravity is still on though, regardless

    if lkey:
      self.accelX = -ACCELERATION_CONST
    if rkey:
      self.accelX = ACCELERATION_CONST

    self.accelX += self.velocityX * FRICTION_COEF
    self.velocityX += self.accelX
    self.velocityY += self.accelY
    self.posX += self.velocityX + MOVE_TIME_CONST * self.accelX
    self.posY += self.velocityY + MOVE_TIME_CONST * self.accelY 

  def redraw(self):
    if abs(self.velocityX)>=1:
      poseIdx=int(self.posX/STRIDE_SIZE)#stride pose
    else:
      poseIdx=IDLE_POSE_INDEX#idle pose
    
    #pose index must be limited to the length of the image list
    poseIdx=poseIdx % len(self._Rimages)
    #some debug text out to see dynamic values of Y velocity and pose   
    #HGame.TextOut("velX {0:.2f}, velY:{1:.2f},pose:{2}".format(self.velocityX, self.velocityY,poseIdx),
    #  (self.posX,self.posY-self.rect.height-10))    
    if self.immune:
      HGame.TextOut("IMM",(self.posX,self.posY-self.rect.height-10),color=RGB_GREEN) 
        
    
    if self.velocityX>=0:
      self.image=self._Rimages[poseIdx]
    else:
      self.image=self._Limages[poseIdx]    
    
    if self.posX+self.rect.width//2 > HGame.Width:
      self.posX = HGame.Width-self.rect.width//2 
    if self.posX < self.rect.width//2:
      self.posX = self.rect.width//2

    #updating rectangle
    self.rect=self.image.get_rect()
    self.rect.midbottom = (self.posX,self.posY)
    
    #update lives display
    HGame.TextOut("Lives:{0}".format(self.lives),(HGame.Width-350,0))    


  def jump(self,platform):
    '''Jumper can jump only when their feet touch the floor/platform by changing their velocity (KICK) in the Y direction;
    jump also ends when colliding with the floor/platform, just like in real world'''
    if not self.dead:
      hits_platform = pygame.sprite.spritecollide(self, platform.spriteGroup, False)
      if hits_platform:
        self.velocityY = JUMP_VELOCITY_KICK
        self.jumpSound.play()
  
  def die(self):
    '''Jumper dies, i.e., for now, just one life,
     but there could be 9 of them, just like cats'''
    print("dead!")
    self.dead=True
    self.failSound.play()
    #when dead set image to a special dead sprite image
    self.image=self.deadSpriteImage
    self.rect=self.image.get_rect()
    self.rect.midbottom = (self.posX,self.posY+20)    #adjustment of Y axis position of the dead body :(  
    self.lives+=-1

  def update_immunity_counter(self):
    self.immunity_counter+=1
    if self.immunity_counter>=HGame.FPS*3:
      self.immune=False  

  def update(self,lkey,rkey,downkey):    
    '''Jumper moves, executes actions (shooting, etc.)
        and redraws itself in new poses/position    
    ''' 
    self.update_immunity_counter()
    if not self.dead:
      self.move(lkey,rkey)
      self.redraw()      
    

    

