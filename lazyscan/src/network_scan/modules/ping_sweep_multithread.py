#!/usr/bin/env python

# -*- coding: utf-8 -*-
#project         :lazy scan
#title           :ping_sweep.py
#description     :Script to automate host discovery in LAN
#author          :Davide Ambrosi
#date            :05/06/2019
#version         :0.1
#usage           :python3 ping_sweep.py <network address> <max threads>
#python_version  :3.7 
#notes           :This implementation use ping command instead of nmap ping-scan, because nmap sends TCP packets, which many machines will drop
#=======================================================================

import sys, os
import ipcalc
import signal

net_addr = sys.argv[1]
max_threads = int(sys.argv[2])

os.system("date > $ping_sweep_log")
os.system("echo \"Ping sweep started:\n\n\" >> $ping_sweep_log ")

# =======================
#      THREAD MANAGER
# =======================

from multiprocessing.dummy import Pool as ThreadPool

def ping(ip):
    print("Pinging: " + str(ip))
    cmd = "ping -c 1 " + str(ip) + " >> $ping_sweep_log 2>&1"
    if os.system(cmd)==0:
        return ip
    return None

def pingParallel(iPs, threads):
    pool = ThreadPool(min(threads, len(iPs)))
    livehosts = pool.map(ping, iPs)
    pool.close()
    pool.join()
    return livehosts

# =======================

# ping all hosts
print ("Pinging " + str(len(ipcalc.Network(net_addr))-2) + " hosts...")

livehosts = pingParallel(ipcalc.Network(net_addr), max_threads)
livehosts = [ x for x in livehosts if x is not None ]

    
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
os.system("echo \"" + str(net_addr) + ";net_addr;\" >> $ping_sweep_result")    
for x in hosts:
    print(x.strip() + " " + str(hosts[x]).strip())
    os.system("echo \"" + x.strip() + ";" + str(hosts[x]).strip() + ";\" >> $ping_sweep_result")

os.system("echo \"\n\n$(date +\"%H:%M:%S\") ping sweep finished\" >> $ping_sweep_log")