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
# S. V. Pantazi (svpantazi@gmail.com), Jan-Apr 2021
# work in progress (WIP)

import config
from svp_modules.game.gmod.gm import HGame
from svp_modules.game.gmod.gm_const import *
from svp_modules.game.gmod.gm_timer import Timer

import pygame as pygame
from pygame.locals import *
import random as rand

from consts import *
from floor import Platform
from higher_platform import LittlePlatform
from jumpers import Jumpers
from hurdle import Hurdle
from collectibles import PrizeCollection
from timer_countdown import begin_countdown, game_countdown_display
from timer_gameover import gameover_display
from menu import make_menu
from boss import Boss

HGame.Init(caption=GAME_CAPTION,mode=(1000,480))
HGame.ShakeTimer = 1
HGame.ShakeIntensity = 1
HGame.FPS=60
HGame.BGMoveSpeed=1
#game setup
#create game objects
platform=Platform()
higher_platform=LittlePlatform()
hurdle=Hurdle()
prizes=PrizeCollection()


jumpers=Jumpers()
boss=Boss()

HGame.ShowSprites([platform,higher_platform,hurdle,jumpers.current,boss])

def reset_game():
  ''' Resets all game objects to the initial state, ready to begin
  In this state, jumper(s) live and can be moved around
  Jumpers do colide with the floor/platform (otherwise they will go through the floor)
  however, colisions with hurdles and prizes are disabled  '''
  #load background image
  HGame.BGImgLoad(BACKGROUND_IMAGE_FILE)
  #clear parallax image list
  HGame.BGParallaxImages.clear()
  #adds one parallax image
  HGame.BGParallaxImgAdd(PARALAX_BACKGROUND_IMAGE_FILE,(254,254,254),2)
  #load background music
  HGame.Music=False #first turn off existing music
  HGame.BGMusicLoad(BACKGROUND_MUSIC_FILE)
  HGame.Music=DEFAULT_BACKGROUND_MUSIC_ON #then put it back on
  HGame.MusicVol=0.6 #default background music volume  

  prizes.reset()
  hurdle.reset()
  boss.reset()

  #boolean flags to drive the game lifecycle logic
  HGame.Ready=True
  HGame.Countdown=False
  HGame.Playing=False
  HGame.Over=False

  HGame.BGImage.set_alpha(50) #transparent background
  
  jumpers.Reset()  
  prizes.reset_counts()

  #jumper position can be offset in the X direction
  jumpers.current.live(XPosOffset=-50)

  #jumpers.current.immune=True  #good for testing

  HGame.Menu.enable()

def start_countdown():
  # Do the job here !
  HGame.Menu.disable()
  HGame.Ready=False
  HGame.Countdown=True
  begin_countdown()

def begin_play():
  '''Game is on! Sets the HGame.GameOver to False and unpauses the Prizes timer so that they appear on screen'''  
  HGame.Countdown=False  
  HGame.Playing=True
  prizes.unpause()
  HGame.BGImage.set_alpha(255) #complete opacity 

def end_game():
  '''Game ended, dramatic background and sad music start. 
  Prizes timer is paused so that they stop appearing. 
  The endGameTimer is triggered so that after a short while the game is reset to the ready state'''
  HGame.Playing=False
  HGame.Over=True
  prizes.pause()
  HGame.BGMoveSpeed=0
  HGame.BGParallaxImages.clear()
  gameover_display()
     
def process_events(e):
  '''checks for key presses and other less frequent events such as timers, etc.'''
  if e.type == pygame.KEYDOWN:
    if e.key == pygame.K_F1:
      pass #what can F1 key be used for?
    elif e.key==PAUSE_TOGGLE_KEY:
      HGame.Paused=not HGame.Paused
    elif e.key == MUSIC_TOGGLE_KEY:
      HGame.Music=not HGame.Music
    elif e.key == pygame.K_RETURN:
      if HGame.Ready:
        start_countdown()
    elif e.key == pygame.K_UP:
        jumpers.current.jump(platform)
    elif e.key == pygame.K_DELETE:
        if jumpers.current.can("start_shooting"):
        #if jumper.__class__==Jumper:
          jumpers.current.start_shooting()
    #elif e.key == pygame.K_w:
    #    jumper2.jump(platform)      
    elif e.key == pygame.K_F4:      
      jumpers.Cycle()

