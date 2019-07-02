#!/usr/bin/env python

# -*- coding: utf-8 -*-
#project         :lazy scan
#title           :sample_module.py
#description     :Sample module script
#author          :Davide Ambrosi
#date            :
#version         :0.1
#usage           :python3 smb.py <host> <protocol info dictionary> <verbose>
#python_version  :3.7 
#notes           :
#=======================================================================

import sys, os
import json
import time

host = sys.argv[1] 
PROTOCOL_INFO = json.loads(sys.argv[2])
verbose = bool(sys.argv[3])

os.system("date > $LOG_FILE")
os.system("echo '\n** ExploitDB search: \n' >> $LOG_FILE")
os.system("echo \"\t$(date +\"%H:%M:%S\") ExploitDB search on smb\" >> $host_scan_log")

print("\n\033[1mScanning SMB protocol on  " + host + "...\033[0m")

# Search for known exploits
try:
    cmd = "searchsploit " + PROTOCOL_INFO["name"] + " " + PROTOCOL_INFO["product"]  + " " + PROTOCOL_INFO["version"]
    if verbose:
        os.system(cmd + " | tee -a $LOG_FILE")
    else:
        os.system(cmd + " >> $LOG_FILE")
except:
    cmd = "searchsploit " + PROTOCOL_INFO["name"] + " " + PROTOCOL_INFO["product"]
    if verbose:
        os.system(cmd + " | tee -a $LOG_FILE")
    else:
        os.system(cmd + " >> $LOG_FILE")

os.system("echo \"\t\t " + cmd + "\" >> $host_scan_log")


# =======================
#      PROTOCOL SCAN
# =======================

os.system("echo '\n\n** PROTOCOL scan started: \n' >> $LOG_FILE")

if verbose:
    print("\nScanning PROTOCOL...")

cmd_file = "config/scanners/PROTOCOL.conf"
cmd_list = "/tmp/PROTOCOL.conf.temp"
os.system("cp " + cmd_file + " " + cmd_list + "; sed -i '/^#/d;/^$/d' " + cmd_list)

with open(cmd_list) as fp:
    line = fp.readline()
    
    while line:
        line = line.replace("$HOST", str(host))
        if line.endswith("\n") or line.endswith("\r"): line=line[:-1] #remove new line character
        
        os.system("echo \"\t$(date +\"%H:%M:%S\") Run command: " + str(line) + "\" >> $host_scan_log")        
        if verbose:
            os.system(line + " | tee -a $LOG_FILE $PROTOCOL_RESULT")
        else:
            os.system(line + " | tee -a $PROTOCOL_RESULT >> $LOG_FILE")
        os.system("echo \"\t$(date +\"%H:%M:%S\") Command terminated\" >> $host_scan_log")
        line = fp.readline()

print("\t[+] SMB scan finished")
os.system("echo \"\n\n$(date +\"%H:%M:%S\") SMB scan finished\" >> $LOG_FILE")