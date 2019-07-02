#!/usr/bin/env python

# -*- coding: utf-8 -*-
#project         :lazy scan
#title           :arp_scan.py
#description     :Script to automate host discovery in LAN
#author          :Davide Ambrosi
#date            :31/05/2019
#version         :0.1
#usage           :python3 arp_scan.py <network address> <network interface>
#python_version  :3.7 
#notes           :arp-scan requires sudo rights
#=======================================================================

import sys, os, re
import ipcalc
import signal

net_addr = sys.argv[1]
net_int = sys.argv[2]

os.system("date > $arp_scan_log")
os.system("echo \"arp-scan started:\n\n\" >> $arp_scan_log ")

logfile = "/tmp/arpscan.log"
# sudo arp-scan --interface enp3s0f1 172.27.88.0/26 --pcapsavefile /tmp/lazyscan/results/net_scan/arp.pcap
os.system ("sudo arp-scan --interface " + net_int + " " + net_addr + " > " + logfile)
os.system("cat " + logfile + " >> $arp_scan_log")

# read log file and extract alive hosts
ip_reg = re.compile("^([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])\.([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])\.([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])\.([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])") 

print ("\nHosts found: ")
print ('\033[1m\tIP\t\tMAC\t\thostname\033[0m')
with open(logfile) as fp:  
    line = fp.readline()
    
    os.system("echo \"" + str(net_addr) + ";net_addr;\" > $arp_scan_result")  
    while line:
        if ip_reg.search(line):
            if line.endswith("\n") or line.endswith("\r"): line=line[:-1] #remove new line character
            
            print(line.split("\t")[0] + "\t" + line.split("\t")[1] + "\t" + line.split("\t")[2])
            os.system("echo \"" +line.split("\t")[0] + ";" + line.split("\t")[1] + ";" + line.split("\t")[2] + ";\" >> $arp_scan_result")
            
        line = fp.readline()
        
os.system("echo \"\n\n$(date +\"%H:%M:%S\") arp scan finished\" >> $arp_scan_log")