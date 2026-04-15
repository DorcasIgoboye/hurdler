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

# versions
import os
from datetime import date
CURRENT_VERSION=os.path.realpath( __file__).split(os.path.sep)[-2]+'_v10 '+date.strftime(date.today(),'%b %d %Y')

#collectibles constants
COLLECTIBLE_MAX_PERIOD=3000 #milliseconds
COLLECTIBLES_TIMER_TICK_PERIOD=100 #milliseconds, 100 will make it tick 10 times a second    
PRIZE_COUNT=10 # count of prizes in the list
PRIZE_PROBABILITY_RANGES=[10,30] #there is 10% changes for prize to be a vaccine


#hurdler game constants
ACCELERATION_CONST = 0.9
FRICTION_COEF = -0.12
JUMP_VELOCITY_KICK=-27 #little sprites need to reach the top too :)
MOVE_TIME_CONST=0.5
HURDLE_VELOCITY=10
BULLET_VELOCITY=20
STRIDE_SIZE=20
IDLE_POSE_INDEX=0

LIVES_COUNT=3

GAME_CAPTION="Cyber Infection: Firewall Collapse"
BACKGROUND_IMAGE_FILE='bgfirewall.png'
PARALAX_BACKGROUND_IMAGE_FILE='bgfirewall.png'
GAME_OVER_BACKGROUNG_IMAGE='game_over_screen.png'
BACKGROUND_MUSIC_FILE='background.mp3'
SAD_MUSIC_FILE='cashreg.wav'
COUNTDOWN_BEEP='count_beep.mp3'
COUNTDOWN_GO='go.mp3'
GAME_OVER_SOUND='game_over.mp3'
BOSS_HIT_SOUND='boss_hit.mp3'
BOSS_ATTACK_SOUND='boss_attack.mp3'
DEFAULT_BACKGROUND_MUSIC_ON=False #put this on False ASAP so that you do not go crazy

#setting Jumper 1 sprites dictionary/database      
#to find dimensions of a sprite, you need to load it up in some paint program
#then hover with the mouse on it and estimate the pixel position of its left top corner as well as its pixel width and height

RAMONA_SPRITES = {
  'file': "Xbox 360 - Scott Pilgrim vs the World The Game - Ramona Flowers P3.png",

  'left_right_move_sprites': [
    {'name': "idle1", 'location': (0, 128), 'dimension': (64,64)},
    {'name': "idle2", 'location': (64, 128), 'dimension': (64,64)},
    {'name': "idle3", 'location': (128, 128), 'dimension': (64,64)},

    {'name': "run1", 'location': (0, 64), 'dimension': (64,64)},
    {'name': "run2", 'location': (64, 64), 'dimension': (64,64)},
    {'name': "run3", 'location': (128, 64), 'dimension': (64,64)},
    {'name': "run4", 'location': (192, 64), 'dimension': (64,64)},
    {'name': "run5", 'location': (256, 64), 'dimension': (64,64)},
    {'name': "run6", 'location': (320, 64), 'dimension': (64,64)}
  ],

  'dead_sprite': {
    'name': "dead",
    'location': (0, 34*64),
    'dimension': (64,64)
  }
}

RAMONA_SHOOT_SPRITE_SEQUENCE = {
  'file': "Xbox 360 - Scott Pilgrim vs the World The Game - Ramona Flowers P3.png",

  'shooting_sprites': [
    {'name': "shoot1", 'location': (0, 192), 'dimension': (64,64)},
    {'name': "shoot2", 'location': (64, 192), 'dimension': (64,64)},
    {'name': "shoot3", 'location': (128, 192), 'dimension': (64,64)},
    {'name': "shoot4", 'location': (192, 192), 'dimension': (64,64)},
    {'name': "shoot5", 'location': (256, 192), 'dimension': (64,64)}
  ]
}

#setting Jumper 2 sprites dictionary/database
SCOTT_SPRITES = {
  'file': "Xbox 360 - Scott Pilgrim vs the World The Game - Scott Pilgrim P1.png",

  'left_right_move_sprites': [
    {'name': "neutral pose", 'location': (0*64, 2*64), 'dimension': (64, 64)},
    {'name': "Run pose 1",   'location': (1*64, 2*64), 'dimension': (64, 64)},
    {'name': "Run pose 2",   'location': (2*64, 2*64), 'dimension': (64, 64)},
    {'name': "Run pose 3",   'location': (3*64, 2*64), 'dimension': (64, 64)},
    {'name': "Run pose 4",   'location': (4*64, 2*64), 'dimension': (64, 64)},
    {'name': "Run pose 5",   'location': (5*64, 2*64), 'dimension': (64, 64)},
    {'name': "Run pose 6",   'location': (6*64, 2*64), 'dimension': (64, 64)},
    {'name': "Run pose 7",   'location': (7*64, 2*64), 'dimension': (64, 64)},
    {'name': "Run pose 8",   'location': (8*64, 2*64), 'dimension': (64, 64)}
  ],

  'dead_sprite': {
    'name': "dead pose",
    'location': (0*64, 0*64),
    'dimension': (64, 64)
  },

  'duck_sprite': {
    'name': "duck pose",
    'location': (1*64, 1*64),
    'dimension': (64, 64)
  }
}

print(CURRENT_VERSION)