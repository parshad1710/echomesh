from __future__ import absolute_import, division, print_function, unicode_literals

import cechomesh

from echomesh.base import Config
from echomesh.color import Combine
from echomesh.expression import Expression
from echomesh.output.Poll import Poll
from echomesh.util import Log

LOGGER = Log.logger(__name__)

class Visualizer(Poll):
  INSTANCE = None

  def __init__(self, light_count=None, period=None, transform=None, **kwds):
    assert not Visualizer.INSTANCE
    Visualizer.INSTANCE = self

    assert cechomesh.is_started()
    self.lighting_window = cechomesh.PyLightingWindow()
    self.period = period
    self.transform = transform

    self.period_set = period is not None
    self.light_count_set = light_count is not None
    self.transform_set = transform is not None

    if self.light_count_set:
      self.set_light_count(light_count)

    Config.add_client(self)
    super(Visualizer, self).__init__(
      is_redirect=False, period=self.period, **kwds)

  def _after_thread_pause(self):
    self.lighting_window.close()

  def snapshot(self, filename):
    self.lighting_window.save_snapshot_to_file(filename)

  def config_update(self, get):
    if not self.light_count_set:
      self.set_light_count(get('light', 'count'))

    if not self.period_set:
      self.period = Expression.convert(get('light', 'visualizer', 'period'))
    if not self.transform_set:
      transform = get('light', 'visualizer', 'transform')
      if transform:
        try:
          self.transform = cechomesh.Transform(transform)
        except:
          LOGGER.error('Don\'t understand transform %s', transform)
    self.brightness = Expression.convert(get('light', 'brightness'))
    if self.transform:
      self.brightness = self.transform.apply(self.brightness)

  def set_light_count(self, light_count):
    self.lighting_window.set_light_count(light_count)

  def emit_output(self, data):
    lights = Combine.combine(data)
    lights.scale(self.brightness)
    self.lighting_window.set_lights(lights)