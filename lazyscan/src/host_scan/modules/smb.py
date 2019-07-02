#!/usr/bin/env python

# -*- coding: utf-8 -*-
#project         :lazy scan
#title           :smb.py
#description     :Script to find fulnerabilities in the smb protocol
#author          :Davide Ambrosi
#date            :07/06/2019
#version         :0.1
#usage           :python3 smb.py <host> <smb info dictionary> <verbose>
#python_version  :3.7 
#notes           :
#=======================================================================

import sys, os
import json
import time

host = sys.argv[1] 
smb_info = json.loads(sys.argv[2])
verbose = bool(sys.argv[3])

os.system("date > $smb_log")
os.system("echo '\n** ExploitDB search: \n' >> $smb_log")
os.system("echo \"\t$(date +\"%H:%M:%S\") ExploitDB search on smb\" >> $host_scan_log")

print("\n\033[1mScanning SMB protocol on  " + host + "...\033[0m")

# Search for known exploits
try:
    cmd = "searchsploit " + smb_info["name"] + " " + smb_info["product"]  + " " + smb_info["version"]
    if verbose:
        os.system(cmd + " | tee -a $smb_log")
    else:
        os.system(cmd + " >> $smb_log")
except:
    cmd = "searchsploit " + smb_info["name"] + " " + smb_info["product"]
    if verbose:
        os.system(cmd + " | tee -a $smb_log")
    else:
        os.system(cmd + " >> $smb_log")

os.system("echo \"\t\t " + cmd + "\" >> $host_scan_log")


# =======================
#        SMB SCAN
# =======================

os.system("echo '\n\n** SMB scan started: \n' >> $smb_log")

if verbose:
    print("\nScanning SMB...")

cmd_file = "config/scanners/smb.conf"
cmd_list = "/tmp/smb.conf.temp"
os.system("cp " + cmd_file + " " + cmd_list + "; sed -i '/^#/d;/^$/d' " + cmd_list)

with open(cmd_list) as fp:
    line = fp.readline()
    
    while line:
        line = line.replace("$HOST", str(host))
        if line.endswith("\n") or line.endswith("\r"): line=line[:-1] #remove new line character
        
        os.system("echo \"\t$(date +\"%H:%M:%S\") Run command: " + str(line) + "\" >> $host_scan_log")        
        if verbose:
            os.system(line + " | tee -a $smb_log $smb_result")
        else:
            os.system(line + " | tee -a $smb_result >> $smb_log")
        os.system("echo \"\t$(date +\"%H:%M:%S\") Command terminated\" >> $host_scan_log")
        line = fp.readline()

print("\t[+] SMB scan finished")
os.system("echo \"\n\n$(date +\"%H:%M:%S\") SMB scan finished\" >> $smb_log")