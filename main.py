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
                '--list-aid',
                help='print the list of all supported application aid and quit.'
                )
    
    input = ['--help']
    args = parser.parse_args(input)
        
    return               
    
if __name__ == "__main__":
    main()

