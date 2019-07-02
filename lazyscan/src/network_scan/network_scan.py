#!/usr/bin/env python

# -*- coding: utf-8 -*-
#project         :lazy scan
#title           :network_scan.py
#description     :Main point manage host discovery modules 
#author          :Davide Ambrosi
#date            :27/05/2019
#version         :0.1
#usage           :python3 network_scan.py
#python_version  :3.6  
#=======================================================================

import sys, os, re
import subprocess
import time
from datetime import datetime

# Main definition - constants
menu_actions  = {}  
 
# =======================
#     MENUS FUNCTIONS
# =======================
 
# Main menu
def main_menu():
    os.system('clear')
    
    print ("Host Discovery,\n")
    print ("Please choose the discovery method to start:")
    print ("1. Ping Sweep")
    print ("2. ARP scan")  
    # print ("3. 0Trace / Service traceroute")  # https://jon.oberheide.org/0trace/ 
    print ("\n0. Quit")
    choice = input(" >>  ")
    exec_menu(choice)
 
    return
 
# Execute menu
def exec_menu(choice):
    os.system('clear')
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
 
# Menu 1
def ping_sweep_menu():
    
    os.system("echo \"$(date +\"%H:%M:%S\") Ping sweep menu' selected\" >> $network_scan_log")
    print ("Ping sweep! (Type help to show all possible commands)\n")
    
    net="0.0.0.0/0"
    command = ""
    threads = 1
    while command != "exit":
        command = input(" >> ")
        
        # == HELP == #
        if command == "help":
            print("Available commands: ")
            print("\t- config \tShow current configuration")
            print("\t- set <ip/mask> \tSet network address to scan (ex: 192.168.1.0/24)")
            print("\t- run \t\tRun the scan")
            print("\t- T \t\tNumber of threads, max 5 (default: 1)")
            print("\t- exit \t\tCome back to main menu")
            
        # == CONFIG == #
        elif command == "config":
            print("** Network address: " + net)
            print("** Threads: " + str(threads))
            
        # == SET IP == #
        elif command.split(" ")[0] == "set":       
            ip_reg = re.compile("^([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])\.([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])\.([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])\.([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])\/([0-9]{1,2})$")     
            try:
                if ip_reg.match( command.split(" ")[1] ):
                    net = command.split(" ")[1]
                    os.system("echo \"$(date +\"%H:%M:%S\") Setted network " + str(net) + "\" >> $network_scan_log")
                else:
                    print("ERROR: IP address not recognized! (ex: 192.168.1.0/24)")
            except:
                print ("Invalid syntax!.\n")
                
        # == SET THREADS == #
        elif command.split(" ")[0] == "T":   
            try:
                if int(command.split(" ")[1]) < 1 or int(command.split(" ")[1]) > 5:
                    print("ERROR: The number of threads must be an integer between 1 and 5")
                else:
                    threads = int(command.split(" ")[1])
                    os.system("echo \"$(date +\"%H:%M:%S\") Setted " + str(threads) + " threads\" >> $network_scan_log")
            except:
                print ("Invalid syntax!.\n")
        
        # == RUN == #
        elif command == "run":
            if net == "0.0.0.0/0":
                print("Please set the network address!")
            else:
                os.system("echo \"$(date +\"%H:%M:%S\") Ping sweep started on " + str(net) + " with " + str(threads) + " threads\" >> $network_scan_log")
                
                if threads == 1:
                    ping = subprocess.Popen(['python3', './src/network_scan/modules/ping_sweep.py', str(net)],
                                            shell=False,
                                            stdin=subprocess.PIPE
                                            )
                else: 
                    ping = subprocess.Popen(['python3', './src/network_scan/modules/ping_sweep_multithread.py', str(net), str(threads)],
                                            shell=False,
                                            stdin=subprocess.PIPE,
                                            stderr=subprocess.PIPE
                                            )
                ping.communicate()
                
                os.system("echo \"$(date +\"%H:%M:%S\") Ping sweep finished\" >> $network_scan_log")
                
        #== CLEAR ==#
        elif command == "clear":
            os.system("clear")
        
        # == EXIT == #
        elif command == "exit":
            os.system("echo \"$(date +\"%H:%M:%S\") Ping sweep module terminated\" >> $network_scan_log")
            exec_menu(str(9))
        else:
            print ("Invalid selection, please try again.\n")
    return
 
