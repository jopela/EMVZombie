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
from util import usign

# VISA application AIDs.
VISA_COD = "\xA0\x00\x00\x00\x03\x10\x10"

# MasterCard application AIDs.
# ...

# Interact application AIDs.
INTERAC_CAN = "\xA0\x00\x00\x02\x77\x10\x10"

# TODO: Refactor this class code for use with the python with statement?
class Card:
    
    def __init__(self):
        self.ch = ch_def()
        return
    
    # EMV commands for financial transaction. This implementation is based on 
    # EMV Integrated Circuit Card Specifications for Payment Systems, Book 3 
    # version 4.3. 
    def select(self, aid):
        """ Returns the command/response pair for the SELECT command.
         Parameter aid is a byte string representing the aid to select."""
        
        # SELECT command encoding.
        command = CommandAPDU(0x00, 0xa4, 0x04, 0x00, aid)
        return self.send_command(command)                 
        
    def application_block(self):
        print "please implement me"
        return
    
    def application_unblock(self):
        print "please implement me"
        return
    
    def card_block(self):
        print "please implement me"
        return
    
    def external_authenticate(self):
        print "please implement me"
        return
    
    def generate_application_cryptogram(self):
        print "please implement me"
        return
    
    def get_challenge(self):
        print "please implement me"
        return
    
    def get_data(self, msb_tag, lsb_tag):
        """ Returns the command/response pair for the GET DATA command. The 
        msb_tag and lsb_tag represent the most significant and least 
        significant part of the tag byte respectively."""
        
        # GET DATA command encoding.
        command = CommandAPDU(0x80, 0xca, msb_tag, lsb_tag)
        return
    
    def get_processing_options(self, pdol='\x83\00'):
        """ Returns the command/response pair for the GET PROCESSING OPTIONS
        command. If the pdol parameter is not specified, the default pdol value
        of 0x8300 is used."""
        
        # GET PROCESSING OPTIONS encoding
        command = CommandAPDU(0x80, 0xa8, 0x00, 0x00, pdol)
        return self.send_command(command)
    
    def internal_authenticate(self):
        print "please implement me"
        return    
    
    def pin_change_unblock(self):
        print "please implement me"
        return
    
    def read_record(self, sfi, rnbr):        
        # read record command encoding.
        # command = CommandAPDU(0x00, 0x82, rnbr, (sfi << 3 | 4))
        
        # TODO: for some reason, the commented command above DOES NOT WORK.
        # you need to manually add the Le parameter of the read_record command
        # Le. This should be investigated further but in the meantime,
        # let's use a work around and add it ourself manually.
        
        # Does this only happen when there is no command body? read further
        # about it in EMV book 3 v4.3 
        tmp = CommandAPDU(0x00, 0xb2, rnbr, (sfi << 3 | 4)).getBytes()
        tmp.append(0)
        command = CommandAPDU(tmp)
                
        return self.send_command(command)
               
        
    def verify(self, sfi,rnbr):
        print "please implement me"
        return
    
    # Helper methods
    def send_command(self,command):
        """ takes car of sending a given command and preparing the raw
        response for function return. """
        
        # this will take the array of signed values and cast it to a
        # list of "unsigned" integer. This is the expected type by most
        # of the EMVzombie toolkit functions.  
        f = lambda x : tuple([usign(i) for i in x]) 
        
        response = self.ch.transmit(command).getBytes()
        command = command.getBytes()
                
        return f(command), f(response)
    
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
            
        
        
    
      
  
 
    
    
    
    
    



    