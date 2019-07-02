#!/usr/bin/env python

# -*- coding: utf-8 -*-
#project         :lazy scan
#title           :generate_report_host_scan.py
#description     :Script to collect all results generated from host scan and generate a human readable report
#author          :Davide Ambrosi
#date            :01/07/2019
#version         :0.1
#usage           :python3 generate_report_host_scan.py <destination folder>
#python_version  :3.6  
#notes           :
#=======================================================================

import sys, os
from datetime import datetime

dest = sys.argv[1]
now = datetime.now()

# ===========================
#      HOST SCAN RESULTS
# ===========================
md_file = dest + "/host_scan.md"

f = open(md_file, "w+")
f.write('<p align="right"><i>' + str(now.strftime("%d/%m/%Y %H:%M:%S")) + '</i></p>')
f.write("\n\n")
f.write("# Host Scan")
f.write("\n\n")

## *** NMAP CVE scan *** ##
tmp_out = "/tmp/nmap_cve_scan.out"
os.system("cp $nmap_cve_scan_result " + tmp_out)

if os.stat(tmp_out).st_size > 1:
    with open(tmp_out) as fp:  
        line = fp.readline()
        
        f.write("## Nmap CVE scan")
        f.write("\n\n")
        f.write("```bash")
        f.write("\n")
        while line:
            line = fp.readline()
            f.write(line + "\n")
        f.write("```")
        f.write("\n\n")
##************************##  

## *** NMAP port scan *** ##
tmp_out = "/tmp/nmap_port_scan.out"
os.system("cp $nmap_port_scan_result " + tmp_out)

if os.stat(tmp_out).st_size > 1:
    with open(tmp_out) as fp:  
        line = fp.readline()
        
        f.write("## Nmap port scan")
        f.write("\n\n")
        f.write("```bash")
        f.write("\n")
        while line:
            line = fp.readline()
            f.write(line + "\n")
        f.write("```")
        f.write("\n\n")
##***********************##  

#cmd = "find $result_host_scan_folder -maxdepth 2 -type f -size +1c | grep -v port-scan | grep -v cve-scan > /tmp/result-list.txt"

## *** Modules results *** ##
module_file = "config/modules.conf"
module_list = "/tmp/modules.conf.temp"
os.system("cp " + module_file + " " + module_list + "; sed -i '/^#/d;/^$/d' " + module_list)

with open(module_list) as fp:
    line = fp.readline()
    
    while line:
        parts = line.split(";")
        port = parts[0]
        module = parts[1] 
        if port is not 80:
            out_file = parts[2]    
            out_file = "$" + out_file   
            if out_file.endswith("\n") or out_file.endswith("\r"): out_file=out_file[:-1] #remove new line character  
 
        #*** Read single module result ***#
        if int(port) == 80:
            f.write("## Port " + port + " scan")
            f.write("\n\n")
            f.write(" --> Check http_report.pdf")
            
            # copy aquatone files and all pages md 
            os.system("mkdir " + dest + "/http")
            http_dest = dest + "/http"
            md_file_http = http_dest + "/http_scan.md"
            pdf_file_http = http_dest + "/http_scan.pdf"
            os.system("cp -r $result_host_scan_folder_http_aquatone " + http_dest + "/aquatone")
            os.system("cp -r $result_host_scan_folder_http_pages " + http_dest)
            
            # write and compile http report
            f_http = open(md_file_http, "w+")
            f_http.write('<p align="right"><i>' + str(now.strftime("%d/%m/%Y %H:%M:%S")) + '</i></p>')
            f_http.write("\n\n")
            f_http.write("# HTTP Scan")
            f_http.write("\n\n")
            
            res = os.environ['result_host_scan_folder_http'] + "/"
            files = sorted(filter(os.path.isfile, ["{}{}".format(res,i) for i in os.listdir(res)]), key=os.path.getmtime)
            for file in files:
                if os.stat(file).st_size > 1:
                    with open(file) as fp3:  
                        line2 = fp3.readline()
                        f_http.write("## " + file)
                        f_http.write("\n\n")
                        f_http.write("```bash")
                        f_http.write("\n")
                        while line2:
                            f_http.write(line2 + "\n")
                            line2 = fp3.readline()
                        f_http.write("```")
                        f_http.write("\n\n")
            
            f_http.close()
            
            # compile http file
            try:
                os.system("pandoc -V geometry:margin=1in -o " + pdf_file_http + " " + md_file_http)
            except:
                sys.exit(1)  
        else:
            tmp_out = "/tmp/port_" + str(port) + ".out"
            os.system("cp " + out_file + " " + tmp_out)

            if os.stat(tmp_out).st_size > 1:
                with open(tmp_out) as fp2:  
                    line = fp2.readline()
                    
                    f.write("## Port " + port + " scan")
                    f.write("\n\n")
                    f.write("```bash")
                    f.write("\n")
                    while line:
                        line = fp2.readline()
                        f.write(line + "\n")
                    f.write("```")
                    f.write("\n\n")
        #*********************************#
            
        line = fp.readline()
##*************************##  

f.close()
    
# create pdf
pdf_file = dest + "/host_scan.pdf"

try:
    os.system("pandoc -V geometry:margin=1in -o " + pdf_file + " " + md_file)
except:
    sys.exit(1)    

sys.exit(0)
