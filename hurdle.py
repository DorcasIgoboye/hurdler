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

VIRUS_SPRITES = [
    {"name": "Worm", "location": (0, 314), "dimension": (256, 300)},
    {"name": "Virus", "location": (256, 314), "dimension": (256, 300)},
    {"name": "Macro Virus", "location": (512, 314), "dimension": (256, 300)},
    {"name": "Polymorphic Virus", "location": (768, 314), "dimension": (256, 300)}
]

class Hurdle(SimpleSprite):
  '''The hurdle is just a rectangle, but it could be any sprite
  collision with rectangle objects is dead easy, built-into pygame'''

  def __init__(self):
    super().__init__()

    #create a sprite group for hurdle
    #this is necessary to get access to the built-in sprite collision function spritecollide
    self.spriteGroup = pygame.sprite.Group()
    self.spriteGroup.add(self)
    self.base_velocity = HURDLE_VELOCITY
    self.speed = self.base_velocity  
    self.start_time = pygame.time.get_ticks()
    self.sm=SpriteMap(getSpriteFile('viruses_resized.png'))
    self.image_list=self.sm.load_many(VIRUS_SPRITES,color_key=RGB_WHITE)

    # Scale virus sprites to 25% size (adjust as needed)
    scaled_list = []
    for img in self.image_list:
      new_w = img.get_width() // 4 
      new_h = img.get_height() // 4  
      scaled = pygame.transform.scale(img, (new_w, new_h))
      scaled_list.append(scaled)

    self.image_list = scaled_list


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

    if HGame.Difficulty == 'easy':
      diff = 0.7
    elif HGame.Difficulty == 'hard':
      diff = 1.5
    else:
      diff = 1.0

    self.spawn_time = pygame.time.get_ticks()
    self.active = False
    self.speed = self.base_velocity
    self.mutate()

    spawn_type = rand.choice(["LEFT", "RIGHT"])
    SAFE_DISTANCE = 10 

    if spawn_type == "LEFT":
      self.posX = -self.rect.width - SAFE_DISTANCE
      self.posY = rand.randint(self.rect.height, HGame.Height - 100)
      self.velocityX = self.speed
      self.velocityY = 0

    elif spawn_type == "RIGHT":
      self.posX = HGame.Width + SAFE_DISTANCE
      self.posY = rand.randint(self.rect.height, HGame.Height - 100)
      self.velocityX = -self.speed
      self.velocityY = 0

    self.direction = 1 if self.velocityX > 0 else -1

  def redraw(self):
    if self.posX < -self.rect.width // 2:      
      self.reset()
    self.rect.x = self.posX
    self.rect.y = self.posY

  
  def move(self):
    self.posX += self.velocityX
    self.posY += self.velocityY

    if (
        self.posX < -self.rect.width or
        self.posX > HGame.Width + self.rect.width or
        self.posY > HGame.Height + self.rect.height
    ):
        self.reset()

  def die(self):
    self.dead=True
    #dramatic explosion?
    self.reset()

  def _get_difficulty_multiplier(self):
    if HGame.Difficulty == 'easy':
      return 0.7
    elif HGame.Difficulty == 'hard':
      return 1.5
    return 1.0

  def set_difficulty(self, mult):
    self.speed = self.base_velocity * mult

    
  def update(self):
    if not self.active:
        if pygame.time.get_ticks() - self.spawn_time > 800:
            self.active = True
        else:
            return

    if not self.dead:
        time_alive = (pygame.time.get_ticks() - self.start_time) / 1000
        time_factor = 1 + time_alive * 0.0005
        self.velocityX = self.direction * self.speed * time_factor

    self.move()
    self.redraw()