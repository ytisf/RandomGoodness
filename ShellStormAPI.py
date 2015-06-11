#!/usr/bin/python

import sys
import urllib2
from tabulate import tabulate

ERR = -1
GOOD = 0

class ShellStormSearch():

	def __init__(self):
		self._SearchURL = "http://shell-storm.org/api/?s="
		self._SearchSplitter = "*"
		self._CSVSplitter = "::::"
		self._GetURL = " http://shell-storm.org/shellcode/files/shellcode-"

	def search(self, query):

		try:
			search_string = query.replace(" ", self._SearchSplitter)
			f = urllib2.urlopen(self._SearchURL + search_string)
			answer = f.read()
			f.close()

		except urllib2, e:
			print "Error in socket: %s" % e
			return ERR

		except:
			print "Unknown error."
			return ERR

		gib = self.parseHTML(answer)
		return gib

	def parseHTML(self, raw):
		full_answer = []
		b = raw.split("\n")
		for ansr in b:
			this = ansr.split(self._CSVSplitter)
			try:			
				loopy_temp = { "Author": this[0], "Platform": this[1], "Title": this[2],
								"ID": this[3], "URL": this[4]}
				full_answer.append(loopy_temp)
			except:
				# This is probably an empty line
				continue
		
		if len(full_answer) != 0:
			return full_answer
		else:
			return GOOD

	def printTable(self, parsed):
		print tabulate(parsed, tablefmt='orgtbl', headers="keys")

	def getShellCode(self, shellID):
		try:
			getIt = self._GetURL + str(shellID) + ".php"
			f = urllib2.urlopen(getIt)
			answer = f.read()
			f.close()
			return answer

		except IOError, e:
			print "Error! %s" % e
			return ERR

		except:
			print "General Error"
			return ERR


# Run a search
a = ShellStormSearch()
raw = a.search("windows xp sp3")
a.printTable(raw)

# Get one with particular ID
sc_id = 569
print a.getShellCode(sc_id)

