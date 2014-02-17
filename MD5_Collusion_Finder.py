#!usr/bin/python
import os
import hashlib
os.system("clear")
def getMD5Hash(textToHash=None):
    return hashlib.md5(textToHash).hexdigest()
print "Md5 collusion finder by Barak Tawily\n"
print getMD5Hash(str(13332))
c = raw_input("insert a md5 hash you want to collision:") 
#c4ca4238a0b923820dcc509a6f75849b
#b026324c6904b2a9cb4b88d6d61c81d1 - 1
counter = 0

while 1:
	md = getMD5Hash(str(counter))

	print "Number" + str(counter) + " ------ " + str(md) + " : " + str(c)
	if str(md) == str(c):
		print "got found!! " + str(counter) + " is equal"
		break
	else: counter=counter+1

