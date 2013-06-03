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

import emv
from util import resp2str, usign

def main():
    
    # Application selection
    card = emv.Card()
    
    select_c , select_r = card.select(emv.VISA_COD)
    gpo_c, gpo_r = card.get_processing_options() 
        
    aip, afl = emv.parse_gpo_resp(gpo_r)
    
    
    print "afl parsed", emv.parse_afl(afl)
                   
    return               
    
if __name__ == "__main__":
    main()

