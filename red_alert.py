damn = "http://www.tzevaadom.com/history.html"
interval = 4

import pygtk
pygtk.require('2.0')
import pynotify
import time
import urllib2
from BeautifulSoup import BeautifulSoup
from prettytable import PrettyTable


def get_html():
	response = urllib2.urlopen(damn);
	response = response.read()
	return response


def get_table(html):

	alert = []
	all_alerts = []

	soup = BeautifulSoup(''.join(html))
	table = soup.find('table')
	rows = table.findAll('tr')
	for tr in rows:
	  cols = tr.findAll('td')
	  for td in cols:
	      text = ''.join(td.find(text=True))
	      alert.append(text)
	  all_alerts.append(alert)
	  alert = []
	return all_alerts

def pop_alert(alert):
	pynotify.init("Basic")
	n = pynotify.Notification(alert[2], alert[3] +"   -   " + alert[1])
	n.set_timeout(pynotify.EXPIRES_DEFAULT)
	n.show()


def main():

	html_body = get_html()
	array_of_alerts = get_table(html_body)

	last_alert = array_of_alerts[0]
	pop_alert(last_alert)

	while True:
		html_body = get_html()
		array_of_alerts = get_table(html_body)

		if array_of_alerts[0][2] == last_alert[2]:
			print "no changes"
			time.sleep(interval)
		else:
			pop_alert(array_of_alerts[0])

if __name__ == "__main__":
	main()


