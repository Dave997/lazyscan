#!/usr/bin/env python

# -*- coding: utf-8 -*-
#project         :lazy scan
#title           :http_.py
#description     :Script to find fulnerabilities in the http protocol
#author          :Davide Ambrosi
#date            :07/06/2019
#version         :0.1
#usage           :python3 http.py <host> <http info dictionary> <verbose>
#python_version  :3.7 
#notes           :the _ in the name is due to requests import 
#=======================================================================

import sys, os
import json
import subprocess
import requests
from bs4 import BeautifulSoup

host = sys.argv[1]
http_info = json.loads(sys.argv[2])
verbose = bool(sys.argv[3])

if "http://" not in host and "https://" not in host:
    host = "http://" + host

print("\n\033[1mScanning HTTP protocol on  " + host + "...\033[0m")

os.system("date > $http_log")
os.system("date > $nikto_log")
os.system("date > $web_recon_log")
os.system("date > $wfuzz_folders_log")
os.system("date > $wfuzz_files_log")
os.system("date > $spider_log")
os.system("date > $tech_log")
os.system("date > $cms_scan_log")
os.system("date > $xss_log")
os.system("date > $sqli_log")

os.system("echo '\n** ExploitDB search: \n' >> $http_log")
os.system("echo \"\t$(date +\"%H:%M:%S\") ExploitDB search on http\" >> $host_scan_log")

# Search for known exploits on the web server
try:
    cmd = "searchsploit " + http_info["name"] + " " + http_info["product"]  + " " + http_info["version"]
    if verbose:
        os.system(cmd + " | tee -a $http_log")
    else:
        os.system(cmd + " >> $http_log")
except:
    cmd = "searchsploit " + http_info["name"] + " " + http_info["product"]
    if verbose:
        os.system(cmd + " | tee -a $http_log")
    else:
        os.system(cmd + " >> $http_log")

os.system("echo \"\t\t " + cmd + "\" >> $host_scan_log")
    
print("\t[+] http exploit scan finished!")

# =======================
#      WEB PAGE SCAN
# =======================

#-- NIKTO --
os.system("echo \"\t\t$(date +\"%H:%M:%S\") Nikto started\" >> $host_scan_log")
if verbose:
    print("\nRunning Nikto...")

cmd = "nikto -h " + host + " -o $nikto_result"
if verbose:
    os.system(cmd + " | tee -a $nikto_log")
else:
    os.system(cmd + " >> $nikto_log")
print("\t[+] Nikto scan done!")
os.system("echo \"\t\t$(date +\"%H:%M:%S\") Nikto finished\" >> $host_scan_log")
#-----------

#-- WFUZZ --
os.system("echo \"\t\t$(date +\"%H:%M:%S\") Wfuzz on dirs started\" >> $host_scan_log")
if verbose:
    print("\nRunning Wfuzz...")

cmd = "wfuzz -f $wfuzz_out_dirs,json -c -z file,$dir_wordlist --hc 404 " + host + "/FUZZ"
if verbose:
    os.system(cmd + " | tee -a $wfuzz_folders_log")
else:
    os.system(cmd + " >> $wfuzz_folders_log")
    
print("\t[+] Wfuzz directory listing done!")
os.system("echo \"\t\t$(date +\"%H:%M:%S\") Wfuzz on dirs finished\" >> $host_scan_log")

os.system("echo \"\t\t$(date +\"%H:%M:%S\") Wfuzz on files started\" >> $host_scan_log")
cmd = "wfuzz -f $wfuzz_out_files,json -c -z file,$file_wordlist --hc 404 " + host + "/FUZZ"
if verbose:
    os.system(cmd + " | tee -a $wfuzz_files_log")
else:
    os.system(cmd + " >> $wfuzz_files_log")
    
print("\t[+] Wfuzz files listing done!")
os.system("echo \"\t\t$(date +\"%H:%M:%S\") Wfuzz on files finished\" >> $host_scan_log")
#-----------

#-- SPIDER --
os.system("echo \"\t\t$(date +\"%H:%M:%S\") Spidering started\" >> $host_scan_log")
if verbose:
    print("\nSpidering...")

cmd = "wget --spider -r --no-directories " + host + " 2>&1 | grep '^--' | awk '{ print $3 }' | grep -v '\.\(css\|js\|png\|gif\|jpg\|JPG\|ico\|svg\|pdf\)' | awk -F '\\?*' '{print $1}' | uniq"
if verbose:
    os.system(cmd + " | tee $spider | tee -a $spider_log")
