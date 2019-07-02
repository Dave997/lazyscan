#!/usr/bin/env python

# -*- coding: utf-8 -*-
#project         :lazy scan
#title           :nmap_cve_scan.py
#description     :Script to automate host discovery in LAN
#author          :Davide Ambrosi
#date            :06/06/2019
#version         :0.1
#usage           :python3 nmap_cve_scan.py <host address>
#python_version  :3.7 
#notes           :
#=======================================================================

import sys, os

host = sys.argv[1]

os.system("date > $nmap_cve_scan_log")
os.system("echo "" > $nmap_cve_scan_result")
os.system("echo 'Nmap CVE scan started:\n\n' >> $nmap_cve_scan_log")

print("\nScanning " + str(host) + "...")

cmd_file = "config/scanners/cve_scan.conf"
cmd_list = "/tmp/cve_scan.conf.temp"
os.system("cp " + cmd_file + " " + cmd_list + "; sed -i '/^#/d;/^$/d' " + cmd_list)

with open(cmd_list) as fp:
    line = fp.readline()
    
    while line:
        line = line.replace("$HOST", str(host))
        if line.endswith("\n") or line.endswith("\r"): line=line[:-1] #remove new line character
        
        os.system("echo \"\t$(date +\"%H:%M:%S\") Run command: " + str(line) + "\" >> $host_scan_log")        
        os.system(line)
        os.system("echo \"\t$(date +\"%H:%M:%S\") Command terminated\" >> $host_scan_log")
        line = fp.readline()
        
        #sys.stdout.flush()

print("Finished!")
os.system("echo \"\n\n$(date +\"%H:%M:%S\") Nmap CVE scan finished\" >> $nmap_cve_scan_log")