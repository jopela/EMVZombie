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
import argparse
import supertlv
from util import resp2str as r2str

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
    
    parser.add_argument(
                '-c',
                '--config',
                help='path to the config file. For more detail see config.yaml',
                type=argparse.FileType()
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
    print sel_pse_r
    
    # If the application supports PSE, add it to the set of supported
    # applications.
    if sel_pse_s == 0x9000:
        pse_aid = supertlv.find("84", r2str(sel_pse_r))
        # if we cannot retrieve the aid from the PSE response, it means the 
        # the card sent a malformed or invalid response. We do not really care
        # but we need to add the AID by some other way.
        if not pse_aid:
            pse_aid = [i for i in sel_aid[AID_INDEX] if (i != '\\' and i != 'x')]
        
        supp_app.add(pse_aid)
        # Also add the list of applications that can be extracted from the 
        # pse response.
        sfi = supertlv.find("88")
        
        if sfi:
            status = 0x9000
            while status == 0x9000:
                # read all the possible record of that SFI
                break
            
def select_all(terminal):
    """ Try to select all the applications know to the terminal and 
    returns the set of AID that returned 0x9000 for the SELECT command.
    """
    return None
                
if __name__ == "__main__":
    main()

