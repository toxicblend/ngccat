#!/usr/bin/env python

import re
from optparse import OptionParser

ln_re = re.compile("(?P<line>N\d+)?\s*(?P<rest>G.*)", re.I)
beginend_re = re.compile("\s*(?P<beginEnd>(\%)|(M2))\s*", re.I)
junk_re = re.compile("(\(Tool change\))|(T\d+ M06 .*)",re.I)

#self.reg = re.compile("(?P<line>N\d+)?\s*(?P<command>G\d+)\s*(X(?P<X>-?\d+(\.\d*)?))?\s*(Y(?P<Y>-?\d+(\.\d*)?))?\s*(Z(?P<Z>-?\d+(\.\d*)?))?(?P<extra>.*)", re.I)

def builtinCommand(command, outFile, isFirst, isLast):
  line = ""
  if command == "begin":
    line = "(begin)\nG64 P0.02 Q0.02\n(\\begin)\n"
  elif command == "end":
    line = "(end)\nM5\nM101\n(\\end)\n"
  elif command=="fine":
    line = "(fine)\nG64 P0.02 Q0.02\n(\\fine)\n"
  elif command=="fine2":
    line = "(fine)\nG64 P0.04 Q0.04\n(\\fine)\n"
  elif command=="fine3":
    line = "(fine)\nG64 P0.08 Q0.08\n(\\fine)\n"
  elif command=="rough":
    line = "(rough)\nG64 P0.4 Q0.4\n(\\rough)\n"
  elif command=="safez":
    line = "(safez)\nG0Z2.0F1000.0\n(\\safez)\n"  
  else:
    print("unknown built-in command: %s" % (command,))
    exit(1)
  if isFirst:
    outFile.write("%\n")  
  outFile.write(line)  
  if isLast:
    outFile.write("%\n")
    
def copyDataFromFile(inFileName, outFile, isFirst, isLast, keeplines):
  inFile = open(inFileName, 'r')
  if isFirst:
    outFile.write("%\n")   
  line = "(beginning %s)\n" % (inFileName,)
  outFile.write(line)
     
  try:
    for line in iter(inFile):
      if junk_re.search(line):
        continue
      if not keeplines:
        m = ln_re.search(line)
        if m and m.group("line"):
          line = m.group("rest") + "\n"
      m = beginend_re.search(line)
      if m:
        continue
        #line = "%s %d %d %d" % (m.group("beginEnd"), isFirst, isLast, beginProgramSeen)
      outFile.write(line)    
  finally:
    inFile.close()
  line = "(end of %s)\n" % (inFileName,)
  outFile.write(line)
  if isLast:
    outFile.write("%\n")
      
if __name__=="__main__":
  builtinCommands = ["begin", "end", "fine", "fine2", "fine3","rough", "safez"]
  parser = OptionParser()
  parser.add_option("-o", "--output", dest="outputFileName",
                      help="write report to FILE", metavar="FILE")
  parser.add_option("-q", "--quiet",
                    action="store_false", dest="verbose", default=True,
                    help="don't print status messages to stdout")
  parser.add_option("-l", "--keeplines",
                    action="store_true", dest="keeplines", default=False,
                    help="keep line numbering")  
  (options, args) = parser.parse_args()
  outFile = open(options.outputFileName, 'w')
  try:
    for i in range(len(args)):
      if args[i] in builtinCommands:
        builtinCommand(args[i],outFile,i==0,i==len(args)-1)
      else:
        inputFileName = args[i]
        copyDataFromFile(inputFileName, outFile,i==0, i==len(args)-1, options.keeplines)
  finally:
    outFile.close()
