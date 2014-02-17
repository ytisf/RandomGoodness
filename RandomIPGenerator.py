#!/usr/bin/python
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                    ..__...__.........._____.
#                    _/  |_|__|._______/  ___\
#                    \   __\  |/  ___/\   __\.
#                    .|  |.|  |\___ \..|  |...
#                    .|__|.|__/____  >.|__|...
#                    ..............\/.........
#
#                 Random IP Addresses Generator
#
#       Build by Yuval (tisf) Nativ from See-Security Group
#                  http://www.see-security.com
#                 https://avtacha.wordpress.com
#
#     .__.................__......................_._.........
#     / _\.___..___....../ _\.___..___._..._._.__(_) |_._..._.
#     \ \./ _ \/ _ \_____\ \./ _ \/ __| |.| | '__| | __| |.| |
#     _\ \  __/  __/_____|\ \  __/ (__| |_| | |..| | |_| |_| |
#     \__/\___|\___|.....\__/\___|\___|\__,_|_|..|_|\__|\__, |
#     ..................................................|___/.
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from random import randrange
import sys
import getopt

def restart_line():
    sys.stdout.write('\r')
    sys.stdout.flush()

def printhelp():
   print ''
   print '                    ..__...__.........._____.'
   print '                    _/  |_|__|._______/  ___\ '
   print '                    \   __\  |/  ___/\   __\.'
   print '                    .|  |.|  |\___ \..|  |...'
   print '                    .|__|.|__/____  >.|__|...'
   print '                    ..............\/.........'
   print ''
   print '          Created By Yuval Nativ (tisf) of See-Security'
   print '                   http://www.see-security.org'
   print '                  https://avtacha.wordpress.com'
   print ''
   print 'Syntax not used properly.'
   print 'Use the -a or --amount to choose number of random IPs to generate.'
   print 'Use the -o or --type to choose if output format will be CSV or TXT.'
   print ''
   print 'randips.py -a <amount2generate> -o <type2export>'
   print '      ex.:  randips.py -a 300 -o csv > ips.csv'
   print ''

def main(argv):
   amount2generate = ''
   type2export = ''
   try:
      opts, args = getopt.getopt(argv,"ha:o:h",["amount=","type=","help="])
   except getopt.GetoptError:
      printhelp()
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         printhelp()
         sys.exit()
      elif opt in ("-a", "--amount"):
         amount2generate = arg
      elif opt in ("-h", "--help"):
         help = arg
      elif opt in ("-o", "--type"):
         type2export = arg
   if type2export=='':
      printhelp()
      sys.exit()
   if amount2generate=='':
      printhelp()
      sys.exit()
   not_valid = [10,127,254,255,1,2,169,172,192]
   i=0
   if type2export=='csv':
       while i<int(amount2generate):
          first = randrange(1,256)
          while first in not_valid:
             first = randrange(1,256)
          ip = ".".join([str(first),str(randrange(1,256)),str(randrange(1,256)),str(randrange(1,256))])
          restart_line()
          sys.stdout.write(ip)
          sys.stdout.flush()
          print ';'
          i=i+1

   if type2export=='txt':
       while i<int(amount2generate):
          first = randrange(1,256)
          while first in not_valid:
             first = randrange(1,256)
          ip = ".".join([str(first),str(randrange(1,256)),str(randrange(1,256)),str(randrange(1,256))])
          print ip
          i=i+1

if __name__ == "__main__":
   main(sys.argv[1:])
