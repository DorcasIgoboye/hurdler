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
BACKGROUND_IMAGE_FILE='bg_cyber.png'
PARALAX_BACKGROUND_IMAGE_FILE='bg_parallax_grid.png'
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

RAMONA_SPRITES={
  'file':"Xbox 360 - Scott Pilgrim vs the World The Game - Ramona Flowers P3.png",
  'left_right_move_sprites':[
    {'name':"neutral pose",'location':(4,26),    'dimension':(36,70)},
    {'name':"Run pose 1",  'location':(630,120), 'dimension':(50,70)},
    {'name':"Run pose 2",  'location':(680,120), 'dimension':(45,70)},
    {'name':"Run pose 3",  'location':(730,120), 'dimension':(45,70)},
    {'name':"Run pose 4",  'location':(780,120), 'dimension':(45,70)},
    {'name':"Run pose 5",  'location':(825,120), 'dimension':(45,70)},
    {'name':"Run pose 6",  'location':(874,120), 'dimension':(43,70)},
    {'name':"Run pose 7",  'location':(917,120), 'dimension':(47,70)},
    {'name':"Run pose 8",  'location':(915,120), 'dimension':(50,70)}
  ],
  'dead_sprite':
    {'name':"dead pose",'location':(1174,728),'dimension':(75,40)}
}

RAMONA_SHOOT_SPRITE_SEQUENCE={  
  'file':"Xbox 360 - Scott Pilgrim vs the World The Game - Ramona Flowers P3.png",
  'shooting_sprites':[
    #{'name':"shoot pose 1",  'location':(635,1450),'dimension':(40,70)},    
    {'name':"shoot pose 2",  'location':(675,1450), 'dimension':(32,70)},    
    {'name':"shoot pose 3",  'location':(707,1450), 'dimension':(44,70)},
    {'name':"shoot pose 4",  'location':(751,1450), 'dimension':(49,70)},    
    {'name':"shoot pose 5",  'location':(800,1450), 'dimension':(50,70)},    
    {'name':"shoot pose 6",  'location':(850,1450), 'dimension':(51,70)},    
    {'name':"shoot pose 7",  'location':(898,1450), 'dimension':(84,70)},    
    {'name':"shoot pose 8",  'location':(982,1450), 'dimension':(84,70)},    
    {'name':"shoot pose 9",  'location':(1066,1450), 'dimension':(82,70)},    
    {'name':"shoot pose 10",  'location':(1148,1450), 'dimension':(89,70)},    
    {'name':"shoot pose 11",  'location':(1237,1450), 'dimension':(86,70)},        
    {'name':"shoot pose 12",  'location':(1323,1450), 'dimension':(50,70)},    
    {'name':"shoot pose 13",  'location':(1373,1450), 'dimension':(41,70)},    
    #{'name':"shoot pose 14",  'location':(1414,1450), 'dimension':(36,70)}    
  ]
}

#setting Jumper 2 sprites dictionary/database
SCOTT_SPRITES={
  'file':"Xbox 360 - Scott Pilgrim vs the World The Game - Scott Pilgrim P1.png",
  'left_right_move_sprites':[
    {'name':"neutral pose",'location':(5,8),    'dimension':(40,60)},
    {'name':"Run pose 1",  'location':(8,79),   'dimension':(40,60)},
    {'name':"Run pose 2",  'location':(50,75),  'dimension':(45,70)},
    {'name':"Run pose 3",  'location':(97,78),  'dimension':(45,70)},
    {'name':"Run pose 4",  'location':(155,82), 'dimension':(45,70)},
    {'name':"Run pose 5",  'location':(205,81), 'dimension':(45,70)},
    {'name':"Run pose 6",  'location':(245,77), 'dimension':(43,70)},
    {'name':"Run pose 7",  'location':(290,76), 'dimension':(47,70)},
    {'name':"Run pose 8",  'location':(341,81), 'dimension':(50,70)}
  ],
  'dead_sprite':
    {'name':"dead pose",'location':(219,1286),'dimension':(75,40)},
  'duck_sprite':
    {'name':"low height pose",'location':(233,1111),'dimension':(325-233,1145-1111)}  

}

print(CURRENT_VERSION)