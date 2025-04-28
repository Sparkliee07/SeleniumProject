'''
Created on Aug 28, 2016

TOOD: This is working pretty well.  Remaining issue is that commands with parens around parameters end up with nested
      tuples:

      ('IsSlotThere', ((1, 2, (True,)),))
      ('IsSlotThere', ((1, 2),))
      ('IsSlotThere', ((1,),))


@author: reichert
'''

import shlex

class TerParserError(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg
    
class TerParser(object):


    def __init__(self):
        self.areParensRequired = False
        self.areCommasWhiteSpace = True

    def parseCommand(self, cmd):
        return self.parseCommandLineCommand(cmd)

    def parseCommandLineCommand(self, cmd):
        lexer = shlex.shlex(cmd)
        try:
            methodName = lexer.get_token()
            paramString = "("
            for token in lexer:
                if token not in (','):
                    paramString += token
                    if token not in ('('):
                        paramString += ","
            paramString += ")"
        except Exception as e:
            # Raise a custom error with a message including the command that caused the issue
            raise TerParserError(f"ERROR -- Couldn't parse: {cmd}") from e
                
        try:
            params = eval(paramString)
            return methodName,params

        except Exception as e:
            raise TerParserError(f"ERROR -- Couldn't evaluate parameters: {paramString}") from e

