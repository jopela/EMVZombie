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

# VISA application AIDs.
VISA_COD = "\xA0\x00\x00\x00\x03\x10\x10"

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
        
        # SELECT command.
        command = CommandAPDU(0x00, 0xa4, 0x04, 0x00, aid)
        response = self.ch.transmit(command)
        
        return command.getBytes(), response.getBytes()
        
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
    
    def get_data(self):
        print "please implement me"
        return
    
    def get_processing_options(self, pdol='\x83\00'):
        """ Returns the command/response pair for the GET PROCESSING OPTIONS
        command. If the pdol parameter is not specified, the default pdol value
        of 0x8300 is used."""
        
        # GET PROCESSING OPTIONS encoding
        command = CommandAPDU(0x80, 0xa8, 0x00, 0x00, pdol)
                       
        
        return
    
    def internal_authenticate(self):
        print "please implement me"
        return
    
    def pin_change_unblock(self):
        print "please implement me"
        return
    
    def read_record(self, sfi,rnbr):
        print "please implement me"
        return
    
    def verify(self, sfi,rnbr):
        print "please implement me"
        return
    