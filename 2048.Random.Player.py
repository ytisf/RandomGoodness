import sys
import time
import signal
import random
import subprocess
from evdev import UInput, ecodes as e
from subprocess import PIPE, Popen

def GetActiveWindowTitle():
    return subprocess.Popen(["xprop", "-id", subprocess.Popen(["xprop", "-root", "_NET_ACTIVE_WINDOW"], stdout=subprocess.PIPE).communicate()[0].strip().split()[-1], "WM_NAME"], stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0].strip().split('"', 1)[-1][:-1]

def send_keys(object, key):
	object.write(e.EV_KEY, key, 1)
	object.write(e.EV_KEY, key, 0)
	ui.syn()


i = 5
moves = 100000

print("Go to 2048 window. ["+str(i)+"] secs.")
while i != 0:
	print(" " + str(i))
	time.sleep(1)
	i -= 1

print("Commencing...\n")

keys = ["e.KEY_UP", "e.KEY_DOWN", "e.KEY_LEFT", "e.KEY_RIGHT"]
keys = [105, 106, 103, 108]

#random.choice(foo)
ui = UInput()
current_title = GetActiveWindowTitle()
if 'Firefox' in current_title:
	while moves != 0:
		temp_key = random.choice(keys)
		send_keys(ui, temp_key)
		time.sleep(0.1)
		moves -= 1
	print("Done")
else:
	print("You're not on the firefox window.")

ui.close()