else:
    os.system(cmd + " | tee $spider >> $spider_log")

print("\t[+] Spidering done!")
os.system("echo \"\t\t$(date +\"%H:%M:%S\") Spidering finished\" >> $host_scan_log")
#------------

#-- TECH USED --
os.system("echo \"\t\t$(date +\"%H:%M:%S\") Whatweb started\" >> $host_scan_log")
if verbose:
    print("\nGathering technology informations...")

cmd = "whatweb --color=never " + host
if verbose:
    os.system(cmd + " | tee $tech | tee -a $tech_log")
else:
    os.system(cmd + " | tee $tech >> $tech_log")

if verbose:
    print("\n")

os.system("echo \"\t\t$(date +\"%H:%M:%S\") Whatweb finished\" >> $host_scan_log")
os.system("echo \"\t\t$(date +\"%H:%M:%S\") Wad started\" >> $host_scan_log")

cmd = "wad -u " + host + " -q"
if verbose:
    os.system(cmd + " | tee $tech_json | tee -a $tech_log")
else:
    os.system(cmd + " | tee $tech_json >> $tech_log")
    
os.system("echo \"\t\t$(date +\"%H:%M:%S\") Wad finished\" >> $host_scan_log")

# cms scan if detected
wad_out = {}
cms = ""

try:
    tech_json = os.environ['tech_json']
    with open(tech_json) as json_file:  
        wad_out = json.load(json_file)
        
    if len(wad_out) > 0:
        for x in wad_out[list(wad_out.keys())[0]]:
            if "cms" in x['type']:
                cms = x['app']
                if verbose:
                    print (cms + " found!")

        if len(str(cms)) > 0:
            os.system("echo '** Scanning " + cms + ": \n' >> $cms_scan_log")
            if verbose:
                print("\nScanning " + cms + "...")

            if cms.lower() == "wordpress":
                os.system("echo \"\t\t$(date +\"%H:%M:%S\") WPscan started\" >> $host_scan_log")
                # https://wpscan.org/
                cmd = "wpscan --url " + host + " -f json"
                if verbose:
                    os.system(cmd + " | tee $cms_out | tee -a $cms_scan_log")
                else:
                    os.system(cmd + " | tee $cms_out >> $cms_scan_log")
                os.system("echo \"\t\t$(date +\"%H:%M:%S\") WPscan finished\" >> $host_scan_log")
            elif cms.lower() == "joomla":
                os.system("echo \"\t\t$(date +\"%H:%M:%S\") Joomscan started\" >> $host_scan_log")
                # https://tools.kali.org/web-applications/joomscan
                cmd = "perl /opt/joomscan/joomscan.pl --url " + host
                if verbose:
                    os.system(cmd + " | tee $cms_out | tee -a $cms_scan_log") 
                else:
                    os.system(cmd + " | tee $cms_out >> $cms_scan_log")
                os.system("echo \"\t\t$(date +\"%H:%M:%S\") Joomscan finished\" >> $host_scan_log")
            else:
                print("\t[-] CMS not recognized!")
        else:
            print("\t[-] No cms detected")
    else:
            print("\t[-] No cms recognized")
except:
    print(" [-] Error parsing wad json file for cms scan")

#---------------

#-- PAGE SCAN --

# get pages
pages = []

spider = os.environ['spider']
with open(spider) as f: 
    for line in f: 
        line = line[:-2] if line.endswith("\n") else line
        pages.append(line)

wfuzz = {} 
wfuzz_out_files = os.environ['wfuzz_out_files']
with open(wfuzz_out_files) as json_file:  
    wfuzz = json.load(json_file)  
for url in wfuzz:
    pages.append(url['url'])

# remove duplicate entries
pages = list(dict.fromkeys(pages))

# aquatone report
txt_list = open("/tmp/aquatone_urls.txt", "w+")
for url in pages:
    txt_list.write(url+"\n")
txt_list.close()

if verbose:
    cmd = "cat /tmp/aquatone_urls.txt | aquatone -out $result_host_scan_folder_http_aquatone"
else:
    cmd = "cat /tmp/aquatone_urls.txt | aquatone -out $result_host_scan_folder_http_aquatone > /dev/null"
os.system("echo \"\t\t$(date +\"%H:%M:%S\") Aquatone started\" >> $host_scan_log")
os.system(cmd)
os.system("echo \"\t\t$(date +\"%H:%M:%S\") Aquatone finished\" >> $host_scan_log")
    
