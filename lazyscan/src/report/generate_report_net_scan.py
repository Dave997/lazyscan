#!/usr/bin/env python

# -*- coding: utf-8 -*-
#project         :lazy scan
#title           :generate_report_net_scan.py
#description     :Script to collect all results generated from network scan and generate a human readable report
#author          :Davide Ambrosi
#date            :01/07/2019
#version         :0.1
#usage           :python3 generate_report_net_scan.py <destination folder>
#python_version  :3.6  
#notes           :
#=======================================================================

import sys, os
from datetime import datetime

dest = sys.argv[1]
now = datetime.now()

# ===========================
#     NETWORK SCAN RESULTS
# ===========================
    
md_file_net = dest + "/network_scan.md"

f = open(md_file_net, "w+")
f.write('<p align="right"><i>' + str(now.strftime("%d/%m/%Y %H:%M:%S")) + '</i></p>')
f.write("\n\n")
f.write("# Network Scan")
f.write("\n")

#ping sweep 
alive_hosts = []    
net = ""
ping_out = "/tmp/ping-sweep.out"
os.system("cp $ping_sweep_result " + ping_out)

if os.stat(ping_out).st_size > 0:
    with open(ping_out) as fp:  
        line = fp.readline()
        while line:
            parts = line.split(";")
            if parts[1] == "net_addr":
                net = parts[0]
            else:
                alive_hosts.append(line)
                
            line = fp.readline()
        
        # write report
        f.write("## Ping Sweep")
        f.write("\n\n")
        f.write("Network Scanned: `" + net + "`")
        f.write("\n\n")
        f.write("Host alive:\n\n")
        f.write("> | IP | Hostname |\n")
        f.write("> |:---:|:---:| \n")
        for line in alive_hosts:
            parts = line.split(";")
            f.write("> | " + parts[0] + " | " + parts[1] + " | \n")
        f.write("\n\n<br>\n")
    
#arp scan
alive_hosts = []    
net = ""
arp_out = "/tmp/arp-scan.out"
os.system("cp $arp_scan_result " + arp_out)

if os.stat(arp_out).st_size > 0:
    with open(arp_out) as fp:  
        line = fp.readline()
        while line:
            parts = line.split(";")
            if parts[1] == "net_addr":
                net = parts[0]
            else:
                alive_hosts.append(line)
                
            line = fp.readline()
        
        # write report
        f.write("\n")
        f.write("## Arp Scan ")
        f.write("\n\n")
        f.write("Network Scanned: `" + net + "`")
        f.write("\n\n")
        f.write("Host alive:\n\n")
        f.write("> | IP | MAC | Hostname |\n")
        f.write("> |:---:|:---:|:---:| \n")
        for line in alive_hosts:
            parts = line.split(";")
            f.write("> | " + parts[0] + " | " + parts[1].split("(")[0] + " | " + parts[2] + " |\n")
        f.write("\n\n<br>\n")

f.close()
    
# create pdf
pdf_file = dest + "/network_scan.pdf"

try:
    os.system("pandoc -s -o " + pdf_file + " " + md_file_net)
except:
    sys.exit(1)    

sys.exit(0)