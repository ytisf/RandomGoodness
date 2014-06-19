#!/bin/bash

banner(){
	echo "###################################"
	echo "###################################"
	echo "#####  Basic Ubuntu Upgrader  #####"
	echo "###################################"
	echo "###################################"
	echo ""
	echo "WARNING: This will make your ubuntu AWESOME!"
	echo "This script will install and compile all of the things."
	echo "Notice that you need to change metasploit's DB password"
	echo "which is set to default to '123456'"
}


check_if_root(){

	#	This function checks if it runs as root or exits

	if [ "$(id -u)" != "0" ]; then
		echo "Please execute this script as root"
		exit 1
	fi	
}

check_internet_connection(){
	for interface in $(ls /sys/class/net/ | grep -v lo);
	do
  		if [[ $(cat /sys/class/net/$interface/carrier) = 1 ]]; then OnLine=1; fi
	done
	if ! [ $OnLine ]; then echo "Not Online" > /dev/stderr; exit; fi
}

prompt(){
	read -n1 -p "This will do a complete system update and overrun files on the machine. Continue? (y/n) "
	echo
	[[ $REPLY = [yY] ]] && echo "Continuing" || { echo "You didn't answer yes, so i'll go now..."; exit 1; }
}

update_system(){
	sudo apt-get update
	sudo apt-get -y upgrade
	sudo apt-get -y dist-upgrade
}

create_directories(){
	# Installs basic working directories
	mkdir /tmp/remove_me_later
	mkdir ~/Dev
}

install_basics(){
	# Installing things needed for general installtion
	sudo apt-get -y install git subversion build-essential
	sudo apt-get -y install gcc libssl-dev python2.7-dev ruby1.9.3
	sudo apt-get -y install rar gparted p7zip-full figlet
}

install_extra_fun(){
	sudo apt-get -y install vlc ubuntu-restricted-extras 
	sudo apt-get -y install filezilla firefox gufw
	sudo apt-get -y install brasero keepass2 geany 
	sudo apt-get -y install torsocks vidalida tor
}

install_hacking(){
	sudo apt-get -y install wireshark tcpdump tcpflow ettercap-text-only sslstrip dsniff 
	sudo apt-get -y install socks4-clients traceroute
}

getNcompileNmap(){
	cd /opt/
	wget http://nmap.org/dist/nmap-6.46.tar.bz2
	tar xfv nmap-6.46.tar.bz2
	cd nmap-6.46
	./configure
	make
	sudo make install
}

metasploit(){
	cd /tmp/remove_me_later
	git clone https://github.com/darkoperator/MSF-Installer
	cd MSF-Installer
	chmod +x msf_install.sh
	sudo ./msf_install -p 123456 -i
}

fix_bashrc(){
	cd ~
	wget -O .bashrc https://raw.githubusercontent.com/ytisf/RandomGoodness/master/DamnUsefulBashrc.sh
}

get_sqlmap(){
	cd ~/Dev
	git clone https://github.com/sqlmapproject/sqlmap.git sqlmap-dev
	return 0
}

get_joomscan(){
	 sudo apt-get -f install libwww-perl libwww-mechanize-perl
	 wget "http://downloads.sourceforge.net/project/joomscan/joomscan/2012-03-10/joomscan-latest.zip?r=http%3A%2F%2Fsourceforge.net%2Fprojects%2Fjoomscan%2F%3Fsource%3Ddlp&ts=1368806935&use_mirror=ncu" -O joomscan-latest.zip
	 unzip joomscan-latest.zip
	 cd joomscan
	 chmod +x joomscan.pl
	 perl joomscan.pl update
}

install_fierce(){
	cd ~/Dev
	mkdir fierce
	cd fierce
	wget http://ha.ckers.org/fierce/fierce.pl
	wget http://ha.ckers.org/fierce/hosts.txt
	return 0
}

dont_touch_me(){
	iptables -I INPUT -i eth0 -p icmp -s 0/0 -d 0/0 -j DROP
	iptables -I INPUT -i wlan0 -p icmp -s 0/0 -d 0/0 -j DROP
	echo 1 > /proc/sys/net/ipv4/icmp_echo_ignore_all
	iptables -P INPUT DROP
	iptables -P FORWARD DROP
	iptables -A INPUT -i lo -j ACCEPT
	iptables -A OUTPUT -o lo -j ACCEPT
	iptables -A INPUT -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT
}

get_tor_broswer(){
	cd ~/Dev
	wget https://www.torproject.org/dist/torbrowser/3.6.2/tor-browser-linux64-3.6.2_en-US.tar.xz
	tar xfv tor-browser-linux64-3.6.2_en-US.tar.xz

}

clean_everything(){
	rm -rf /tmp/remove_me_later
	rm -rf /opt/nmap-6.46.tar.bz2
}

banner
check_if_root
check_internet_connection
prompt
dont_touch_me
create_directories
update_system
fix_bashrc
install_basics
install_extra_fun
install_hacking
getNcompileNmap
metasploit
get_sqlmap
get_joomscan
clean_everything
