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

from javax.smartcardio import CommandAPDU
from terminal import ch_def
from util import usign, resp2str

# VISA application AIDs.
VISA_COD = "\xA0\x00\x00\x00\x03\x10\x10"

# MasterCard application AIDs.
# ...

# Interact application AIDs.
INTERAC_CAN = "\xA0\x00\x00\x02\x77\x10\x10"

    
# Other EMV related functions.
def parse_gpo_resp(resp):
    """ Extracts and return the Application Interchange Profile and the
    AFLs from the GET PROCESSING OPTIONS command response. """
    # determine the format of the GET PROCESSING OPTIONS response message.
    resp = list(resp)
    
    if resp.pop(0) == 0x80:
        # disregard the length
        resp.pop(0)
        
        # AIP consists of the next 2 bytes.
        aip = resp[:2]
        # and the AFL is the rest, minus the status code included in
        # the response.
        afl = resp[2:-2]
        
        return aip, afl
                
    else:
        print "format for the GPO response not yet supported ..."
        return None 
    
def parse_afl(afl):
    """takes an AFL and returns a list of tuples of the form (sfi, rnbr)."""
    result = []
    while len(afl) != 0:
        sfi = (afl[0] & 0xf8) >> 3
        first_record = afl[1]
        last_record = afl[2]
        for i in range(first_record,last_record+1):
            result.append((sfi,i))
        
        afl = afl[4:]
        
    return result
