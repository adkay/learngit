from distutils.core import setup
import py2exe
import sys
 
#this allows to run it with a simple double click.
sys.argv.append('py2exe')
 
py2exe_options = {
        "includes": ["sip"],
        "compressed": 1,
        "optimize": 0,
        "ascii": 0,
        }
 
setup(
      name = 'PyQt Demo',
      version = '1.0',
      windows = ['g:\soft\main.py',], 
      zipfile = None,
      options = {'py2exe': py2exe_options}
      )