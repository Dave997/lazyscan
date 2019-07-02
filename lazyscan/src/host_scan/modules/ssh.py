#!/usr/bin/env python

# -*- coding: utf-8 -*-
#project         :lazy scan
#title           :ssh.py
#description     :Script to find fulnerabilities in the ssh protocol
#author          :Davide Ambrosi
#date            :07/06/2019
#version         :0.1
#usage           :python3 ssh.py <host> <ssh info dictionary> <verbose>
#python_version  :3.7 
#notes           :
#=======================================================================

import sys, os
import json

host = sys.argv[1] 
ssh_info = json.loads(sys.argv[2])
verbose = bool(sys.argv[3])

print("\n\033[1mScanning SSH protocol on  " + host + "...\033[0m")

os.system("date > $ssh_log")
os.system("echo "" > $ssh_result")
os.system("echo '\n** ExploitDB search: \n' >> $ssh_log")
os.system("echo \"\t$(date +\"%H:%M:%S\") ExploitDB search on ssh\" >> $host_scan_log")

# Search for known exploits
try:
    cmd = "searchsploit " + ssh_info["name"] + " " + ssh_info["product"]  + " " + ssh_info["version"]
    if verbose:
        os.system(cmd + " | tee -a $ssh_log")
    else:
        os.system(cmd + " >> $ssh_log")
    os.system(cmd.replace("searchsploit", "searchsploit -j") + " > $ssh_result")
except:
    cmd = "searchsploit " + ssh_info["name"] + " " + ssh_info["product"]
    if verbose:
        os.system(cmd + " | tee -a $ssh_log")
    else:
        os.system(cmd + " >> $ssh_log")
    os.system(cmd.replace("searchsploit", "searchsploit -j") + " > $ssh_result")

os.system("echo \"\t\t " + cmd + "\" >> $host_scan_log")
    
print("\t[+] ssh exploit scan finished!")

# Custom commands
os.system("echo '\n\n** SSH custom commands: \n' >> $ssh_log")

cmd_file = "config/scanners/ssh.conf"
cmd_list = "/tmp/ssh.conf.temp"
os.system("cp " + cmd_file + " " + cmd_list + "; sed -i '/^#/d;/^$/d' " + cmd_list)

with open(cmd_list) as fp:
    line = fp.readline()
    
    while line:
        line = line.replace("$HOST", str(host))
        if line.endswith("\n") or line.endswith("\r"): line=line[:-1] #remove new line character
        
        os.system("echo \"\t$(date +\"%H:%M:%S\") Run command: " + str(line) + "\" >> $host_scan_log")        
        if verbose:
            os.system(line + " | tee -a $ssh_log $ssh_result")
        else:
            os.system(line + " | tee -a $ssh_result >> $ssh_log")
        os.system("echo \"\t$(date +\"%H:%M:%S\") Command terminated\" >> $host_scan_log")
        line = fp.readline()

print("\t[+] ssh scan finished")
os.system("echo \"\n\n$(date +\"%H:%M:%S\") SSH scan finished\" >> $ssh_log")