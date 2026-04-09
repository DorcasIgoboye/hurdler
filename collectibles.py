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
from svp_modules.game.gmod.gm_timer import Timer
from svp_modules.game.gmod.gm_sprite import SimpleSprite

from consts import *
import random as rand

class Prize(SimpleSprite):
  '''collectibles prizes, etc. appear and disappear randomly can be collected for points'''
  count=0
  
  def __init__(self,time,sprite_file, appear_sound_file, collect_sound_file,color_key=RGB_WHITE):
    super().__init__()    
    self.appearSound=pygame.mixer.Sound(appear_sound_file)
    self.collectSound=pygame.mixer.Sound(collect_sound_file)    
    self.image=pygame.image.load(sprite_file)
    self.image.set_colorkey(color_key)
    self.rect = self.image.get_rect()
    self.rect.center = (rand.randint(0,HGame.Width-1),rand.randint(0,HGame.Height-1))
    self.creation_time=time
    self.displayTime = time+rand.randint(0,COLLECTIBLE_MAX_PERIOD // 10)
    print("created {0} with display time {1} seconds ".format(self,(self.displayTime-self.creation_time)/10))

  def appear(self):
    """Adds the prize to the game.AllSpritesGroup to make it show in the game
    also plays the new prize sound"""
    HGame.ShowSprite(self)
    self.appearSound.play()
    print("{0} appeared after {1} seconds".format(self,(self.displayTime-self.creation_time)/10))

  def disappear(self):
    HGame.HideSprite(self)    

  def collect(self):
    Prize.count=Prize.count+1
    self.collectSound.play()
    self.disappear()

class Vaccine(Prize):
  '''Vaccine prize class'''
  count=0

  def __init__(self,time):
    super().__init__(time,getSpriteFile("covid-19-coronavirus-vaccine_cropped64.png"),getSoundFile("cashreg.wav"),getSoundFile("175946780.mp3"))

  def collect(self):
    super().collect()
    Vaccine.count=Vaccine.count+1

class Coin(Prize):
  '''Coin prize class'''
  count=0

  def __init__(self,time):
    super().__init__(time,getSpriteFile("Bitcoin64.png"),getSoundFile("cashreg.wav"),getSoundFile("cashreg.wav"))

  def collect(self):
    super().collect()
    Coin.count=Coin.count+1

class HealthInfo(Prize):
  '''Health Informatics prize class'''
  count=0

  def __init__(self,time):
    super().__init__(time,getSpriteFile("bluebreeze_logo.png"),getSoundFile("hyperspace_activate.wav"),getSoundFile("cashreg.wav"))

  def collect(self):
    super().collect()
    HealthInfo.count=HealthInfo.count+1

class PrizeCollection(): 
  '''Maintains the list of prizes'''     
  # sprite group has all the prizes

  def __init__(self):
    super().__init__()
    self.prizeSpriteGroup = pygame.sprite.Group()

    def prize_timer_tick_callback(timer):
      for p in self.__prizes:      
        if timer.count>=p.displayTime and not self.prizeSpriteGroup.has(p):
          self.prizeSpriteGroup.add(p)#need to add this prize to the prize sprite collection so collision check will work
          p.appear()

    self.prize_timer=Timer(period=COLLECTIBLES_TIMER_TICK_PERIOD,callback=prize_timer_tick_callback)
    self.reset()    
    self.pause()


  def add(self,count=1):    
    for i in range(count):
      toss=rand.randint(0,100)      
      if 0<toss<=PRIZE_PROBABILITY_RANGES[0]:
        prize=Vaccine(self.prize_timer.count)
      elif PRIZE_PROBABILITY_RANGES[0]<toss<=PRIZE_PROBABILITY_RANGES[1]:
        prize=HealthInfo(self.prize_timer.count)        
      else:
        prize=Coin(self.prize_timer.count)
      self.__prizes.append(prize)
  
  def reset(self):
    self.prize_timer.reset()
    for prize in self.prizeSpriteGroup:
      prize.disappear()
    self.prizeSpriteGroup.empty()
    self.__prizes=[]
    self.add(PRIZE_COUNT)


  def reset_counts(self):
    Coin.count=0
    Vaccine.count=0
  
  def check_collisions_with(self,obj):        
    prizes_hits = pygame.sprite.spritecollide(obj, self.prizeSpriteGroup, True)#True means that after collision, prize object disappears
    for prize in prizes_hits:
      prize.collect()      
      self.prizeSpriteGroup.remove(prize)      
      self.__prizes.remove(prize)#remove the collected prize from the prize list
      self.add()#add a new thing to the collection 
    
  def pause(self):
    self.prize_timer.pause()

  def unpause(self):
    self.prize_timer.unpause()
  
  def update(self):
    HGame.TextOut("Coins:{0}, Vacc's:{1}".format(Coin.count,Vaccine.count),(HGame.Width-220,0),RGB_GREEN)    





  

