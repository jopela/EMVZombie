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

#TODO: right now main is used mainly for hand-testing. Once the design 
# begins to solidify, we need to move testing to a proper testing
# framework (nose ?).

#TODO: include command line argument parsing logic in main.
import emv
import terminal
from util import resp2str
import argparse

def main():
    
    parser = argparse.ArgumentParser()
    
    parser.add_argument(
                '-a',
                '--aid',
                help='creates a card clone for application aid'\
                ' if this is not specified, the tool will create a clone with'\
                ' the content of all supported applications.',
                default = None
                )
    
    parser.add_argument(
                '-l',
                '--listaid',
                help='print the list of all supported application aid and quit.',
                action='store_true'
                )
    
    args =  parser.parse_args(['--listaid'])
    
    if args.listaid:
        aid_list()
            
    return

def aid_list():
    """ Returns the set of aids supported by the card. """
        
    AID_INDEX = 0
    DESCRIPTION_INDEX = 1
    term = terminal.Terminal()
    supp_app = set([])
    
    # PSE selection.
    sel_aid = emv.aid['pse']
    sel_pse_c, sel_pse_r, sel_pse_s = term.select(sel_aid[AID_INDEX])
    
    # if the application supports pse, add it to the set of supported
    # applications.
    if sel_pse_s == 0x9000:
        supp_app.add('pse')
        # also add the list of application that can be extracted from the 
        # pse response
        print sel_pse_r     
        
if __name__ == "__main__":
    main()

