#!/bin/bash
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
#              Automatic Network Reconnasaince Tool
#
#      Build by Yuval (tisf) Nativ and Bar (ba7a7chy) Hofesh
#                   of the See-Security Group
#
#                     yuval@see-security.com
#
#                  http://www.see-security.com
#                 http://www.hackingdefined.org
#
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


if [[ $EUID -ne 0 ]]; then
   echo ''
   echo 'Error:   This script must be run as root' 1>&2
   echo ''
   exit 1
fi

clear

PKG_OK=$(dpkg-query -W --showformat='${Status}\n' arp-scan|grep "install ok installed")
echo 'Checking for arp-scan: '$PKG_OK
if [ "" == "$PKG_OK" ]; then
	echo "Resolving dependencies, please wait."
	sudo apt-get --force-yes --yes install arp-scan
fi

PKG_OK=$(dpkg-query -W --showformat='${Status}\n' nmap|grep "install ok installed")
echo 'Checking for nmap: '$PKG_OK
if [ "" == "$PKG_OK" ]; then
	echo "Resolving dependencies, please wait."
	sudo apt-get --force-yes --yes install nmap
fi

PKG_OK=$(dpkg-query -W --showformat='${Status}\n' tcpdump|grep "install ok installed")
echo 'Checking for tcpdump: '$PKG_OK
if [ "" == "$PKG_OK" ]; then
	echo "Resolving dependencies, please wait."
	sudo apt-get --force-yes --yes install tcpdump
fi

PKG_OK=$(dpkg-query -W --showformat='${Status}\n' nbtscan|grep "install ok installed")
echo 'Checking for nbtscan: '$PKG_OK
if [ "" == "$PKG_OK" ]; then
	echo "Resolving dependencies, please wait."
	sudo apt-get --force-yes --yes install nbtscan
fi

clear

echo ""
echo ' ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
echo ' ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
echo ' ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
echo ''
echo '    .__.................__......................_._.........'
echo '    / _\.___..___....../ _\.___..___._..._._.__(_) |_._..._.'
echo '    \ \./ _ \/ _ \_____\ \./ _ \/ __| |.| |  __| | __| |.| |'
echo '    _\ \  __/  __/_____|\ \  __/ (__| |_| | |..| | |_| |_| |'
echo '    \__/\___|\___|.....\__/\___|\___|\__,_|_|..|_|\__|\__, |'
echo '    ..................................................|___/.'
echo ''
echo '              Automatic Network Reconnasaince Tool'
echo ''
echo '      Build by Yuval (tisf) Nativ and Bar (ba7a7chy) Hofesh'
echo '                   of the See-Security Group'
echo ''
echo '                  http://www.see-security.com'
echo '                 http://www.hackingdefined.org'
echo ''
echo ' ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
echo ' ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
echo ' ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
echo ""
echo "What is the project's name: "
read company
echo "Creating directory structure for $company..."
mkdir $company-`date +%Y-%m-%d`
cd $company-`date +%Y-%m-%d`
echo '' > EventLog.log
echo 'Project '$company' initiated at ' `date +%Y-%m-%d::%H:%S:%N` > EventLog.log
echo ""
interfaces=$(/sbin/ifconfig |grep -e ^[a-z] |  awk '{ printf $1 " "}')
echo "Your network adapters and their configuration:"
	for i in $interfaces
	do
	    addr=$(/sbin/ifconfig $i | grep 'inet addr:' | cut -d: -f2 | awk '{ print $1}')
	    echo "$i : $addr"
	done
