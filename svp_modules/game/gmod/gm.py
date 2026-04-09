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

S. V. Pantazi (svpantazi@gmail.com), 2021
OOP PyGame module wrapper
this module is meant to simplify the development of a simple game by abstracting/hiding some of the technicalities 
of the pygame framework
It is work in progress (WIP)
Development based on these resources:
https://www.pygame.org/docs/index.html
https://www.pygame.org/docs/tut/MakeGames.html
'''

import os
import pygame as pg
import random as rand
from pygame.locals import *
import gm_const# as gm_const
from gm_helper import *
#import gm_timer
from gm_timer import Timer
import pygame_menu #https://pygame-menu.readthedocs.io/en/4.0.2/


def is_global_timer_event(event_type):
  return (event_type-gm_const.GLOBAL_TIMER_EVENT) in range(0,len(gm_const.TIMERS))

def get_global_timer(event_type):   
  for t in gm_const.TIMERS:
    if t._timer_id==(event_type-gm_const.GLOBAL_TIMER_EVENT):
      return t

#note IMPORTANT: properties work only in objects (instances) not in classes
#so the basic game needs be an object, i.e., class instance
class BasicGame(object):

  @property
  def Paused(self):
    return self.__paused

  @Paused.setter
  def Paused(self,val):
    print("paused",val)
    if self.__paused!=val:
      self.__paused=val

  @property
  def Font(self):
    return self.font

  @Font.setter
  def Font(self,val):
    if self.font!=val:
      self.font=val

  @property
  def Menu(self):
    return self.__menu

  @Menu.setter
  def Menu(self,val):
    if self.__menu!=val:
      self.__menu=val

  @property
  def Canvas(self):
    return self.__canvas

  @property
  def Width(self):
    return self.__canvasSize[0]

  @property
  def Height(self):
    return self.__canvasSize[1]

  @property
  def MidX(self):
    return self.__canvasSize[0]//2

  @property
  def MidY(self):
    return self.__canvasSize[1]//2

  @property
  def PlayTime(self):
    return self.__playTime
  
  @property
  def BGMoveSpeed(self):    
    return self.__BGMoveSpeed

  @BGMoveSpeed.setter
  def BGMoveSpeed(self,speed):
    self.__BGMoveSpeed=speed
    
  @property
  def MusicVol(self):    
    return pg.mixer_music.get_volume()

  @MusicVol.setter
  def MusicVol(self,vol):
    print("setting background music volume to ",vol)
    pg.mixer_music.set_volume(vol)

  @property
  def Music(self):
    return self.__musicOn

  @Music.setter
  def Music(self,val):
    print("setting background music")
    if not val==self.__musicOn:
      self.__musicOn=val
      if self.__musicOn:
        print("Music on")
        pg.mixer_music.set_endevent(gm_const.MUSIC_END_EVENT)
        pg.mixer_music.play(-1)#-1 is looping forever
      else:
        print("Music off")
        pg.mixer_music.set_endevent()
        pg.mixer_music.stop()

  def BGMusicLoad(self, bgMusicFile):
    pg.mixer_music.unload()
    pg.mixer_music.load(getAssetFile(gm_const.ASSET_PATH_MUSIC,bgMusicFile))    

  __FPS=gm_const.DEFAULT_FPS
  @property
  def FPS(self):
    return self.__FPS

  @FPS.setter
  def FPS(self, fps):
      if fps < 1:
          self.__FPS = 1
      elif fps > 1000:
          self.__FPS = 1000
      else:
          self.__FPS = fps

  @property
  def BGImage(self):
    return self.__BGimage

  @BGImage.setter
  def BGImage(self, bgImageSurface):
    __convertedImgSurface=bgImageSurface.convert(self.__BGimage)
    pg.transform.scale(__convertedImgSurface, BasicGame.__canvasSize, self.__BGimage)

  def BGImgLoad(self, bgImageFile):
    __imageSurface=pg.image.load(getImageFile(bgImageFile))
    self.BGImage=__imageSurface

  @property
  def BGParallaxImages(self):
    return self.__BGParallaxImages
  
  def BGParallaxImgAdd(self, parallaxImageFile,color_key,scrollSpeed):
    __imageSurface=pg.image.load(getImageFile(parallaxImageFile))
    __convertedImgSurface=pg.Surface(BasicGame.__canvasSize).convert(__imageSurface)
    pg.transform.scale(__imageSurface, BasicGame.__canvasSize, __convertedImgSurface)    
    __convertedImgSurface.set_colorkey(color_key)    
    self.__BGParallaxImages.append({"img_surface":__convertedImgSurface,"scroll_speed":scrollSpeed, "position":0})

  def TextOut(self,txt="",pos=(0,0),color=gm_const.RGB_BLACK):
    text_surface = self.font.render(txt, True, color)
    text_surface = text_surface.convert_alpha() #is this really needed?
    #return text
    self.__canvas.blit(text_surface,pos)
    #to draw text in the middle of a window
    #text_w,text_h = self.font.size(txt) 
    #self.__canvas.blit(text_surface, ((self.__canvasSize[0] - text_w) // 2, (self.__canvasSize[1] - text_h) // 2))
 
  
  def TextOutMiddle(self,txt="",color=gm_const.RGB_BLACK):
    #to draw text in the middle of a window
    text_w,text_h = self.font.size(txt) 
    middle_pos=(self.MidX - text_w // 2, self.MidY - text_h // 2)
    self.TextOut(txt,middle_pos,color)
  
  def ShowSprite(self,sprite):
    BasicGame.__sprites.add(sprite)
    
  
  def ShowSprites(self,sprite_list):
    for s in sprite_list:
      BasicGame.__sprites.add(s)
  
  def HideSprite(self,sprite):
    BasicGame.__sprites.remove(sprite)

  def HideSprites(self,sprite_list):
    for s in sprite_list:
      BasicGame.__sprites.remove(s)


  def __init__(self):
    super().__init__()
    #initialize pygame framework
    pg.init()
    #initialize sound mixer and load background music
    pg.mixer.init(buffer=2048) #preinitialize sound buffer

    #create the all sprite group of sprites
    BasicGame.__sprites = pg.sprite.Group()

    self.__BGImage=None
    self.__menu = None

  def Init(self,caption="",mode=gm_const.DEFAULT_GAME_WINDOW_SIZE):

    #set caption
    pg.display.set_caption(caption)
      
    #fps clock construction
    self.__fpsClock=pg.time.Clock()

    #initialize canvas/drawing surface
    self.__canvas = pg.display.set_mode(mode,pg.DOUBLEBUF)
    self.__canvas.fill(gm_const.RGB_WHITE) 

    #set canvas size - as an internal class property
    BasicGame.__canvasSize=self.__canvas.get_size()
    #set font
    self.font = pg.font.SysFont('mono', 20, bold=True)

    #initialize background image drawing surface
    self.__BGimage = pg.Surface(BasicGame.__canvasSize).convert()
    self.__BGParallaxImages=[]

    self.__paused=False
    self.__musicOn=False
    self.__backgroundPosition=0
    self.__BGMoveSpeed=0
    

  def EventUpdate(self):  
    event_list=pg.event.get()
    if self.__menu and self.__menu.is_enabled():
          self.__menu.update(event_list)

    for e in event_list:      
      if self.__EventCallback:
        #all events will be passed on to user if not paused
        if not self.__paused: self.__EventCallback(e)        
        else:
          #when game is paused, there some exception key callbacks 
          if e.type == pg.KEYDOWN and e.key in [gm_const.MUSIC_TOGGLE_KEY,gm_const.PAUSE_TOGGLE_KEY]:
            self.__EventCallback(e)
      #default processing of events
      if e.type==QUIT:
        self.__looping = False # loop will end, pygame window will close
      elif e.type == pg.KEYDOWN:
          if e.key == pg.K_ESCAPE:
            self.__looping = False      
      elif e.type==gm_const.MUSIC_END_EVENT:
        print("Happy song loop")
        #pg.mixer_music.rewind()
        #pg.mixer_music.play()
      elif is_global_timer_event(e.type):        
        timer=get_global_timer(e.type)
        timer.tick()


  def DrawUpdate(self):  
    self.__playTime+=self.__fpsClock.tick(self.__FPS)/1000.0
      
    self.__canvas.fill(gm_const.RGB_WHITE)
        
    #BasicGame.__sprites.clear(self.__canvas, self.__BGimage)

    
    #draw background, there must be one - now it can move
    self.__canvas.blit(self.__BGimage.subsurface(self.__backgroundPosition, 0,self.__BGimage.get_width()-self.__backgroundPosition,self.__BGimage.get_height()),(0,0))
    self.__canvas.blit(self.__BGimage.subsurface(0,0,self.__backgroundPosition,self.__BGimage.get_height()), (self.__BGimage.get_width()-self.__backgroundPosition,0)) 
    #
    #draw backround parallax images
    for ir in self.__BGParallaxImages:
      self.__canvas.blit(ir["img_surface"].subsurface(
        ir["position"], 0, ir["img_surface"].get_width()-ir["position"],ir["img_surface"].get_height()),
        (0,0))
      self.__canvas.blit(ir["img_surface"].subsurface(
        0, 0, ir["position"],ir["img_surface"].get_height()),
        (ir["img_surface"].get_width()-ir["position"],0))       

      
    
    #if FPS_DISPLAY_ON    
    text = "FPS:{0:.1f} Music:{1}".format(self.__fpsClock.get_fps(),['Off','On'][self.__musicOn])
    self.TextOut(text,(0,0),gm_const.RGB_RED)

    if self.__paused:
      self.TextOutMiddle('PAUSED',color=gm_const.RGB_RED)

    #update callback only if game is not paused
    if self.__UpdateCallback and not self.__paused: 
      #pressed keys data passed on to user in the graphics update as well for fast moves
      self.__UpdateCallback(pg.key.get_pressed())

    BasicGame.__sprites.draw(self.__canvas)

    if self.__menu and self.__menu.is_enabled():
          self.__menu.draw(self.__canvas)

    pg.display.flip()
    #pg.display.update()

    #moving background hack!
    self.__backgroundPosition+=self.__BGMoveSpeed
    if self.__backgroundPosition>self.__BGimage.get_width():
      self.__backgroundPosition=0

    for ir in self.__BGParallaxImages:
      ir['position']+=ir['scroll_speed']
      if ir['position']>ir["img_surface"].get_width():
        ir['position']=0

  def Run(self,event_callback=None,update_callback=None):
    self.__playTime=0.0
    self.__looping=True
    self.__EventCallback=event_callback
    self.__UpdateCallback=update_callback
    while self.__looping:
      self.EventUpdate()
      self.DrawUpdate()
    
  def Done(self):
    print("Game finished after {0:.2f} seconds".format(self.__playTime))
    pg.mixer_music.stop()
    pg.quit()


#global basic game object refered to as BG throughout
HGame=BasicGame()
rand.seed()

if __name__ == '__main__':
  HGame.Init(caption=gm_const.DEFAULT_PYGAME_WINDOW_CAPTION)
  HGame.Run()
  HGame.Done()


