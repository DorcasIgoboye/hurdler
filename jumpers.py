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

from consts import *
from svp_modules.game.gmod.gm import HGame
from jumper_ramona import Ramona
from jumper_scott import Scott

class Jumpers():

  def __init__(self):
    self.LIST=[Ramona(),Scott()] #, Jumper2(), - test jumper
    self.current_index=0  #default to Ramona  
    self.Reset()

  @property
  def current(self):
    return self.LIST[self.current_index] 

  def Cycle(self):
    HGame.HideSprite(self.current)#hides current jumper

    self.current_index+=1 #increments index
    if self.current_index==len(self.LIST): #if end of list, cycles back to first
      self.current_index=0

    HGame.ShowSprite(self.current)#shows current jumper
    print('switched to Jumper ',self.current)
  
  def AllDead(self):
    dead_jumper_count=0
    while self.LIST[dead_jumper_count].dead:
      self.Cycle()            
      dead_jumper_count+=1
      if dead_jumper_count==len(self.LIST):
        return True
    return False

  def Reset(self):
    for j in self.LIST:
      j.reset()
      j.live()
      j.lives=LIVES_COUNT    