def check_platform_collisions():     
  '''Platform/floor collisions are separate because they are essential in both phases of the game (ready and during play)
  or else jumpers with go through the floor forever, due to the physics of gravity!'''
  platform.check_collisions_with(jumpers.current)   
  higher_platform.check_collisions_with(jumpers.current)         

def check_prize_and_hurdle_collisions():     
  '''Prizes and hurdle collisions are enabled only in the play phase of the game, when the game is on!
  Clearly, the current jumper is not immune to collecting prizes :)'''
  prizes.check_collisions_with(jumpers.current)
  #immunity! collect a prize, get immunity! should not be too difficult to implement
  if not jumpers.current.immune:
    if not jumpers.current.dead:
      hurdle.check_collisions_with(jumpers.current)

def game_update(keys=None):
  '''Game update callback gets called by pygame framework FPS-times a second.
  All drawing/display updates as well as collision checks belong here;
  Keypress info is also available here in order to allow for fast physics update: moves, hover, etc'''
  
  if keys is None:
    keys = pygame.key.get_pressed()
  
  #Note how collisions with platform/floor are updated at all times, 
  # regardless of dead/alive status, or whether the game has not started
  check_platform_collisions()

  #hurdles are moving at all times - for dramatic effect during ready phase of the game
  # collisions with them are enabled only during the game on phase
  hurdle.update()
  boss.update()

  if jumpers.current.has('bullet'):
    jumpers.current.bullet.check_collisions_with(hurdle)
  #jumpers are updated and moved at all times unless dead
  #the moving logic was moved into the Jumper class
  #here the update method is called with the boolean values
  #for the keys associated with the movement directions
  jumpers.current.update(keys[K_LEFT],keys[K_RIGHT],keys[K_DOWN])  


if HGame.ShakeTimer > 0:
    offset_x = rand.randint(-HGame.ShakeIntensity, HGame.ShakeIntensity)
    offset_y = rand.randint(-HGame.ShakeIntensity, HGame.ShakeIntensity)

    jumpers.current.rect.x += offset_x
    jumpers.current.rect.y += offset_y

    HGame.ShakeTimer -= 1
    HGame.ShakeIntensity *= 0.8
    
      #prizes are visible at all times
def game_update(keys=None):

  if keys is None:
    keys = pygame.key.get_pressed()

  # platform collisions
  check_platform_collisions()

  # update enemies
  hurdle.update()
  boss.update()

  # bullet collisions
  if jumpers.current.has('bullet'):
    jumpers.current.bullet.check_collisions_with(hurdle)

  # player movement
  jumpers.current.update(keys[K_LEFT], keys[K_RIGHT], keys[K_DOWN])

  if HGame.ShakeTimer > 0:
    offset_x = rand.randint(-HGame.ShakeIntensity, HGame.ShakeIntensity)
    offset_y = rand.randint(-HGame.ShakeIntensity, HGame.ShakeIntensity)
    HGame.ShakeTimer -= 1

    jumpers.current.rect.x += offset_x
    jumpers.current.rect.y += offset_y

  # prizes
  prizes.update()

  # game state logic
  if HGame.Ready:
    pass

  elif HGame.Countdown:
    game_countdown_display()

  elif HGame.Playing:
    check_prize_and_hurdle_collisions()

    if jumpers.current.dead:
      if jumpers.current.lives > 0:
        jumpers.current.live()
      else:
        if jumpers.AllDead():
          end_game()

  elif HGame.Over:
    pass

make_menu(start_countdown)

def main():
  '''Entry point into the game'''
  #the HGame object is shared across all parts of the game
  #adding pointers to the reset_game(), begin_game() and end_game() functions allows easy access to these calls 
  #from other parts of the code (e.g., the countdown timer code)

  HGame.Reset=reset_game
  HGame.Countdown=begin_countdown
  HGame.Begin=begin_play
  HGame.End=end_game
  
  HGame.Reset()
  HGame.Run(event_callback=process_events,update_callback=game_update)
  HGame.Done()

if __name__ == '__main__':
    main()