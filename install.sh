#!/bin/sh

#    Script for lazy scan installation
#
#    Author: Davide Ambrosi

PKT_MNG="" # supported packet manager
OS=""      # current running os

##==== FUNCTIONS ====##

error() { \
    clear; 
    echo "\033[0;31mERROR\033[0m - $1"; 
    exit 1;
}

success() { \
    echo "[ \033[32mOK\033[m  ] - $1"
}

check_install() { \
    which $1 > /dev/null 2>&1
    if [ $? -ne 0 ]; then
        $PKT_MNG install -y $1 || error "Unable to install $1"
    fi
}

check_install() { \
    which $1 > /dev/null 2>&1
    if [ $? -ne 0 ]; then
        $PKT_MNG install -y $1 || error "Unable to install $1"
    fi
}

check_install_python() { \
    python3 -c "import $2" > /dev/null 2>&1
    if [ $? -ne 0 ]; then
        #$PKT_MNG install -y "python-$1" || error "Unable to install python-$1"
        pip3 install $1 || error "Unable to install $1 with pip \nTry with $PKT_MNG install python3-pip"
    fi
}

check_err() { \
    which $1 > /dev/null 2>&1
    if [ $? -ne 0 ]; then
        echo "\033[0;31mERROR\033[0m: $1 not found! Please check the installation.\n"
        exit 0;
    fi
} 
##===================##

echo "Welcome in the laz-webscan installer!"
echo "\nThe following packages will be installed:\nipcalc wad droopescan figlet git nikto wfuzz whatweb smbclient enum4linux python-bs4 python3-bs4 sqlmap arp-scan nmap aquatone BeautifulSoup wpscan joomscan searchsploit nmap-vulners vulscan pandoc texlive-latex-extra lazyscan\n"
read -rp "Do you agree? [Y/n] " REPLY

case $REPLY in
    n|no) 
        exit 0
        ;;
    Y|yes|y) 
        ;;
    "") 
        ;;
    *)  
        echo "Option not recognized!"
        exit 1
        ;;
esac

#* GET RUNNING OS 
if [ -f /etc/os-release ]; then
    # systemd
    . /etc/os-release
    OS=$NAME
elif type lsb_release >/dev/null 2>&1; then
    # linuxbase.org
    OS=$(lsb_release -si)
elif [ -f /etc/lsb-release ]; then
    # For some versions of Debian/Ubuntu without lsb_release command
    . /etc/lsb-release
    OS=$DISTRIB_ID
elif [ -f /etc/debian_version ]; then
    # Older Debian/Ubuntu/etc.
    OS=Debian
else
    # Fall back to uname, e.g. "Linux <version>", also works for BSD, etc.
    OS=$(uname -s)
fi

case $OS in 
    Ubuntu|Debian|"Kali GNU/Linux"|"Parrot GNU/Linux")
        PKT_MNG="apt"
        ;;
    Fedora)
        PKT_MNG="dnf"
        ;;
    *)
        echo "\033[0;31mERROR\033[0m - OS ($OS) Not supported!"
        exit 0
        ;;
esac

$PKT_MNG -y update || error "Are you sure you're running this script as the root user?"

# install required packages
check_err "python3"
check_err "python2"
check_err "pip3"
check_err "pip2"
check_install_python "ipcalc" "ipcalc"
check_install_python "wad" "wad"
check_install_python "droopescan" "droopescan"
check_install "figlet"
check_install "git"
check_install "nikto"
check_install "wfuzz"
check_install "whatweb"
check_install "smbclient"
check_install "python-bs4"
check_install "python3-bs4"
check_install "sqlmap"
check_install "arp-scan"
check_install "nmap"
check_install "pandoc"
check_install "texlive-latex-extra"

# no sudo password for arp-scan
user=$(whoami)
host=$(hostname)
echo "$user     $host=(root) NOPASSWD: /usr/sbin/arp-scan" >> /etc/sudoers

# install aquatone
which aquatone > /dev/null 2>&1
if [ $? -ne 0 ]; then
    bash -c "cd /tmp; wget https://github.com/michenriksen/aquatone/releases/download/v1.7.0/aquatone_linux_amd64_1.7.0.zip; unzip aquatone_linux_amd64_1.7.0.zip"
    mv /tmp/aquatone /usr/local/bin/
fi

# install xsser
pip2 install BeautifulSoup
which xsser > /dev/null 2>&1
if [ $? -ne 0 ]; then
    bash -c "cd /tmp; wget https://xsser.03c8.net/xsser/xsser_1.7-1_amd64.deb; dpkg -i xsser_1.7-1_amd64.deb"
fi

# installing cms scanners
    #wordpress
which wpscan > /dev/null 2>&1
if [ $? -ne 0 ]; then
    gem install wpscan
    wpscan --update
fi
    #joomla 
if [ ! -e /opt/joomscan ]; then 
    git clone https://github.com/rezasp/joomscan.git /opt/joomscan
    perl /opt/joomscan/joomscan.pl --update
else    
    perl /opt/joomscan/joomscan.pl --update
fi

# download a dictionary for wfuzz
bash -c "cd /usr/share/wfuzz/wordlist/general/; curl -O https://raw.githubusercontent.com/danielmiessler/SecLists/master/Discovery/Web-Content/Common-PHP-Filenames.txt"

# install exploit db
which searchsploit > /dev/null 2>&1
if [ $? -ne 0 ]; then
    git clone https://github.com/offensive-security/exploitdb.git /opt/exploitdb
    sed 's|path_array+=(.*)|path_array+=("/opt/exploitdb")|g' /opt/exploitdb/.searchsploit_rc > ~/.searchsploit_rc
    ln -sf /opt/exploitdb/searchsploit /usr/local/bin/searchsploit
fi
searchsploit -u #this process sometimes it gets stuck during the update

# istall nmap cve detectors
bash -c "cd /usr/share/nmap/scripts/;\
[ -e nmap-vulners ] || git clone https://github.com/vulnersCom/nmap-vulners.git;\
[ -e vulscan ] || git clone https://github.com/scipag/vulscan.git;\
chmod +x vulscan/utilities/updater/updateFiles.sh;\
./vulscan/utilities/updater/updateFiles.sh"

# Creating symbolic link
cp -r lazyscan /opt/ && success "Directory in opt/ created!" || error "Unable to create directory in opt/"
chmod +x /opt/lazyscan/lazy_scan.sh
ln -s /opt/lazyscan/lazy_scan.sh /usr/local/bin/lazyscan

success "Finish! Now you can type lazyscan in your terminal to run the application!"