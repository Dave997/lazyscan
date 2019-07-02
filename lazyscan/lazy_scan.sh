#! /bin/sh

#    lazy scan
#
#    Application to automate vulnerability assessment through the network
#
#    Author: Davide Ambrosi

OPT=0

##==== FUNCTIONS ====##

banner() { \
    figlet "Lazy scan"

    echo "Welcome in the lazy scan tool, please use this tool only if you have the consent!\n"
    echo "1) Network scan"
    echo "2) Host scan"
    echo "3) Generate Report"
    echo "0) Exit"
}

error() { \
    echo "[\033[0;31mERROR\033[0m] - $1"; 
}

success() { \
    echo "[  \033[32mOK\033[m  ] - $1"
}

##===================##

clear

cur_path=$(pwd)
cd /opt/lazyscan

# export folder variables 
export -p > /tmp/exp1
. ./config/folders_location.conf
. ./config/logs.conf
. ./config/results.conf
. ./config/scanners/wfuzz.conf
export -p > /tmp/exp2

if [ -e $base_output_folder ]; then
    echo "Found an existing result directory $base_output_folder.\n"
    read -rp "It will be overwritten, do you want to proceed? [Y/n]" REPLY

    case $REPLY in
        n|no|N) 
            echo "Goodbye!"
            exit 0
            ;;
        *)  
            rm -rf $base_output_folder
            ;;
    esac
fi

# create all necessary folder and files
diff /tmp/exp1 /tmp/exp2 | sed "s/^.*=//g;/^[0-9]/d;s/'//g" > /tmp/new_stuff.log
for folder in $(cat /tmp/new_stuff.log | grep -v log$ | grep -v '\.\(txt\|csv\|json\)'); do
    mkdir $folder
done
for file in $(cat /tmp/new_stuff.log | grep log$); do
    touch $file
done
for file in $(cat /tmp/new_stuff.log | grep -v log$ | grep '\.\(txt\|csv\|json\)'); do
    touch $file
done


# start the application
date > $lazyscan_log
echo "Application started:\n\n" >> $lazyscan_log

clear
banner

while :; do
    printf "\nSelect an option: "
    read OPT

    case $OPT in
        ## NETWORK SCAN MODULE
        "1")
            echo "$(date +"%H:%M:%S") Network scan module selected" >> $lazyscan_log

            bash -c "cd /opt/lazyscan/; python3 src/network_scan/network_scan.py"

            echo "$(date +"%H:%M:%S") Network scan module ended" >> $lazyscan_log
            clear
            banner
            ;;
        ## HOST SCAN MODULE
        "2")
            echo "$(date +"%H:%M:%S") Host scan module selected" >> $lazyscan_log

            bash -c "cd /opt/lazyscan/; python3 src/host_scan/host_scan.py"

            echo "$(date +"%H:%M:%S") Host scan module ended" >> $lazyscan_log
            clear
            banner
            ;;
        ## REPORT MODULE
        "3")
            echo "$(date +"%H:%M:%S") Report module selected" >> $lazyscan_log

            clear

            if [ $(find $result_folder -type f ! -size 0 | wc -l) -gt 0 ]; then
                [ $(find $result_net_scan_folder -type f ! -size 0 | wc -l) -gt 0 ] && bash -c "cd /opt/lazyscan/; python3 src/report/generate_report_net_scan.py $report_folder_network"
                if [ $? -ne 0 ]; then
                    error "No results file found for network scan!"
                else
                    success "Report for network scan created!"
                fi

                [ $(find $result_host_scan_folder -type f ! -size 0 | wc -l) -gt 0 ] && bash -c "cd /opt/lazyscan/; python3 src/report/generate_report_host_scan.py $report_folder_host"
                if [ $? -ne 0 ]; then
                    error "No results file found for host scan!"
                else
                    success "Report for host scan created!"
                fi
            else
                error "No results found"
            fi

            echo "$(date +"%H:%M:%S") Report module ended" >> $lazyscan_log
            banner
            ;;
        ## EXIT
        "0")
            read -rp "Do you really want to exit? [y/N] " REPLY

            case $REPLY in
                y|yes) 
                    echo "Goodbye!"
                    echo "\n\n$(date +"%H:%M:%S") Application ended!" >> $lazyscan_log
                    cd $cur_path
                    exit 0
                    ;;
                *)  
                    clear
                    banner
                    ;;
            esac
            ;;
        *)
            echo "\033[0;31mERROR\033[0m - Bad input!"; 
            ;;
    esac
done