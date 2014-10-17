#!/usr/bin/python

import re
import os
import sys

def help():
	sys.stdout.write("Dropper Maker\n\n")
	sys.stdout.write("This will make a binary a C array.\n")
	sys.stdout.write("Useful for droppers.\nOutput will be saved to 'array.c'.\n")
	sys.stdout.write("Made by Yuval tisf Nativ under GPLv3\n")


sorted_array = []
everything = []
out_filename = "array.c"

if len(sys.argv) == 2:

	raw_array = os.popen('hexdump ' + sys.argv[1]).read()
	raw_array = str(raw_array)

	if raw_array.find("No such file") != -1:
		sys.stderr.write("The file specified was not found.\n")
		sys.exit(1)

	raw_array = raw_array.split('\n')

	for each in raw_array:
		tmp = each[8:]
		tmp = tmp.replace(" ", "")
		for each in re.findall(r'.{1,2}',tmp,re.DOTALL):
			everything.append(each)
		sorted_array.append(tmp)

	i = 0
	fp = open(out_filename, "w+")
	fp.write("unsigned char Dropped_elf[] = {\n")
	for i in range(0,len(everything),1):
		if i == len(everything)-1:
			fp.write("0x" + str(everything[i]) + " \n")
		else:
			if i%10 == 0:
				fp.write("0x" + str(everything[i]) + ", \n")
				i+=1
			else:
				fp.write("0x" + str(everything[i]) + ", ")
				i+=1
	fp.write("};\n\n")
	fp.write("unsigned int Dropped_elf_len = %s;\n\n" % str(len(everything)))
else:
	help()
	sys.exit(1)
