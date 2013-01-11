from __future__ import absolute_import, division, print_function, unicode_literals

import os
import os.path
import random
import time

from echomesh.config import Config
from echomesh.graphics import Rect
from echomesh.util import Log
from echomesh.util.DefaultFile import DefaultFile
from echomesh.util.ThreadLoop import ThreadLoop

from pi3d import Display
from pi3d import Texture

LOGGER = Log.logger(__name__)

DIMENSIONS = Config.get('pi3d', 'dimensions')
BACKGROUND = Config.get('pi3d', 'background')

DISPLAY = Display.create(False, *DIMENSIONS, background=BACKGROUND)

DEFAULT_IMAGE_DIRECTORY = DefaultFile('assets/image')

PI3D_DISPLAY = None
DO_PRELOAD = not True

class Pi3dDisplay(ThreadLoop):
  def __init__(self, echomesh):
    super(Pi3dDisplay, self).__init__()
    self.echomesh = echomesh
    self.texture_cache = Texture.Cache()
    self.sprites = []
    self.count = 0
    self.display = DISPLAY
    self.preload()
    global PI3D_DISPLAY
    PI3D_DISPLAY = self

  def add_sprite(self, *sprites):
    self.display.add_sprites(*sprites)

  def run(self):
    try:
      self.display.frames_per_second = Config.get('update_interval')
      self.is_open = self.display.loop_running()
    except:
      self.close()
      import traceback
      LOGGER.critical(traceback.format_exc())
      raise

  def load_texture(self, imagefile):
    if imagefile == '$random':
      imagefile = random.choice(os.listdir(DEFAULT_IMAGE_DIRECTORY.directory))

    imagefile = DEFAULT_IMAGE_DIRECTORY.expand(imagefile)
    return self.texture_cache.create(imagefile)

  def preload(self):
    if DO_PRELOAD:
      for imagefile in os.listdir(DEFAULT_IMAGE_DIRECTORY):
        self.load_texture(imagefile)

  def close(self):
    super(Pi3dDisplay, self).close()
    self.display.destroy()
    self.echomesh.close()