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
from util import resp2str as r2str, partition

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
    
    args = parser.parse_args()
        
    if args.listaid:
        aid_list()
    elif args.aid:
        clone(args.aid)
    else:
        print "nothing to do, quitting"
        
                   
    return

def aid_list():
    """ Returns the set of aids supported by the card. """
        
    AID_INDEX = 0
    DESCRIPTION_INDEX = 1
    
    term = terminal.Terminal()
    supp_app = set([])
    
    # PSE selection.
    pse_aid = emv.aid['pse']
    sel_pse_c, sel_pse_r, sel_pse_s = term.select(pse_aid[AID_INDEX])
            
    # If the application supports PSE, add it to the set of supported
    # applications.
    if sel_pse_s == 0x9000:
        supp_app.add(pse_aid)
        
        # extract the list of applications supported by the card based on the 
        # PSE response.
        sfi = supertlv.find("88", sel_pse_r)
        
        if sfi:
            status = 0x9000
            while status == 0x9000:
                # read all the possible record of that SFIbran
                break
            
def select_all(terminal):
    """ Try to select all the applications know to the terminal and 
    returns the set of AID that returned 0x9000 for the SELECT command.
    """
    return None

def clone(aid):
    
    term = terminal.Terminal()
    # Application selection.
    select_c, select_r, select_s = term.select(aid)
    
    if select_s == 0x9000:
        print "*" * 10 + "Select Response" + "*" * 10
        print supertlv.human(select_r)
    else:
        print "select command returned error status {0}".format(hex(select_s))
    
    # get processing option.
    gpo_c, gpo_r, gpo_s = term.get_processing_options()
    
    if gpo_s == 0x9000:
        print "*" * 10 + "Get processing Option Response" + "*" * 10
        print supertlv.human(gpo_r)
    else:
        print "gpo command returned error status {0}".format(hex(select_s))
                              
if __name__ == "__main__":
    main()

