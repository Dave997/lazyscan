#!/usr/bin/env python

# -*- coding: utf-8 -*-
#project         :lazy scan
#title           :ping_sweep.py
#description     :Script to automate host discovery in LAN
#author          :Davide Ambrosi
#date            :29/05/2019
#version         :0.1
#usage           :python3 ping_sweep.py <network address>
#python_version  :3.7 
#notes           :This implementation use ping command instead of nmap ping-scan, because nmap sends TCP packets, which many machines will drop
#=======================================================================

import sys, os
import ipcalc
import signal

net_addr = sys.argv[1]

os.system("date > $ping_sweep_log")
os.system("echo \"Ping sweep started:\n\n\" >> $ping_sweep_log ")

# ping all hosts
livehosts = []
count = 1
for x in ipcalc.Network(net_addr):
    print("Pinging: " + str(x) + "  [" + str(count) + "/" + str(len(ipcalc.Network(net_addr))-2) + "]")
    cmd = "ping -c 1 " + str(x) + " >> $ping_sweep_log 2>&1"
    if os.system(cmd)==0:
        livehosts.append(x)
    count+=1
    
os.system("echo '\n\n' >> $ping_sweep_log")

hosts = { str(i):"" for i in livehosts }

print("\nGathering hostnames...")

#get all possible hostnames 
cmd = "nmap -sP " + net_addr + " -oN $ping_sweep_log --append-output | sed '/^$/d;/^Starting/d;/^Host/d;/^Nmap done/d' | awk '{gsub(\"Nmap scan report for \", \"\");print}' | awk '{gsub(\" \", \";\");print}' > /tmp/hostnames.out"
os.system(cmd)

print("Matching..")
with open("/tmp/hostnames.out") as fp:  
    line = fp.readline()
    
    while line:
        parts = line.split(";")
        if len(parts) > 1:
            parts[1] = parts[1].replace('(', '')
            parts[1] = parts[1].replace(')', '')
            if parts[1].endswith("\n") or parts[1].endswith("\r"): parts[1]=parts[1][:-1] #remove new line character
            hosts[parts[1]] = parts[0]
            
        line = fp.readline()

print ("\nHosts found:")  
os.system("echo \"" + str(net_addr) + ";net_addr;\" > $ping_sweep_result")    
for x in hosts:
    print(x.strip() + " " + str(hosts[x]).strip())
    os.system("echo \"" + x.strip() + ";" + str(hosts[x]).strip() + ";\" >> $ping_sweep_result")
    
os.system("echo \"\n\n$(date +\"%H:%M:%S\") ping sweep finished\" >> $ping_sweep_log")

#=========================================
# SCAPY VERSION

# import logging
# from scapy.all import *
# # scapy prints out many warning if ipv6 is not available, so I prefer to suppress them
# logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
# net_addr = "172.27.88.4" #sys.argv[1].split(',')
# print(net_addr)
# livehosts = []
# #for x in net_addr:
# #    if lex(x) > 0:
# packet=IP(dst=str(net_addr))/ICMP()
# response = sr1(packet,timeout=1,verbose=0)
# if not (response is None):
#     if response[ICMP].type==0:
#         livehosts.append(str(net_addr))
# print ("Scan complete!\n")
# if len(livehosts)>0:
#     print ("Hosts found:\n")
#     for host in livehosts:
#         print (host)
# else:
#     print ("No live hosts found\n")
# ## -> nmap -sP 172.27.88.0/26net_addr = sys.argv[1]