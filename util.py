'''
Created on May 24, 2013
@author: Jonathan Pelletier (jonathan.pelletier1@gmail.com)

This file is part of EMVZombie.

EMVZombie is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

EMVZombie is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with EMVZombie.  If not, see <http://www.gnu.org/licenses/>.
'''

import sys

# Miscellaneous  helper functions use throughout all modules

def die(msg):
    print msg
    sys.exit(-1)

def usign(val):
    """Returns the unsigned value of the given integer on 8 bits."""
    return (val + (1 << 8)) % (1 << 8)
    
def resp2str(val):
    """returns a human readable string from a card command response."""
    return "".join([hex(i)[2:].zfill(2) for i in val])

def human(ite):
    """Takes an iterable of byte[] and return a list containing the hex 
    representations of these byte[]."""
    
    return [resp2str(val) for val in ite] 
       
