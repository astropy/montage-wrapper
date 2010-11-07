from commands import *
from wrappers import *

__version__ = '0.9.1'

# Check whether Montage is installed
installed = False
for dir in os.environ['PATH'].split(':'):
    if os.path.exists(dir + '/mProject'):
        installed = True
        break

if not installed:
    raise Exception("Montage commands are not in your PATH")
