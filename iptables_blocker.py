#!/usr/bin/python
import os
import sys
import socket

iptables = "/sbin/iptables"
blacklist = "blacklist.txt"

class bcolors:
	BLUE = '\033[94m'
	GREEN = '\033[92m'
	WARNING = '\033[93m'
	ENDC = '\033[0m'

	OKGREEN = GREEN + "[+] " + ENDC
	OKBLUE = BLUE + "[+] " + ENDC
	BADRED = WARNING + "[-] " + ENDC

def banner():
	if os.getuid() == 0:
		pass
	else:
		print bcolors.BADRED + "Go and get root rights and think about what you've done!"
		sys.exit(1)

	print bcolors.WARNING + "\n|==========================================|" + bcolors.ENDC
	print bcolors.WARNING + "|==========================================|" + bcolors.ENDC
	print bcolors.WARNING +    "| "+bcolors.BLUE+"     Pentesters' Black List Applyer     "+bcolors.WARNING+" |" + bcolors.ENDC
	print bcolors.WARNING +   "| "+bcolors.GREEN+"          By tisf under GPLv3         "+bcolors.WARNING+"   |" + bcolors.ENDC
	print bcolors.WARNING + "|==========================================|" + bcolors.ENDC
	print bcolors.WARNING + "|==========================================|" + bcolors.ENDC + "\n"

def execme(command):
	#""" Execute a command and return 0 or 1 """
	command = str(command)
	output = os.system(command)
	if output == "":
		return 0
	else:
		return 1

def flash_iptable_rules():
	#""" Flash all iptables Rules """

	flash = (iptables + " -F")
	output = execme(flash)	
	return output

def stop_him(ip):
	main_err_stat = 0
	a = execme(iptables + " -A OUTPUT -d " + ip + " -j DROP")
	main_err_stat += a
	a = execme(iptables + " -A FORWARD -d " + ip + " -j DROP")
	main_err_stat += a
	a = execme(iptables + " -A INPUT -d " + ip + " -j DROP")
	main_err_stat += a
	return main_err_stat
	
def finalle():
	#"""   Last rules to be added to get lowest priority   """

	execme(iptables + " -P OUTPUT ACCEPT")
	execme(iptables + " -P INPUT ACCEPT")
	execme(iptables + " -P FORWARD ACCEPT")

def back2normal():

	execme(iptables + " -P OUTPUT ACCEPT")
	execme(iptables + " -P INPUT ACCEPT")
	execme(iptables + " -P FORWARD ACCEPT")

def main():
	# Argvs
	total = len(sys.argv)
	cmdargs = str(sys.argv)
	script_name = str(sys.argv[0])
	filename = ""
	try:
		filename = str(sys.argv[1])
	except:
		print bcolors.OKBLUE + "No filename given. Using 'blacklist.txt' as default."
		filename == "blacklist.txt"
	if filename == "-h":
		banner()
		print "Usage: \t" + script_name + " <ip_list>"
		print "\tIf no file was given will try 'blacklist.txt'."
		print "\tWill open up your firewall before a pentest and block particular IPs."
		sys.exit(0)

	banner()

	bl_sanatized = []
	validated_addresses = []
	bad_addresses = []

	# Read file and get IPs
	try:
		with open(blacklist) as f:
			blacklist_ips = f.readlines()
	except IOError:
		print bcolors.BADRED + "Unable to load blacklist file."
		sys.exit(1)

	# Sanatize new lines
	for each in blacklist_ips:
		bl_sanatized.append(each.rstrip('\n'))

	# Check that the IPs are valid
	for ip in bl_sanatized:
		try:
			socket.inet_aton(ip)
			validated_addresses.append(ip)
		except socket.error:
			bad_addresses.append(ip)

	# Testing for bad IPs
	if len(bad_addresses) > 0:
		message = bcolors.BADRED + "There are mal formed addesses in the file: "
		for each in bad_addresses:
			message += str(each) + ", "
		print message
		qstn = raw_input("\n" + bcolors.OKBLUE + "Do you wish to continue only with good ones [y/n]?\n\t\t")
		if qstn.rstrip('\n') == 'y':
			print bcolors.OKBLUE + "Proceeding..."
		else:
			print bcolors.BADRED + "Exiting now."
			sys.exit(1)

	# Continue Blocking Everything
	for johnny in validated_addresses:
		okay = stop_him(johnny)
		if okay == 1:
			print(bcolors.BADRED + "Error with " +str(johnny)+ ". Continuing")
		else:
			print(bcolors.OKGREEN + str(johnny) + " added.")

	# Making sure everything else is on ACCEPT
	finalle()

	skipped = "\n" + bcolors.OKBLUE + "Skipped the following addresses: "
	for mal in bad_addresses:
		skipped += str(mal) + ", "

	print skipped

	while 1:
		quit = raw_input("\nType 'q' when you are finished.\nDo NOT terminate with CTRL+C!  [q] ")
		quit = quit.rstrip('\n')
		if quit == "q":
			print bcolors.OKBLUE + "Quitting.\n"
			flash_iptable_rules()
			back2normal()
			a = bcolors.GREEN + "               ACCEPT" + bcolors.BLUE
			a += "\t                          ,,\n"
			a += "\t                         ';;\n"
			a += "\t                          ''\n"
			a += "\t            ____          ||\n"
			a += "\t           ;    \         ||\n"
			a += "\t            \,---'-,-,    ||\n"
			a += "\t            /     (  o)   ||\n"
			a += "\t          (o )__,--'-' \  ||\n"
			a += "\t,,,,       ;'uuuuu''   ) ;;\n"
			a += "\t\   \      \ )      ) /\//\n"
			a += "\t '--'       \'nnnnn' /  \\\n"
			a += "\t   \\      //'------'    \\\n"
			a += "\t    \\    //  \           \\\n"
			a += "\t     \\  //    )           )\n"
			a += "\t      \\//     |           |\n"
			a += "\t       \\     /            |\n"
			a += "\t\n"
			a += "\t       ALL THE "+bcolors.WARNING+"TRAFFIC!\n" + bcolors.ENDC
			print a
			print bcolors.OKBLUE + "Did you get that root shell? :)"
			sys.exit(0)
		else:
			pass

if __name__ == "__main__":
	main()

