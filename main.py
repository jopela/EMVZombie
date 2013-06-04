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
from util import resp2str, usign

def main():
    
    print "GO GO Gadget o-card!"
    # DEBUG quick function renaming
    f = lambda x: resp2str(x)
    
    # Application selection
    card = emv.Card()
    
    # SELECT
    select_c , select_r = card.select(emv.VISA_COD)
    
    print "SELECT"
    print resp2str(select_c), resp2str(select_r)
    
    # GET PROCESSING OPTIONS
    gpo_c, gpo_r = card.get_processing_options()
    
    print "GET PROCESSING OPTIONS"
    print f(gpo_c), f(gpo_r)    
        
    # Extract the aip and the afl from the GPO answer.
    aip, afl = emv.parse_gpo_resp(gpo_r)
    
    # Read all the records from the card into a dictionary.
    records_id = emv.parse_afl(afl)
    card_records = dict()
    
    for r in records_id:
        sfi = r[0]
        rnbr = r[1]
        rrec_c, rrec_r = card.read_record(sfi, rnbr)
        card_records[rrec_c] = rrec_r        
    
    print "READ RECORD (all)"
    
    for k in card_records.keys():
        print f(k),f(card_records[k])
        
    print "done!"
                  
    return               
    
if __name__ == "__main__":
    main()

