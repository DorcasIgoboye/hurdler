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

from consts import *
from floor import Platform
from jumpers import Jumpers
from hurdle import Hurdle
from collectibles import PrizeCollection
from timer_countdown import begin_countdown, game_countdown_display
from timer_gameover import gameover_display
from menu import make_menu
from boss import Boss
from jumper_ramona import Ramona
from jumper_scott import Scott
from core import DataCore
from game_state import State
from narrative import Narrative

HGame.Init(caption=GAME_CAPTION,mode=(1000,480))
HGame.FPS=60
HGame.BGMoveSpeed=1
#game setup
#create game objects
platform=Platform()
core = DataCore()
hurdle = Hurdle(core)

prizes=PrizeCollection()

player1 = Ramona(player_id=1)
player2 = Scott(player_id=2)
jumpers = [player1, player2]
players = jumpers

boss = Boss(players, State.level)
narrative = Narrative()

HGame.ShowSprites([platform, hurdle, player1, player2, boss])

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
  
  for player in jumpers:
    player.reset()
    player.live()

  #jumper position can be offset in the X direction
  player1.live(XPosOffset=-50)
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
  if State.level >= 2:
      boss.active = True # boss active
  else:
      boss.active = False

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
  narrative.game_lost()
     
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
      
      # Player 2 jump key
      if e.key == pygame.K_UP:
         player2.jump(platform)

      # Player 1 jump key
      if e.key == pygame.K_SPACE:
          player1.jump(platform)

def check_platform_collisions():     
  '''Platform/floor collisions are separate because they are essential in both phases of the game (ready and during play)
  or else jumpers with go through the floor forever, due to the physics of gravity!'''
  for player in jumpers:
    platform.check_collisions_with(player)
        

def check_prize_and_hurdle_collisions():     
  '''Prizes and hurdle collisions are enabled only in the play phase of the game, when the game is on!
  Clearly, the current jumper is not immune to collecting prizes :)'''
  for player in jumpers:
    prizes.check_collisions_with(player)
    if not player.immune and not player.dead:
        hurdle.check_collisions_with(player)


def game_update(keys):
  '''Game update callback gets called by pygame framework FPS-times a second.
  All drawing/display updates as well as collision checks belong here;
  Keypress info is also available here in order to allow for fast physics update: moves, hover, etc'''
  
  #Note how collisions with platform/floor are updated at all times, 
  # regardless of dead/alive status, or whether the game has not started
  check_platform_collisions()

  #hurdles are moving at all times - for dramatic effect during ready phase of the game
  # collisions with them are enabled only during the game on phase
  hurdle.update()
  boss.update()
  narrative.update()
  narrative.draw(HGame)

  for player in jumpers:
    if player.has('bullet'):
        player.bullet.check_collisions_with(hurdle)

  # --- BOSS BULLET COLLISION CHECK ---
  if boss.bullet:
    for player in jumpers:
      boss.bullet.check_collisions_with(player)

  #jumpers are updated and moved at all times unless dead
  #the moving logic was moved into the Jumper class
  #here the update method is called with the boolean values
  #for the keys associated with the movement directions
  for player in jumpers:
    if player.player_id == 1:
        l = keys[K_a]
        r = keys[K_d]
        down = keys[K_s]
        jump = keys[K_SPACE]
        shoot = keys[K_f]

    elif player.player_id == 2:
        l = keys[K_LEFT]
        r = keys[K_RIGHT]
        down = keys[K_DOWN]
        jump = keys[K_UP]
        shoot = keys[K_RCTRL]

    # movement
    player.update(l, r, down)

    # jumping
    if jump:
        player.jump(platform)

    # shooting
    if shoot and player.can("start_shooting"):
        player.start_shooting()
  

  #prizes are visible at all times
  prizes.update()   

  if HGame.Ready:
    pass

  elif HGame.Countdown:
    game_countdown_display()

  elif HGame.Playing:
    # Increase difficulty
    boss.velocityX += 0.001
    hurdle.velocityX += 0.001

    #prize and hurdle collisions only during game on phase
    check_prize_and_hurdle_collisions()
    all_dead = True

    # Draw the core every frame during active gameplay and end the game
    core.draw()

    if core.is_destroyed():
        HGame.GameOver = True

    for player in jumpers:
        if player.dead:
            if player.lives > 0:
                player.live()
            else:
                pass  # player stays dead
        else:
            all_dead = False

    if all_dead:
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