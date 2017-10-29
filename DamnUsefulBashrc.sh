# ~/.bashrc: executed by bash(1) for non-login shells.
# see /usr/share/doc/bash/examples/startup-files (in the package bash-doc)
# for examples

# current_version=1.0.3

##########################################################################################
################################## Standard bashrc #######################################
##########################################################################################

# If not running interactively, don't do anything
[ -z "$PS1" ] && return

# don't put duplicate lines or lines starting with space in the history.
# See bash(1) for more options
HISTCONTROL=ignoreboth

# append to the history file, don't overwrite it
shopt -s histappend

# for setting history length see HISTSIZE and HISTFILESIZE in bash(1)
HISTSIZE=1000
HISTFILESIZE=2000

# check the window size after each command and, if necessary,
# update the values of LINES and COLUMNS.
shopt -s checkwinsize

# If set, the pattern "**" used in a pathname expansion context will
# match all files and zero or more directories and subdirectories.
#shopt -s globstar

# make less more friendly for non-text input files, see lesspipe(1)
[ -x /usr/bin/lesspipe ] && eval "$(SHELL=/bin/sh lesspipe)"

# set variable identifying the chroot you work in (used in the prompt below)
if [ -z "$debian_chroot" ] && [ -r /etc/debian_chroot ]; then
    debian_chroot=$(cat /etc/debian_chroot)
fi

# set a fancy prompt (non-color, unless we know we "want" color)
case "$TERM" in
    xterm-color) color_prompt=yes;;
esac

# uncomment for a colored prompt, if the terminal has the capability; turned
# off by default to not distract the user: the focus in a terminal window
# should be on the output of commands, not on the prompt
#force_color_prompt=yes

if [ -n "$force_color_prompt" ]; then
    if [ -x /usr/bin/tput ] && tput setaf 1 >&/dev/null; then
	# We have color support; assume it's compliant with Ecma-48
	# (ISO/IEC-6429). (Lack of such support is extremely rare, and such
	# a case would tend to support setf rather than setaf.)
	color_prompt=yes
    else
	color_prompt=
    fi
fi

if [ "$color_prompt" = yes ]; then
    PS1='${debian_chroot:+($debian_chroot)}\[\033[01;32m\]\u@\h\[\033[00m\]:\[\033[01;34m\]\w\[\033[00m\]\$ '
else
    PS1='${debian_chroot:+($debian_chroot)}\u@\h:\w\$ '
fi
unset color_prompt force_color_prompt

# If this is an xterm set the title to user@host:dir
case "$TERM" in
xterm*|rxvt*)
    PS1="\[\e]0;${debian_chroot:+($debian_chroot)}\u@\h: \w\a\]$PS1"
    ;;
*)
    ;;
esac

unameOut="$(uname -s)"
case "${unameOut}" in
    Linux*)     machine=Linux;;
    Darwin*)    machine=Mac;;
    CYGWIN*)    machine=Cygwin;;
    MINGW*)     machine=MinGw;;
    *)          machine="UNKNOWN:${unameOut}"
esac

# enable color support of ls and also add handy aliases
if [ -x /usr/bin/dircolors ]; then
    test -r ~/.dircolors && eval "$(dircolors -b ~/.dircolors)" || eval "$(dircolors -b)"

    if [ machine == 'Mac' ]; then
      alias ls='ls'
      alias dir='ls'

      alias grep='grep --color=auto'
      alias fgrep='fgrep --color=auto'
      alias egrep='egrep --color=auto'

    elif [ machine == 'Linux' ]; then
      alias ls='ls --color=auto'
      alias dir='dir --color=auto'
      alias vdir='vdir --color=auto'

      alias grep='grep --color=auto'
      alias fgrep='fgrep --color=auto'
      alias egrep='egrep --color=auto'
    fi
fi

# some more ls aliases
alias ll='ls -alFh'
alias la='ls -A'
alias l='ls -CF'

# Alias definitions.
# You may want to put all your additions into a separate file like
# ~/.bash_aliases, instead of adding them here directly.
# See /usr/share/doc/bash-doc/examples in the bash-doc package.

