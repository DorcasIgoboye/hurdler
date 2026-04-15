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

  def __init__(self, players, level):
    super().__init__()

    # boss objects
    self.state = "idle"
    self.active = False
    self.velocityX = 2        # default speed
    self.bullet = None
    self.shootCooldown = 0
    self.shootDelay = 120     # default shooting delay
    self.players = players
    self.attackSound = pygame.mixer.Sound(getSoundFile(BOSS_ATTACK_SOUND))

    # boss adjusts movement speed and shooting frequency based on level
    if level >= 2:
            self.shootDelay = 90

    if level >= 3:
            self.velocityX = 3

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
    '''Shoots at the closest player'''
    from bullet import Bullet
    target = player = min(self.players, key=lambda p: abs(p.posX - self.posX))


    self.bullet = Bullet()
    self.bullet.start_fly(self.posX, self.posY)

    direction = 1 if target.posX > self.posX else -1
    self.bullet.velocityX = 8 * direction

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
    '''Boss becomes activated when the player moves close enough'''
    # Attack the closest player
    player = player = min(self.players, key=lambda p: abs(p.posX - self.posX))

    if self.state == "idle":
        if abs(player.posX - self.posX) < 300:
            self.state = "attack"

    elif self.state == "attack":
        if self.posX < player.posX:
            self.posX += self.velocityX
        else:
            self.posX -= self.velocityX      

  def die(self):
    self.dead=True
    self.reset()

  def update(self):
    if not self.active:
        return  # boss does nothing until activated

    if not self.dead:
        self.move()
        self.redraw()

        # shooting logic
        self.shootCooldown += 1
        if self.shootCooldown > self.shootDelay:
            self.shoot()
            self.shootCooldown = 0

        if self.bullet:
            self.bullet.update()