# Menu 2
def arp_scan_menu():
    os.system("echo \"$(date +\"%H:%M:%S\") arp-scan menu' selected\" >> $network_scan_log")
    print ("ARP scan! (Type help to show all possible commands)\n")
    
    # get current network interface
    net_interface = subprocess.Popen(['ip route | grep -i "default via" | cut -d " " -f 5 | head -n 1'],
                             shell=True,
                             stdin=subprocess.PIPE,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE
                             )
    net_interface = net_interface.communicate()[0].decode()
    if net_interface.endswith("\n") or net_interface.endswith("\r"): net_interface=net_interface[:-1] #remove new line character
    
    net="0.0.0.0/0"
    command = ""
    while command != "exit":
        command = input(" >> ")
        
        # == HELP == #
        if command == "help":
            print("Available commands: ")
            print("\t- config \t\t\tShow current configuration")
            print("\t- set <ip/mask> \t\tSet network address to scan (ex: 192.168.1.0/24)")
            print("\t- set_interface <network interface> \tSet network interface (ex: eth0)")
            print("\t- run \t\t\t\tRun the scan")
            print("\t- exit \t\t\t\tCome back to main menu")
            
        # == CONFIG == #    
        elif command == "config":
            print("** Network address: " + net)
            print("** Network Interface: " + net_interface)
            
        # == SET IP == #
        elif command.split(" ")[0] == "set":       
            ip_reg = re.compile("^([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])\.([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])\.([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])\.([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])\/([0-9]{1,2})$")     
            try:
                if ip_reg.match( command.split(" ")[1] ):
                    net = command.split(" ")[1]
                    os.system("echo \"$(date +\"%H:%M:%S\") Setted network " + str(net) + "\" >> $network_scan_log")
                else:
                    print("ERROR: IP address not recognized! (ex: 192.168.1.0/24)")
            except:
                print ("Invalid syntax!.\n")
                
        # == SET INTERFACE == #
        elif command.split(" ")[0] == "set_interface":
            try:
                interface = command.split(" ")[1]

                # get a list of all available interfaces
                net_interface_list = subprocess.Popen(["ip link show | cut -d \" \" -f 2 | sed '/^$/d' | awk '{gsub(\":\", \"\");print}'"],
                                shell=True,
                                stdin=subprocess.PIPE,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE
                                )
                net_interface_list = net_interface_list.communicate()[0].decode().split("\n")
                if any(str(interface) in i for i in net_interface_list):
                    print("Network interface switched: %s -> %s" %(net_interface, interface))
                    net_interface = interface
                    os.system("echo \"$(date +\"%H:%M:%S\") Setted interface " + str(net_interface) + "\" >> $network_scan_log")
                else:
                    print("Interface not found!")
            except:
                print ("Invalid syntax!.\n")
        
        # == RUN == #
        elif command == "run":
            if net == "0.0.0.0/0":
                print("Please set the network address!")
            else:  
                #get current date time to create unique name
                os.system("echo \"$(date +\"%H:%M:%S\") arp-scan started on " + str(net) + " from interface " + str(net_interface) + "\" >> $network_scan_log")
                
                arp = subprocess.Popen(['python3', './src/network_scan/modules/arp_scan.py', str(net), str(net_interface)],
                                        shell=False,
                                        stdin=subprocess.PIPE,
                                        stderr=subprocess.PIPE
                                        )
                arp.communicate()
                os.system("echo \"$(date +\"%H:%M:%S\") arp-scan finished\" >> $network_scan_log")
                
        # == EXIT == #
        elif command == "exit":
            exec_menu(str(9))
        else:
            print ("Invalid selection, please try again.\n")
    return
 
# Back to main menu
def back():
    menu_actions['main_menu']()
 
# Exit program
def exit():
    os.system("echo \"$(date +\"%H:%M:%S\") Module terminated\" >> $network_scan_log")
    sys.exit()

# =======================
#    MENUS DEFINITIONS
# =======================
 
# Menu definition
menu_actions = {
    'main_menu': main_menu,
    '1': ping_sweep_menu,
    '2': arp_scan_menu,
    '9': back,
    '0': exit,
}
 
# =======================
#      MAIN PROGRAM
# =======================
 
# Main Program
if __name__ == "__main__":
    
    os.system("date > $network_scan_log")
    os.system("echo \"Module started:\n\n\" >> $network_scan_log")
    
    # Launch main menu
    main_menu()