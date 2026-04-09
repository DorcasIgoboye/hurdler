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
import gm_const as gm_const

class Timer(object):
  
  @property
  def count(self):
    return self._tick_count

  @property
  def period(self):
    return self._tick_period

  @property
  def iterations(self):
    return self._max_tick_count

  @property
  def id(self):
    return self._timer_id

  def __init__(self,period=1000,callback=None,end_callback=None,iterations=0,paused=False):
    self._tick_count=0
    self._max_tick_count=iterations
    self._paused=paused

    if len(gm_const.TIMERS)<gm_const.MAX_TIMERS:
      self._tick_period=period
      self._tick_callback=callback
      self._end_callback=end_callback
      self._timer_id=len(gm_const.TIMERS)
      gm_const.TIMERS.append(self)          
      if not paused: self.start()

  def start(self):
    pg.time.set_timer(gm_const.GLOBAL_TIMER_EVENT+self._timer_id, self._tick_period,loops=self._max_tick_count) 
    self.unpause()
    print("START timer {0} id:{1}, tick period {2} and {3} max iterations".format(self,self._timer_id,self._tick_period,self._max_tick_count))

  def reset(self):
    self._tick_count=0
    print("reset timer {0} id:{1}, tick period {2} and {3} max iterations".format(self,self._timer_id,self._tick_period,self._max_tick_count))

  def restart(self):
    self.reset()
    self.start()

  def pause(self):
    self._paused=True

  def unpause(self):
    self._paused=False

  def tick(self):
    if not self._paused:
      if self._tick_callback:
        self._tick_callback(self)
      self._tick_count+=1
      if self._tick_count==self._max_tick_count:
        if self._end_callback:
          self._end_callback(self)    
        self.end()

  def end(self):
    print('timer',self,self._timer_id,'ended after ',self._tick_count*self._tick_period,'msec')        
    pg.time.set_timer(gm_const.GLOBAL_TIMER_EVENT+self._timer_id, 0,loops=0)
    #gm_const.TIMERS.remove(self) - cannot remove - some may still be ticking 
    

