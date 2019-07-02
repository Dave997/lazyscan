#!/usr/bin/env python

# -*- coding: utf-8 -*-
#project         :lazy scan
#title           :ftp.py
#description     :Script to find fulnerabilities in the ftp protocol
#author          :Davide Ambrosi
#date            :07/06/2019
#version         :0.1
#usage           :python3 ftp.py <host> <ftp info dictionary> <verbose>
#python_version  :3.7 
#notes           :Credits to https://github.com/laconicwolf/FTP-Tools/blob/master/ftp_discover.py
#=======================================================================

import sys, os
import json, csv, pprint
import ftplib

host = sys.argv[1] 
ftp_info = json.loads(sys.argv[2])  #{'name': 'ftp', 'product': 'Microsoft ftpd', 'ostype': 'Windows', 'method': 'probed', 'conf': '10'}
verbose = bool(sys.argv[3])
max_depth = 5

os.system("date > $ftp_log")
os.system("echo "" > $ftp_result_dirs")
os.system("echo '\n** ExploitDB search: \n' >> $ftp_log")
os.system("echo \"\t$(date +\"%H:%M:%S\") ExploitDB search on ftp\" >> $host_scan_log")

print("\n\033[1mScanning FTP protocol on  " + host + "...\033[0m")

# Search for known exploits
try:
    cmd = "searchsploit " + ftp_info["name"] + " " + ftp_info["product"]  + " " + ftp_info["version"]
    if verbose:
        os.system(cmd + " | tee -a $ftp_log")
    else:
        os.system(cmd + " >> $ftp_log")
except:
    cmd = "searchsploit " + ftp_info["name"] + " " + ftp_info["product"]
    if verbose:
        os.system(cmd + " | tee -a $ftp_log")
    else:
        os.system(cmd + " >> $ftp_log")

os.system("echo \"\t\t " + cmd + "\" >> $host_scan_log")

# =======================
#       FUNCTIONS
# =======================

def ftp_anon_login(ftp_obj):
    """Attempts to anonymously login to an FTP server"""
    login_message = ''
    try:
        login_message = ftp_obj.login()
    except ftplib.all_errors:
        pass
    return login_message

def list_directories(ftp_obj, depth=1):
    """Return a recursive listing of an ftp server contents (starting from
    the current directory). Listing is returned as a recursive dictionary, where each key
    contains a contents of the subdirectory or None if it corresponds to a file. Adapted from:
    https://stackoverflow.com/questions/1854572/traversing-ftp-listing
    """
    if depth > max_depth:
        return ['depth > {}'.format(max_depth)]
    entries = {}
    try:
        for entry in (path for path in ftp_obj.nlst() if path not in ('.', '..')):
            #print(entry)
            try:
                ftp_obj.cwd(entry)
                entries[entry] = list_directories(ftp_obj, depth + 1)
                ftp_obj.cwd('..')
            except ftplib.error_perm:
                entries[entry] = None
            except Exception as e:
                print('An error occurred: {}'.format(e))
                return entries
    except ftplib.error_perm:
        return entries
    if entries is {}:
        try:
            ftp_obj.cwd('/')
            directories = ftp_obj.nlst()
        except ftplib.error_perm:
            return
        for item in directories:
            entries[item] = ''
    return entries
# =======================

if verbose:
    print("\nScanning Server access...")
    
os.system("echo '\n** FTP server scan: \n' >> $ftp_log")
os.system("echo \"\t$(date +\"%H:%M:%S\") FTP-walk started\" >> $host_scan_log")

# =======================
#       FTP WALK
# =======================
host_data = []
ftp = ftplib.FTP()
try:
    banner = ftp.connect(host, 21, timeout=5)
    print('[+] {0}:{1} - Connection established'.format(host, 21))
    os.system("echo '[+] " + host +  ":21 - Connection established\n' >> $ftp_log")
    
    print('      {}'.format(banner))
    os.system("echo '   --> " + banner + " \n' >> $ftp_log")
    
    # Attempts anonymous login
    login_message = ftp_anon_login(ftp)
    if login_message != '':
        print('[+] {0}:{1} - Anonyomous login established'.format(host, 21))
        os.system("echo '[+] " + host + ":21 - Anonyomous login established \n' >> $ftp_log")
        
        # Performs directory listing.
        all_dirs = ''
        print("Listing directories...")
        os.system("echo '[+] " + host + ":21 - Directory listing started \n' >> $ftp_log")
        dirs = list_directories(ftp)
        all_dirs = pprint.pformat(dirs)
        
        os.system("echo '\t[+] " + host + ":21 - Directory found: \n' >> $ftp_log")
        if dirs:
            print('[+] {0}:{1} - Directory Listing Received'.format(host, 21))
            print(all_dirs)
            os.system("echo '" + json.dumps(all_dirs) + "\n' >> $ftp_log")
            with open("/tmp/ftp_out.json", 'w+') as fp:
                json.dump(dirs, fp)
            os.system("cat /tmp/ftp_out.json >> $ftp_result_dirs")
            
    else:
        print('[-] {0}:{1} - Unable to log in. Permission Error'.format(host, 21))
        os.system("echo '\t[-] " + host + ":21 - Unable to log in. Permission Error \n' >> $ftp_log")
                
except ftplib.all_errors as e:
    print('[-] {0}:{1} - Unable to connect'.format(host, 21))
    os.system("echo '[-] " + host + ":21 - Unable to connect ;\n' >> $ftp_log")
    
os.system("echo \"\t$(date +\"%H:%M:%S\") FTP-walk finished\" >> $host_scan_log")

# =======================

# Custom commands
os.system("echo '\n\n** FTP custom commands: \n' >> $ftp_log")

cmd_file = "config/scanners/ftp.conf"
cmd_list = "/tmp/ftp.conf.temp"
os.system("cp " + cmd_file + " " + cmd_list + "; sed -i '/^#/d;/^$/d' " + cmd_list)

with open(cmd_list) as fp:
    line = fp.readline()
    
    while line:
        line = line.replace("$HOST", str(host))
        if line.endswith("\n") or line.endswith("\r"): line=line[:-1] #remove new line character
        
        os.system("echo \"\t$(date +\"%H:%M:%S\") Run command: " + str(line) + "\" >> $host_scan_log")        
        if verbose:
            os.system(line + " | tee -a $ftp_log $ftp_result")
        else:
            os.system(line + " | tee -a $ftp_result >> $ftp_log")
        os.system("echo \"\t$(date +\"%H:%M:%S\") Command terminated\" >> $host_scan_log")
        line = fp.readline()

print("\t[+] FTP scan finished")
os.system("echo \"\n\n$(date +\"%H:%M:%S\") FTP scan finished\" >> $ftp_log")