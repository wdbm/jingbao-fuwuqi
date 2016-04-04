#!/usr/bin/env python

"""
################################################################################
#                                                                              #
# jingbao-fuwuqi                                                               #
#                                                                              #
################################################################################
#                                                                              #
# LICENCE INFORMATION                                                          #
#                                                                              #
# This program alerts when a server becomes available.                         #
#                                                                              #
# copyright (C) 2015 William Breaden Madden                                    #
#                                                                              #
# This software is released under the terms of the GNU General Public License  #
# version 3 (GPLv3).                                                           #
#                                                                              #
# This program is free software: you can redistribute it and/or modify it      #
# under the terms of the GNU General Public License as published by the Free   #
# Software Foundation, either version 3 of the License, or (at your option)    #
# any later version.                                                           #
#                                                                              #
# This program is distributed in the hope that it will be useful, but WITHOUT  #
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or        #
# FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for     #
# more details.                                                                #
#                                                                              #
# For a copy of the GNU General Public License, see                            #
# <http://www.gnu.org/licenses/>.                                              #
#                                                                              #
################################################################################

Usage:
    jingbao-fuwuqi [options]

Options:
    -h, --help         display help message
    --version          display version and exit
    -s, --system=NAME  system requested [default: KS-1]
"""

name    = "jingbao-fuwuqi"
version = "2016-04-04T1621Z"

import docopt
import os
import sys
import subprocess
import time
import requests
from bs4 import BeautifulSoup

def main(options):
    time_check       = 30
    system_name      = options["--system"]
    #URL              = "https://www.kimsufi.com/en/"
    URL              = "https://www.kimsufi.com/en/servers.xml"
    unavailable_text = "Last server delivered"
    message_alert    = "--- ALERT: system {system_name} available now ---".format(
        system_name = system_name
    )
    while True:
        print("check availability of system {system_name} on page {URL}".format(
            system_name = system_name,
            URL         = URL
        ))
        request     = requests.get(URL)
        page_source = request.text
        soup        = BeautifulSoup(page_source)
        table       = soup.find("table", {"class": "full homepage-table"})
        table_rows  = []
        # Load the table of systems.
        for row in table.find_all("tr"):
            table_rows.append(row)
        # Find the row of the system requested.
        for row in table_rows:
            if system_name in row.text:
                system_row = row
                print("    system {system_name} information detected".format(
                    system_name = system_name
                ))
        # Check if the system requested is not unavailable.
        if unavailable_text not in system_row.text:
            alert(message_alert)
        else:
            print("    system {system_name} unavailable".format(
                system_name = system_name
            ))
        # Wait a time before checking the page again.
        print("    wait {time} seconds before checking again".format(
            time = time_check
        ))
        time.sleep(time_check)

def alert(message):
    print(message)
    speak(message)

def speak(text):
    command =\
        "echo \"" +\
        text      +\
        "\" | festival --tts"
    result = subprocess.check_call(
        command,
        shell      = True,
        executable = "/bin/bash"
    )

if __name__ == "__main__":
    options = docopt.docopt(__doc__)
    if options["--version"]:
        print(version)
        exit()
    main(options)
