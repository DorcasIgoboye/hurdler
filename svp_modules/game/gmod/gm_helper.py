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

import sys
import os
import gm_const as gc
import __main__

def getAssetFile(asset_path,fileName):
  #p=os.path.join(os.path.dirname(os.path.relpath(__file__)),asset_path,fileName)
  p=os.path.join(os.path.dirname(os.path.relpath(__main__.__file__)),asset_path,fileName)
  if os.path.exists(p):
    return p
  else:
    raise Exception("Path [{0}] does not exist".format(p))

def getSpriteFile(fileName):
  return getAssetFile(gc.ASSET_PATH_SPRITES,fileName)

def getSoundFile(fileName):
  return getAssetFile(gc.ASSET_PATH_SOUNDS,fileName)

def getImageFile(fileName):
  return getAssetFile(gc.ASSET_PATH_IMAGES,fileName)