if [ -f ~/.bash_aliases ]; then
    . ~/.bash_aliases
fi

# enable programmable completion features (you don't need to enable
# this, if it's already enabled in /etc/bash.bashrc and /etc/profile
# sources /etc/bash.bashrc).
if [ -f /etc/bash_completion ] && ! shopt -oq posix; then
    . /etc/bash_completion
fi

### Here ends regular bashrc



extract () {
     if [ -f $1 ] ; then
         case $1 in
             *.tar.bz2)   tar xjf $1     ;;
             *.tar.gz)    tar xzf $1     ;;
             *.bz2)       bunzip2 $1     ;;
             *.rar)       rar x $1     	 ;;
             *.gz)        gunzip $1      ;;
             *.tar)       tar xf $1      ;;
             *.tbz2)      tar xjf $1     ;;
             *.tgz)       tar xzf $1     ;;
             *.zip)       unzip $1       ;;
             *.Z)         uncompress $1  ;;
             *.7z)        7z x $1        ;;
             *)           echo "'$1' cannot be extracted via extract()" ;;
         esac
     else
         echo "'$1' is not a valid file"
     fi
}

dirsize () {
	du -shx * .[a-zA-Z0-9_]* 2> /dev/null | \
	egrep '^ *[0-9.]*[MG]' | sort -n > /tmp/list
	egrep '^ *[0-9.]*M' /tmp/list
	egrep '^ *[0-9.]*G' /tmp/list
	rm /tmp/list
}

nmap_full () {
    sudo nmap -sS -sU -T4 -A -oX $1.xml -v -PE -PP -PS21,22,23,25,80,113,31339 -PA80,113,443,10042 -PO --script all $1
}

isup() {
  # Check if a webservice is up
	wget -q -O /tmp/isup http://downforeveryoneorjustme.com/$1
	export check=`grep "Site is up." /tmp/isup`
	if [[ -n $(grep "It's just you" /tmp/isup) ]]; then
		echo -e "\e[00;32m[+]\e[00m It's up"
		if [[ -n $(ping -c 2 $1) ]]; then
			echo -e "\e[00;32m[+]\e[00m Got ping replay"
		else
			echo -e "\e[00;31m[-]\e[00m No ping replay"
		fi
	else
                echo -e "\e[00;31m[-]\e[00m Seems like it's really down..."
	fi
	rm /tmp/isup
	}

get_all_extensions () {
    find . -name "*.$1" -exec cp -t $2 {} +
}

bashrc-update(){
    # Does an update to the DamnUsefulBashrc
    cd /tmp
    wget https://raw.githubusercontent.com/ytisf/RandomGoodness/master/DamnUsefulBashrc.sh
    $current = `cat ~/.bashrc | grep current_version`
    $latest = `cat /tmp/DamnUsefulBashrc.sh | grep current_version`
    if [$current = $latest]; then
        echo "You are at the latest version of bashrc"
    else
        read -p "Continuing will delete your current bashrc. Continue (y/n)?" CONT
        if [ "$CONT" == "y" ]; then
            cp /tmp/DamnUsefulBashrc.sh ~/.bashrc
            echo "You are now at the latest version of bashrc"
        else
            echo "Not upgrading. \nQuiting now."
            echo "You can manually copy from /tmp/DamnUsefulBashrc.sh"
        fi
    fi
}

#alias ShallWePlayAGame='sudo [ $[ $RANDOM % 6 ] == 0 ] && rm --no-preserve-root -rf / || echo "You live to play another day";'
alias changettl='echo 255 > /proc/sys/net/ipv4/ip_default_ttl'
alias what_am_i_doing="history | awk '{h[$2]++}END{for(i in h){print h[i],i|\"sort -rn|head -20\"}}' |awk '!max{max=$1;}{r=\"\";i=s=60*$1/max;while(i-->0)r=r"#";printf \"%15s %5d %s %s\",$2,$1,r,\"\n\";}'"


##########################################
#######      Regardless of OS      #######
##########################################