echo "Please choose network adapter (eth0/eth1/wlan0/wlan1): "
read netadpt
echo "    Network adapted choosen:" `/sbin/ifconfig $netadapt | grep 'inet addr:' | cut -d: -f2 | awk '{ print $1}'` >> EventLog.log
echo ""
echo "Please choose scan type:"
echo "    [1]  I have plenty of time here, Give me the comprehensive one."
echo "    [2]  Make it a quick one. (arp+basic nmap)"
echo "    [3]  Just give me live hosts and solve their MAC address. "
echo "    [4]  Forget about the scanning and give me something fun!. "
read scantype
echo "    Scan type choosen: $scantype" >> EventLog.log
echo "" >> EventLog.log
echo ""
echo ""
echo "The project $company will start now. Please wait as information appears on screen."
echo ""
echo ""
echo ""
echo 'Scan on '$company' initiated at ' `date +%Y-%m-%d::%H:%S:%N` 2>&1 | tee -a EventLog.log
tcpdump -c 50000 -i $netadpt -w $company.cap &> /dev/null &
echo '' 2>&1 | tee -a EventLog.log
echo '     '`date +%Y-%m-%d::%H:%S:%N` ' - Started listener. Information logged to '$company'.cap' 2>&1 | tee -a EventLog.log
echo '     '`date +%Y-%m-%d::%H:%S:%N` ' - ARP scan initiated and saved to file.' 2>&1 | tee -a EventLog.log
arp-scan -I $netadpt -l > arp-scan.txt
echo '     '`date +%Y-%m-%d::%H:%S:%N` ' - ARP scan done. '`cat arp-scan.txt | grep responded | awk '{print $12}'` ' hosts found!' 2>&1 | tee -a EventLog.log
echo '     '`date +%Y-%m-%d::%H:%S:%N` ' - Now extracting IP addresses from file...' 2>&1 | tee -a EventLog.log
grep -Eo '([0-9]{1,3}\.){3}[0-9]{1,3}' arp-scan.txt > arp_ip_extracted.tmp
echo '     '`date +%Y-%m-%d::%H:%S:%N` ' - '`cat arp-scan.txt | grep responded | awk '{print $12}'` ' IPs extracted.' 2>&1 | tee -a EventLog.log
echo '     '`cat arp_ip_extracted.tmp` 2>&1 | tee -a EventLog.log

case "$scantype" in

1)  N=0
    counter=`wc -l "arp_ip_extracted.tmp" | awk '{print $1'}`
    cat arp_ip_extracted.tmp | while read IPADDR ; do
    	    N=$((N+1))
    	    echo '     '`date +%Y-%m-%d::%H:%S:%N` ' - Now proceeding to host '$N' out of '`cat arp-scan.txt | grep responded | awk '{print $12}'`'.' 2>&1 | tee -a EventLog.log
    	    echo '     '`date +%Y-%m-%d::%H:%S:%N` ' - Starting scan for: '`echo $IPADDR` '...' 2>&1 | tee -a EventLog.log
   	    nmap -Pn -T4 -PE -sV -PS22,25,80 -PA21,23,80,3389 $IPADDR >> $IPADDR.log
	    nbtscan -hv $IPADDR >> $IPADDR.log
    	    echo '     '`date +%Y-%m-%d::%H:%S:%N` ' - Scan for '`echo $IPADDR` ' completed and documented in '$IPADDR'.log' 2>&1 | tee -a EventLog.log
    done
    ;;
2)  N=0
    counter=`wc -l "arp_ip_extracted.tmp" | awk '{print $1'}`
    cat arp_ip_extracted.tmp | while read IPADDR ; do
    	    N=$((N+1))
    	    echo '     '`date +%Y-%m-%d::%H:%S:%N` ' - Now proceeding to host '$N' out of '`cat arp-scan.txt | grep responded | awk '{print $12}'`'.' 2>&1 | tee -a EventLog.log
    	    echo '     '`date +%Y-%m-%d::%H:%S:%N` ' - Starting scan for: '`echo $IPADDR` '...' 2>&1 | tee -a EventLog.log
    	    nmap -Pn $IPADDR >> $IPADDR.log
	    nbtscan -hv $IPADDR >> $IPADDR.log
    	    echo '     '`date +%Y-%m-%d::%H:%S:%N` ' - Scan for '`echo $IPADDR` ' completed and documented at '$IPADDR'.log' 2>&1 | tee -a EventLog.log
    done
    ;;
3)  echo  "Recon endded."
    ;;
4)  firefox 9gag.com
    ;;
*) echo "Exception. Will now Quit."
   ;;
esac

clear
echo ''
echo '     Killing tcpdump....'
pkill tcpdump
echo '     Scan completed at '`date +%Y-%m-%d::%H:%S:%N` ' .' 2>&1 | tee -a EventLog.log
echo '     A total of '`cat arp-scan.txt | grep responded | awk '{print $12}'`' hosts scanned.'
echo '     To view log see EventLog.log file.'
echo '     To view scan result of nmap go to nmap.log .'
echo '     Bee good :) .'
echo ''
