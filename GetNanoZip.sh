#!/bin/bash

if [[ $EUID -ne 0 ]]; then
   echo "This script must be run as root" 1>&2
   exit 1
fi

bold=`tput bold`
normal=`tput sgr0`

clear
echo ''
echo ' ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
echo ''
echo '                     NanoZip Building Script'
echo ''
echo '      Built by Yuval (tisf) Nativ of the See-Security Group'
echo '                 http://www.hackingdefined.org'
echo ''
echo ' ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
echo ''

mkdir /usr/bin/nz
cd /usr/bin/nz
wget --quiet http://www.nanozip.net/nanozip-0.09a.linux64.zip
echo -e "\e[00;32m[+]\e[00m Get Zip."
unzip nanozip-0.09a.linux64.zip
echo -e "\e[00;32m[+]\e[00m Decompressed."
echo "alias nza='/usr/bin/nz/./nz a -cO -m1.2g'" >> ~/.bashrc
echo "alias nze='/usr/bin/nz/./nz x'" >> ~/.bashrc
echo -e ''
echo -e "\e[00;32m[+]\e[00m Done!"
echo -e "Use '${bold}nza archive_name filename1 filename2${normal}' to compress."
echo -e "Use '${bold}nze archivename${normal}' to extract."
echo -e "Reload terminal to use the shortcuts... and Be good!"
echo -e ""
