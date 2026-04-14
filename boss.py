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

BOSS_SPRITES = [
    {"name": "attack", "location": (0, 0), "dimension": (256, 300)},
    {"name": "launch", "location": (256, 0), "dimension": (256, 300)},
    {"name": "move", "location": (512, 0), "dimension": (256, 300)},
    {"name": "hit", "location": (768, 0), "dimension": (256, 300)},
    {"name": "conquer", "location": (0, 314), "dimension": (256, 300)},
    {"name": "lose", "location": (256, 314), "dimension": (256, 300)}
]

class Boss(SimpleSprite):
  '''The Boss is a rectangle shape, but it could be any sprite
  collision with rectangle objects is dead easy, built-into pygame'''

  def __init__(self):
    super().__init__()

    # boss attack
    self.bullet = None
    self.shootCooldown = 0
    self.attackSound = pygame.mixer.Sound(getSoundFile(BOSS_ATTACK_SOUND))

    #create a sprite group for Boss
    #this is necessary to get access to the built-in sprite collision function spritecollide
    self.spriteGroup = pygame.sprite.Group()
    self.spriteGroup.add(self)

    self.sm=SpriteMap(getSpriteFile('active_trojan.jpg'))
    self.image_list=self.sm.load_many(BOSS_SPRITES,color_key=RGB_WHITE)

    self.dead=False
    self.reset()

  def check_collisions_with(self,obj):     
    boss_hits = pygame.sprite.spritecollide(obj, self.spriteGroup, False)
    if boss_hits:
      # when colliding with other object, stop the jumper X movement, exacly at the X position where it got hit
      # also make them dead
      obj.velocityX = 0.0
      obj.posX = boss_hits[0].rect.left #there is only one boss in this group, hence boss_hits[0] will always work      
      obj.die()#always, deadly collision! :( - reconsider? health? stamina?, damage model?, broken bones? healthcare healing prizes?
  
  def shoot(self):
    if self.bullet is None or not self.bullet.flying:
        from bullet import Bullet
        self.bullet = Bullet()
        self.bullet.start_fly(self.posX, self.posY)
        self.bullet.velocityX = -10  # shoot LEFT toward player
        self.attackSound.play()

  def mutate(self):
    image_index=rand.randint(0,len(self.image_list)-1)
    self.image=self.image_list[image_index]
    self.rect = self.image.get_rect()    
    self.posY=rand.randint(self.rect.height,HGame.Height)    
    self.rect.midbottom = (0,self.posY)
    
  def reset(self):
    '''resets the position to the right side of the screen and, velocity to BOSS_VELOCITY'''
    self.mutate()
    self.velocityX=2.0#BOSS_VELOCITY
    self.velocityY=2.0#BOSS_VELOCITY
    self.accelX=0
    self.accelY=0
    self.dead=False
    self.posX =- self.rect.width
    self.posY =rand.randint(self.rect.height,HGame.Height) 

    

  def redraw(self):
    if self.posX > HGame.Width+ self.rect.width:
      self.reset()
    self.rect.x = self.posX   
    if self.posY > HGame.Height+self.rect.height:    
      self.reset()
    self.rect.y = self.posY

  def move(self):
    '''Boss moves, or is it the Jumper that runs? Whatever your point of view,
    for now, X accelleration is zero, but one can imagine a boss slowing down or speeding up for various reasons'''
    self.accelX = 0#ACCELERATION_CONST
    max_x_change = self.velocityX + MOVE_TIME_CONST * self.accelX
    self.posX += rand.randint(int(-max_x_change),int(+5*max_x_change))/5
    if self.posX > HGame.Width+self.rect.width:
      self.posX = - self.rect.width #wrap around
    #random move in Y direction
    self.accelY = rand.randint(1,50)/10#ACCELERATION_CONST
    max_y_change = self.velocityY + MOVE_TIME_CONST * self.accelY
    self.posY += rand.randint(-int(max_y_change),+int(5*max_y_change))/5
    if self.posY > HGame.Height+self.rect.height:
      self.posY = - self.rect.height #wrap around      

  def die(self):
    self.dead=True
    #dramatic explosion?
    self.reset()

  def update(self):
    if not self.dead:
        self.move()
        self.redraw()

        # shooting logic
        self.shootCooldown += 1
        if self.shootCooldown > 120:  # every ~2 seconds
            self.shoot()
            self.shootCooldown = 0

        if self.bullet:
            self.bullet.update()

