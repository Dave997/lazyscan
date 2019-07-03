#!/usr/bin/env python

# -*- coding: utf-8 -*-
#project         :lazy scan
#title           :host_scan.py
#description     :Main point manage host vulnerability assessment modules 
#author          :Davide Ambrosi
#date            :29/05/2019
#version         :0.1
#usage           :python3 host_scan.py
#python_version  :3.6  
#notes           :
#=======================================================================

import sys, os, re
import subprocess
import time
from datetime import datetime

# =======================
#     MENUS FUNCTIONS
# =======================
 
# Main menu
def main_menu():
    os.system('clear')
    print("Host automated vulnerability scanner!")
    print("Type help to show available options")
    
    host = "0.0.0.0"
    command = ""
    verbose = False
    while command != "exit":
        command = input(" >> ")
        
        # == HELP == #
        if command == "help":
            print("Available commands: ")
            print("\t- config \tShow current configuration")
            print("\t- host <ip or hostname> \tSet network address of the target machine (ex: 192.168.1.10 or example.com)")
            print("\t- run \t\tRun the port scan")
            print("\t- run-cve \tRun the CVE scan")
            print("\t- v <true/false> \tVerbose [Default: False]")
            print("\t- exit \t\tCome back to main menu")
            
        #== CONFIG ==#
        elif command == "config":
            print("** Host address: " + str(host))
            print("** Verbose: " + str(verbose))
            
        #== SET HOST ==#
        elif command.split(" ")[0] == "host":  
            try:
                host_tmp = str(command.split(" ")[1])
                os.system("echo \"$(date +\"%H:%M:%S\") Ping " + host_tmp + " to check availability\" >> $host_scan_log")
                
                HOST_UP  = True if os.system("ping -c 1 " + host_tmp + " > /dev/null") is 0 else False
                if HOST_UP:
                    host = str(command.split(" ")[1])
                    os.system("echo \"$(date +\"%H:%M:%S\") Host setted " + str(host) + " \" >> $host_scan_log")
                else:
                    print("Host unreachable!")
                    print("N.B The host address must not contain 'http://' or 'https://'")
                    os.system("echo \"$(date +\"%H:%M:%S\") Host unreachable, not setted!\" >> $host_scan_log")
            except:
                print("Wrong syntax!") 
            
        #== VERBOSE ==#
        elif command.split(" ")[0] == "v":       
            choice = str(command.split(" ")[1]).lower()
            if choice == "true":
                verbose = True
                os.system("echo \"$(date +\"%H:%M:%S\") Verbose mode setted!\" >> $host_scan_log")
            elif choice == "false":
                verbose = False
            else:
                print("Wrong syntax!")                
            
        #== RUN-CVE ==#
        elif command == "run-cve":
            os.system("echo \"$(date +\"%H:%M:%S\") Nmap CVE scan started on " + str(host) + "\" >> $host_scan_log")
            
            sp = subprocess.Popen(['python3', './src/host_scan/modules/nmap_cve_scan.py', str(host)],
                                    shell=False,
                                    stdin=subprocess.PIPE,
                                    stderr=subprocess.PIPE
                                    )

            sp.communicate()
            os.system("echo \"$(date +\"%H:%M:%S\") Nmap CVE scan finished\" >> $host_scan_log")
            
        #== RUN-PORT SCAN ==#
        elif command == "run":
            # initial check
            if host == "0.0.0.0":
                print("ip address must be specified!")
            else:            
                os.system("echo \"$(date +\"%H:%M:%S\") Nmap port scan started on " + str(host) + "\" >> $host_scan_log")
                
                sp = subprocess.Popen(['python3', './src/host_scan/modules/nmap_port_scan.py', str(host)],
                                        shell=False,
                                        stdin=subprocess.PIPE
                                        )

                sp.communicate()
                os.system("echo \"$(date +\"%H:%M:%S\") Nmap port scan finished\" >> $host_scan_log")
                
                # start single port vertical vulnerability scanner
                os.system("echo \"\n$(date +\"%H:%M:%S\") Vertical port scan started on " + str(host) + "\" >> $host_scan_log")
                
                if not verbose:
                    verbose = ""
                sp = subprocess.Popen(['python3', './src/host_scan/manager.py', str(host), "/tmp/nmap_port_out.xml", str(verbose)],
                                        shell=False,
                                        stdin=subprocess.PIPE,
                                        stderr=subprocess.PIPE
                                        )

                sp.communicate()
                os.system("echo \"\n$(date +\"%H:%M:%S\") Vertical port scan finished\" >> $host_scan_log")
        
        #== CLEAR ==#
        elif command == "clear":
            os.system("clear")
            
        #== EXIT ==#
        elif command == "exit":
            exec_menu("exit")
        else:
            print ("Invalid selection, please try again.\n")
            
    return

# Execute menu
def exec_menu(choice):
    ch = choice.lower()
    if ch == '':
        menu_actions['main_menu']()
    else:
        try:
            menu_actions[ch]()
        except KeyError:
            print ("Invalid selection, please try again.\n")
            menu_actions['main_menu']()
    return

# Exit program
def exit():
    os.system("echo \"$(date +\"%H:%M:%S\") Module terminated\" >> $host_scan_log")
    sys.exit()

# =======================
#    MENUS DEFINITIONS
# =======================
 
# Menu definition
menu_actions = {
    'main_menu': main_menu,
    'exit': exit,
}

# =======================
#      MAIN PROGRAM
# =======================
 
# Main Program
if __name__ == "__main__":
    
    os.system("date > $host_scan_log")
    os.system("echo \"Module started:\n\n\" >> $host_scan_log")
    
    # Launch main menu
    main_menu()