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

from javax.smartcardio import TerminalFactory
from util import die


# GLOBAL VARIABLES
PROTO_DEF = "*"

def reader_list():
    """ Returns a list of all the available card readers."""
   
    # TODO: make sure exception is properly handled if there are no smartcard
    # reader connected.
    factory = TerminalFactory.getDefault()
    terminals = factory.terminals().list()
       
    return terminals

def terminal_select(name):
    """ Returns the reader that corresponds to the given reader identifier.
    return None if reader does not exists."""
    
    # TODO: make sure this does not catch fire with corner cases.
    factory = TerminalFactory.getDefault()
    terminal = factory.terminals().getTerminal(name)
    return terminal

def reader_name_def():
    """ Returns the name of the first reader found capable of performing
    an ATR with the card. The connection state is OPEN after the call.
    Returns None if connection is impossible. """
    
    # get the list 
    terminals = reader_list()
        
    for t in terminals:
        try:
            card = t.connect(PROTO_DEF)
            ch = card.getBasicChannel()
            card.disconnect(False)
            return t.getName()    
        except:
            pass
        
    return None

def ch_def():
    """ Returns the default channel with which communication with
    the card will occur. """
        
    try:
        reader_def = reader_name_def()
        t = terminal_select(reader_def)
        card = t.connect(PROTO_DEF)
        ch = card.getBasicChannel()
        return ch
    except:
        die("could not get a connection to the card with the default terminal.")
        
        
    
    
        

 
               
    
