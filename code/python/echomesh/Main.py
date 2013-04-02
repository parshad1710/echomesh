from __future__ import absolute_import, division, print_function, unicode_literals

ECHOMESH_EXTERNALS_OVERRIDE_SYSTEM_PACKAGES = True
# If this is True, you want Echomesh to use its own external packages in
# preference to any you might have installed in your system path.

USE_DIGITS_FOR_PROGRESS_BAR = not False
PRINT_STARTUP_TIMES = not False
COUNT = 0

def main():
  import sys

  times = []

  def p(msg=''):
    """Print progress messages while echomesh loads."""
    print(msg, end='\n' if msg else '')
    global COUNT
    dot = str(COUNT % 10) if USE_DIGITS_FOR_PROGRESS_BAR else '.'
    print(dot, end='')
    COUNT += 1

    sys.stdout.flush()

    import time
    times.append(time.time())

  p('Loading echomesh ')

  import os.path
  p()

  from echomesh.base import Path
  p()  # 11ms

  # Make sure we can find the external packages,
  external = os.path.join(Path.CODE_PATH, 'external')
  p()

  if ECHOMESH_EXTERNALS_OVERRIDE_SYSTEM_PACKAGES:
    sys.path.insert(1, external)
  else:
    sys.path.append(external)
  p()

  from echomesh.base import Args
  Args.set_arguments(sys.argv)

  from echomesh.base import Config
  p()  # 1215ms

  Config.recalculate()
  p() # 1329ms

  autostart = Config.get('autostart')
  p()

  if autostart and not Config.get('permission', 'autostart'):
    from echomesh.util import Log
    print()
    Log.logger(__name__).info("Not autostarting because autostart=False")
    exit(0)
  p()

  from echomesh import Instance
  p()  # This is the big one, taking 3709ms on my RP.

  instance = Instance.Instance()
  p()  # 599ms

  print()

  if Config.get('diagnostics', 'startup_times'):
    print()
    for i in range(len(times) - 1):
      print(i, ':', int(1000 * (times[i + 1] - times[i])))
    print()

  instance.run()
  instance.loop()
  instance.join()

  if Config.get('diagnostics', 'unused_configs'):
    import yaml
    print(yaml.safe_dump(Config.get_unvisited()))

  reason = 'at your request' if instance.quitting else 'due to a fatal error'
  print('echomesh shut down %s.' % reason)
