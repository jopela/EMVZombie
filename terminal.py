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

from javax.smartcardio import TerminalFactory, CommandAPDU
import util

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
        util.die("could not get a connection to the card with the default terminal.")
        
# TODO: Refactor this class code for use with the Python with statement?
class Terminal:
    
    def __init__(self):
        self.ch = ch_def()
        return
    
    # EMV commands for financial transaction. This implementation is based on 
    # EMV Integrated Circuit Terminal Specifications for Payment Systems, Book 3 
    # version 4.3. 
    def select(self, aid):
        """ Returns the command/response pair for the SELECT command.
         Parameter aid is a byte string representing the aid to select."""
        aid = util.str2ba(aid)
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
    
    def generate_application_cryptogram(self, tran_data):
        """ Returns the command/response pair for the GENERATE APPLICATION
        CRYPTOGRAM command. The parameter tran_data is the transaction related
        specified by either CDOL1 or CDOL2. """       
        
        return
    
    def get_challenge(self):
        """returns the command/response pair for the GET CHALLENGE command."""
        # This Java package is either cursed or I do not get it.
        # the command below will not work. Issuing the command by "hand"
        # as a work around until further investigation. This is similar
        # to the read_record, and get_data problem.
          
        # command = CommandAPDU(0x00, 0x84, 0x00, 0x00)
        command = CommandAPDU('\x00\x84\x00\x00\x00')
        return self.send_command(command)
                   
    def get_data(self, msb_tag, lsb_tag):
        """ Returns the command/response pair for the GET DATA command. The 
        msb_tag and lsb_tag represent the most significant and least 
        significant part of the tag byte respectively."""
        
        # GET DATA command encoding. 
        
        # Same problem as in READ RECORD. See read_record() for more details.
        tmp = CommandAPDU(0x80, 0xca, msb_tag, lsb_tag).getBytes()
        tmp.append(0)
        command = CommandAPDU(tmp)
        return self.send_command(command)
                
    
    def get_processing_options(self, pdol='\x83\00'):
        """ Returns the command/response pair for the GET PROCESSING OPTIONS
        command. If the pdol parameter is not specified, the default pdol value
        of 0x8300 is used."""
        
        # GET PROCESSING OPTIONS encoding
        command = CommandAPDU(0x80, 0xa8, 0x00, 0x00, pdol)
        return self.send_command(command)
    
    def internal_authenticate(self, auth_data):
        """ Return the command/response pair for the INTERNAL AUTHENTICATE
        command. The parameter auth_data shall be encoded according to the DDOL.
        """
        #TODO: test card does not support DDA. Find a test card that does and
        # test this function.
        command = CommandAPDU(0x00,0x88,0x00,0x00, auth_data)        
        return self.send_command(command)    
    
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
    def send_command(self,com):
        """ takes car of sending a given command and preparing the raw
        response for function return. """
        
        # this will take the array of signed values and cast it to a
        # list of "unsigned" integer. This is the expected type by most
        # of the EMVzombie toolkit functions.  
        f = lambda x : tuple([util.usign(i) for i in x]) 
        
        response_all = self.ch.transmit(com).getBytes()
        
        response = response_all[:-2]
        command = com.getBytes()
        
        sw1 = util.usign(response_all[-2])
        sw2 = util.usign(response_all[-1])
        
        status = (sw1 << 8) | (sw2)
        
        b_command = f(command)
        b_response = f(response)
                           
        return util.resp2str(b_command), util.resp2str(b_response), status
        
    
    
        

 
               
    
