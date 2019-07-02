<p align="right"><i>Davide Ambrosi</i></p>

# LAZY SCAN

## Table of contents
- [LAZY SCAN](#LAZY-SCAN)
  - [Table of contents](#Table-of-contents)
  - [Introduction](#Introduction)
  - [How to use](#How-to-use)
  - [Installation](#Installation)
  - [Configure destination folders and files](#Configure-destination-folders-and-files)
  - [Install new modules](#Install-new-modules)


## Introduction
This is a configurable tool developed to automate the first phases of a vulnerability assessment / penetration test.

It is able to scan the network, in order to identify the alive hosts, and scan all active services of a specific machine. <br>
It keep tracks of each action with many different logs, result files and reports.

## How to use

To make it run, just type `lazyscan` in your console, and then follow the menu' options.

N.B. In some cases, if the user does not have many privileges, it must be launched with sudo

## Installation

1. Clone the repo: `git clone https://github.com/Dave997/lazyscan.git`
2. Move into the repo's foler: `cd lazyscan`
3. Make the installer executable: `chmod +x install.sh`
4. Run the installer: `./install.sh`
   
**N.B**: The installer requires *sudo* permissions!

If the installation gets stuck on this line:

 `[-] Nothing here (/usr/share/exploitdb-papers). Starting fresh...`

(or something related to "exploitdb"), comment the following line in the install.sh: `searchsploit -u`

N.B. For **Fedora** users, it might be required a manual installation of some tools, because they aren't present in the DNF repositories.
(ex. wfuzz --> pip3 install wfuzz)

This installation downloads many different packages and tools, so if you don't need them daily it is preferable use it on Kali or Parrot.


## Configure destination folders and files
The configuration files (outside the scanners folder) are nothing more than a list of variables (ex: `result_folder=$base_output_folder"/results"`) 

You can change their content in order to save the files in the folder which you prefer.

**N.B.**: Varible names MUST NOT be changed! 

In the scanner folder, we can find all config files of service scanners. These files are a list of commands, that will be executed.<br>
Some of them has a default command (with a destination output), so each custom command should have a destination and log file.

## Install new modules 
This tool privide some modules for the most popular services.

If you have to scan a more specific protocol, you can install your personal module! 

To create a module, you can find a file `sample_module.py` in the host scan folder: `src/host_scan/modules`. Just follow the rules specified.

Once you have created your module, insert it in the `modules.conf` file.

The sample_module is structured to read the command from it's config file, so if you want to hardcode your command(s), just modify it accordingly.

N.B. Remember to add the log and result variable to the `logs.conf` and `results.conf` file.