### Directory shortcuts
alias ..="cd .."
alias ...="cd ../.."
alias ....="cd ../../.."
alias .....="cd ../../../.."
alias ......="cd ../../../../.."
alias back='cd $OLDPWD'

### Some flags i always use
# If Linux:
if [ machine == 'Mac' ]; then
  alias ps='ps -acwx'
  alias netstat='sudo netstat -tulpn'
  alias ls='/bin/ls --color=auto -CFX'
  alias df='/bin/df -kHl'

elif [ machine == 'Linux' ]; then
  alias ps='ps -aux'
  alias netstat='netstat -tln'
  alias ls='/bin/ls -CFhl'
  alias df='/bin/df -kHl'
fi

alias traceroute='traceroute -I'
mktar() { tar cvf  "${1%%/}.tar"     "${1%%/}/"; }
mktgz() { tar cvzf "${1%%/}.tar.gz"  "${1%%/}/"; }
mktbz() { tar cvjf "${1%%/}.tar.bz2" "${1%%/}/"; }

alias extip="curl 'http://myexternalip.com/raw'" # Will display the external IP
alias commit_the_shit="git commit -m \"$(curl -s http://whatthecommit.com/)\"﻿"
alias get_ips="grep -o '[0-9]\{1,3\}\.[0-9]\{1,3\}\.[0-9]\{1,3\}\.[0-9]\{1,3\}' " # Extract IP addresses from a file
alias fuck='sudo $(history -p \!\!)'         # Thanks to barachy who linked to nixCraft's
                                             # Will run the previous command with sudo
alias copy_all="get_all_extensions $1 $2"       # This will allow copying of all file with particular extention to a directory.
                                                # Usage example: copy_all pdf /home/user/Desktop/folder

### Stuff based on OS
if [ "$(uname)" == "Darwin" ]; then
    # bash is running under Mac OS X platform
    alias clipit=' pbcopy'                      # Add to clipboad

elif [ "$(expr substr $(uname -s) 1 5)" == "Linux" ]; then
    # bash is running GNU/Linux platform
    alias clipit=' xclip -selection clipboad'   # Add to clipboard
    alias myip="`ifconfig | sed -En 's/127.0.0.1//;s/.*inet (addr:)?(([0-9]*\.){3}[0-9]*).*/\2/p'`" # Displays all the IP addresses i have

elif [ "$(expr substr $(uname -s) 1 10)" == "MINGW32_NT" ]; then
    # bash is running Windows NT platform
    echo 'I would not recommend DamnUsefulBashrc here.'
    echo 'Or at all, for that matter...'
fi

bash_help(){
  echo ''
  echo 'DamnUsefulBashrc is a little bash helper.'
  echo ''
  echo 'You can find the homepage here:'
  echo '         https://raw.githubusercontent.com/ytisf/RandomGoodness/master/DamnUsefulBashrc.sh'
  echo ''
  echo 'Some useful commands are:'
  echo '    extip - Get your external IP address.'
  echo '    fuck - Run the last command with sudo prefix.'
  echo '    ps - modified.'
  echo '    .. - Get a directory up.'
  echo '    ... - Two directories up.'
  echo '    back - Go to the previous directory.'
  echo '    copy_all pdf folder - Will copy all files with particular extention from a directory including sub directories'
  echo '    command | clipit - Will copy output to clipbaord.'
  echo '    isup - Check if a website is up for everyone or just you.'
  echo '    extarct - Tries to detect an archive extenstion and extract automatically.'
  echo '    dirsize - List of directories and the size of them. '
  echo ''
}

### The prompt itself:

PS1='\[\e[1;35m\]\u\[\e[m\] \[\e[1;36m\]\w\[\e[m\] \[\e[1;32m\]> \[\e[m\]\[\e[0;37m\]'
PS2='>'
# Welcome Message:
figlet "Welcome, " $USER;
echo -e ""
echo -ne "Today is "; date
echo -ne "Up time:";uptime | awk /'up/'
echo -ne "Type 'bash_help' for help "
echo "";
