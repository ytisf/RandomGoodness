About
======
This is just a repository of random useful scripts. Some i've written my self, some by my pupils and some where just modified. Credits are given within each code. Each of them is 'not worthy' of their own repository but together they might be useful.

Scripts
==========

## CrestronAirMediaRCE.py
A file with various exploitations of the Crestron AirMedia's AM-100 and AM-101 to make it easier to exploit, utilize and network bridge various devices of this line. 


## GetNanoZip .sh
Automatically downloads, installs and creates an alias within bashrc for nanozip archiving software.

## InfoSecCleaner.js
A small script for GreaseMonkey to remove ads from resources.infosec for better viewing. Too small and unprofessional to upload to UserScripts.

## RandomIPGenerator .py
Will create a bunch of IP addresses based on the rule sets of IPv4. My main use for this is with nmap.

## SudoHoneypot .sh
A honeypot to capture sudo credentials written by a pupil of mine, Barak.

## iptables_BlockAllButFromIsrael .sh
A little script we have released prior to 7th of April 2012 to stop denial of service attacks and block connections from IPs which are not listed as Israel IP addresses. Bear in mind that this will delete all prior iptables rules.

## NetworkMapper .sh
A little script to help locating hosts on the net using arp-scan and then sending it to nmap to save time on your infrastructure pentest.

## KeyLogger 0+1 .c
Not mine but they are useful. Have a few features to add later on...

## CoprimeRandomnessCheck .py
This is based on the fact that in any large set of numbers the distribution between cofactors and coprimes will `lim -> (6/(pi^2))`. Therefore, it will generate 10^6 `long` pairs between 0 and 10^9 and then put them in one of two buckets: coprime or cofactor. After that it will calculate `(6/(pi^2))` and try to evaluate how close they are. **NOT FOR CRYPTO!!!**

## crysknife
crysknife is a simple HTTP 'MiTM' tool. Its original purpose is to help detect malware compromised devices **after** a sinkhole has been created. Hence, nothing fancy or unique. Just want to have this at hand for later. It will save logs to a `recent.log` log file with the requests encoded into base64.

## lazyGrab
This one has some dependncies so its got its own folder. This one just runs over a target file with URLs/DomainNames/IPs and provides screenshots using selenium to save you guys time from manually reviewing nmap scans.


GPL 3
======
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
