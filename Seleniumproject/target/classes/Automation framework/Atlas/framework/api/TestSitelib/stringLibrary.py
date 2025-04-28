'''
A library for the string manipulation we needed for the SIO Runner.

Notes:

    * I don't know why I made this a class, esp. given all the methods are static.

Created on Oct 19, 2016

@author: reichert
'''


import binascii
import string

class StringLibraryError(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg

class StringLibrary(object):
    '''
    classdocs
    '''
    PRINTABLE = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~ \t\n\x0b\x0c'        
    

    def __init__(self):
        '''
        Constructor
        '''
        pass

    @staticmethod    
    def convertAsciiToBinary( aString ):
        """
        This method converts strings encoded in numeric formats into ASCII.
        Strings starting with number base encoding are parsed per that encoding.
        That is:
        
        0x - A hex encoded number
        0b - A binary encoded number
            """
        
        if aString[0] == '0':
            if aString[1] == 'x': return binascii.a2b_hex( aString[2:] )
            if aString[1] == 'b': return eval(aString)
            if aString[1] == 'd': pass
            
        return 0

    @staticmethod
    def convertBinaryToAscii( aString, radix="hex" ):
        """
        Qualcomm does not want preceeding 0x on responses.
        Qualcome wants leading 0's truncated. 
        """
        if len(aString) == 0: return ""
        hexString = "0x" + binascii.b2a_hex( aString )
        if radix == "hex":
            return hexString
        else:
            return "0b" + bin(eval(hexString))
    
    
    @staticmethod
    def stripLeadingCharacters( strIn, radix ):
        '''
        String is assumed to represent a number.
        This method removes leading radix indicators and leading 0's
        In the case of hex radix, it leaves an even number of characters, i.e., 
        the resulting string represents a number of whole bytes. 
        '''
        ptr = 0
        if strIn[0:2] == "0x": ptr = 2
        if strIn[0:2] == "0b": ptr = 2
        i = ptr
        if radix == "hex":
            if (len(strIn) % 2) != 0 :
                raise StringLibraryError("Hex radix string is not an even number of bytes: %s" % strIn)
            for i in range(ptr, len(strIn), 2):
                if ( strIn[i] != '0' ) or (strIn[i+1] != '0'): break;
            return strIn[i:]
        else:
            for i in range(ptr, len(strIn)):
                if ( strIn[i] != '0' ) or (strIn[i+1] != '0'): break;
            return strIn[i:]
        
    @staticmethod
    def compareStrings(actualValue, expectValue, radix):
        '''
        Input values may or may not have leading 0x
        Input values may or may not have leading 0's
        Expected values may indicate nibbles to ignore with "X"
        
        This comparison must start at LSB because expect values can only be 
        multiples of 8 bytes and actual values can be any number of bytes. 
        '''
        av = StringLibrary.stripLeadingCharacters(actualValue, radix)
        ev = StringLibrary.stripLeadingCharacters(expectValue, radix)
#        if ( len(av) != len(ev) ): return False
        compareLength = len(ev)     # len(ev) should be >= len(av)
        for j in range(compareLength):
            evIdx = (len(ev) - 1) - j
            avIdx = (len(av) - 1) - j
            if ev[evIdx] == 'X': continue 
            if (avIdx < 0): 
                if (ev[evIdx] == '0'): continue  # Expect 0's that have been stripped off the begining of AV
                if (ev[evIdx] != '0'): return False
            else:
                if  av[avIdx] != ev[evIdx]: return False
        return True
    
    @staticmethod
    def hex( value, precision ):
        formatString = "0x%0" + repr(precision) + 'x'
        return formatString % value
    
    
    @staticmethod
    def makePrintable( inputString ):
        """
        Besides removing most weird characters that can cause weird problems, also
        need to remove CRs as a CR w/o a LF will cause a line to be erased.
        
        string.printable is : 
        '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~ \t\n\r\x0b\x0c'
        Unfortunately, a lone CR, \r, can cause lines to be deleted.  So have my
        own list of characters which removes the \r:
        '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~ \t\n\x0b\x0c'        
        """
        return filter(lambda x: x in StringLibrary.PRINTABLE, inputString)
        