#scan each page 
print("\nScanning single pages found...")

for page in pages:  
    try:   
        results_folder_pages = os.environ['result_host_scan_folder_http_pages']
        result_file = results_folder_pages + "/" + page.replace("/","-") + ".md"
        os.system("touch " + result_file)
        print("Scanning " + page)
        
        # web-reconnaissance
        os.system("echo \"\t\t$(date +\"%H:%M:%S\") Web-recon started on " + page + "\" >> $host_scan_log")
        try:
            cmd = "python web-reconnaissance.py -u " + page + " -o " + result_file
            os.system("echo 'web-reconnaissance.py launched on " + page + "' >> $web_recon_log")
            sp = subprocess.Popen(['python2', './src/host_scan/modules/web-reconnaissance.py', "-u", str(page), "-o", str(result_file)],
                                    shell=False,
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE
                                    )
            sp.communicate()
            print("\t[+] web-reconnaissance done!")
        except:
            print("\t[-] web-reconnaissance went wrong!")
        os.system("echo \"\t\t$(date +\"%H:%M:%S\") Web-recon finished\" >> $host_scan_log")
        
        # xss scan
        os.system("echo \"\t\t$(date +\"%H:%M:%S\") xsser started on " + page + "\" >> $host_scan_log")
        try:
            cmd = "xsser -u " + page
            os.system("echo 'xsser launched on " + page + "' >> $xss_log")
            os.system("echo '\n<br>' >> " + result_file)
            os.system("echo '# XSS SCAN\n\n' >> " + result_file)
            os.system("echo '``` bash\n' >> " + result_file)
            os.system(cmd + " > /tmp/xsser.log")
            os.system("cat /tmp/xsser.log >> " + result_file)
            os.system("cat /tmp/xsser.log >> $xss_log")
            os.system("echo '\n```\n\n' >> " + result_file)
            print("\t[+] xss scan done!")
        except:
            print("\t[-] xss scan went wrong!")
        os.system("echo \"\t\t$(date +\"%H:%M:%S\") xsser finished\" >> $host_scan_log")    
        
        # SQLi
        os.system("echo \"\t\t$(date +\"%H:%M:%S\") SQLmap started on " + page + "\" >> $host_scan_log")
        try:
            response = requests.get(page)
            soup = BeautifulSoup(response.text, 'html.parser')

            for element in soup.find_all('input'):
                name = element['name']     
                os.system("echo 'sqlmap launched on " + page + "' >> $sqli_log")
                os.system("echo '\n<br>' >> " + result_file)
                os.system("echo '# SQLi SCAN\n\n' >> " + result_file)
                os.system("Testing parameter `" + name + "`:")
                os.system("echo '``` bash\n' >> " + result_file)
                cmd = "sqlmap -u '" + page + "' --dbs --tables --data='" + name + "=asdf' --batch -v 0 > /tmp/sqli.log"
                os.system(cmd)
                os.system("cat /tmp/sqli.log >> " + result_file)
                os.system("cat /tmp/sqli.log >> $sqli_log")
                os.system("echo '\n```\n\n' >> " + result_file)
                
            print("\t[+] SQLi scan done!")
        except:
            print("\t[-] SQLi scan went wrong!")
        os.system("echo \"\t\t$(date +\"%H:%M:%S\") SQLmap finished\" >> $host_scan_log")
    except KeyboardInterrupt:
        break
#---------------

# custom commands 
cmd_file = "config/scanners/http_.conf"
cmd_list = "/tmp/http_.conf.temp"
os.system("cp " + cmd_file + " " + cmd_list + "; sed -i '/^#/d;/^$/d' " + cmd_list)

with open(cmd_list) as fp:
    line = fp.readline()
    
    while line:
        line = line.replace("$HOST", str(host))
        if line.endswith("\n") or line.endswith("\r"): line=line[:-1] #remove new line character
        
        os.system("echo \"\t$(date +\"%H:%M:%S\") Run command: " + str(line) + "\" >> $host_scan_log")        
        if verbose:
            os.system(line + " | tee -a $http_log $http_result")
        else:
            os.system(line + " | tee -a $http_result >> $http_log")
        os.system("echo \"\t$(date +\"%H:%M:%S\") Command terminated\" >> $host_scan_log")
        line = fp.readline()

os.system("echo \"\n$(date +\"%H:%M:%S\") HTTP scan finished\" >> $http_log")