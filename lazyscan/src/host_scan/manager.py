#!/usr/bin/env python

# -*- coding: utf-8 -*-
#project         :lazy scan
#title           :manager.py
#description     :Script to manage all scan modules, port list given
#author          :Davide Ambrosi
#date            :06/06/2019
#version         :0.1
#usage           :python3 manager.py <host> <port list (nmap output)> <verbose>
#python_version  :3.7 
#notes           :
#=======================================================================

import sys, os
import xml.etree.ElementTree as ET
import subprocess
import time
from datetime import datetime
import json

host = sys.argv[1]
nmap_out = sys.argv[2]
verbose = sys.argv[3]

# =======================
#    PARSE XML FILE
# =======================
# Extract all useful data about running services, in ports dictionary

tree = ET.parse(nmap_out)
root = tree.getroot()

ports = {}
for port in root.iter('port'):
    n = int(port.attrib['portid'])
    for service in port.iter('service'):
        #ports[n] = {'name': service.attrib["name"], 'product': service.attrib["product"], 'version': service.attrib["version"]}
        ports[n] = service.attrib
# ======================= #

def run_subprocess(info, modulename):
    # start subprocess
    os.system("echo \"$(date +\"%H:%M:%S\") Started module " + modulename + "\" >> $host_scan_log")
    sp = subprocess.Popen(['python3', './src/host_scan/modules/' + modulename, str(host), info, verbose],
                            shell=False,
                            stdin=subprocess.PIPE
                            )
    sp.communicate()
    os.system("echo \"$(date +\"%H:%M:%S\") " + modulename + " finished\" >> $host_scan_log")

# =======================
#  START PORT2PORT SCAN
# =======================

# load installed module list
module_file = "config/modules.conf"
module_list = "/tmp/modules.conf.temp"
os.system("cp " + module_file + " " + module_list + "; sed -i '/^#/d;/^$/d' " + module_list)

with open(module_list) as fp:
    line = fp.readline()
    
    while line:
        parts = line.split(";")
        port = parts[0]
        module = parts[1] 
        
        if int(port) in ports.keys():
            os.system("echo \"\n$(date +\"%H:%M:%S\") Scanning port " + str(port) + "\" >> $host_scan_log")
            run_subprocess(json.dumps(ports[int(port)]), str(module))
            ports.pop(int(port), None)   
            
        line = fp.readline()
        
   
# Search exploit for all other ports
for k in ports.keys():
    os.system("echo \"\n$(date +\"%H:%M:%S\") Scanning port " + str(k) + "\" >> $host_scan_log")
    
    try:
        print("\n\033[1mScanning " + k["name"] + " protocol on  " + host + "...\033[0m")
        try:
            cmd = "searchsploit " + k["name"] + " " + k["product"]  + " " + k["version"]
        except:
            cmd = "searchsploit " + k["name"] + " " + k["product"]
            
        os.system(cmd + " | tee -a $protocol_exploits_log")
        os.system(cmd.replace("searchsploit", "searchsploit -j") + " | tee -a $protocols_exploits")
    except:
        print("Port filtered!")
        os.system("echo \"\t$(date +\"%H:%M:%S\") " + k + " port filtered!\" >> $host_scan_log")
    
    
os.system("echo \"$(date +\"%H:%M:%S\") All ports have been scanned\" >> $host_scan_log")

# ======================= #