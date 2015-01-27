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
    -h, --help          display this help message.
    --version           display version and exit
    -s, --system=NAME   system requested [default: KS-1]
"""

name    = "jingbao-fuwuqi"
version = "2015-01-27T1429Z"

import docopt
import os
import sys
import subprocess
import time
import requests
from   bs4 import BeautifulSoup

def main(options):
    timeCheck       = 15
    systemName      = options["--system"]
    page            = "https://www.kimsufi.com/en/"
    unavailableText = "replenished"
    messageAlert    = "--- ALERT: system {systemName} available now ---".format(
        systemName  = systemName
    )
    while True:
        print("check availability of system {systemName} on page {page}".format(
            systemName = systemName,
            page       = page
        ))
        request     = requests.get(page)
        pageSource  = request.text
        soup        = BeautifulSoup(pageSource)
        table       = soup.find("table", {"class" : "full homepage-table"})
        tableRows   = []
        # Load the table of systems.
        for row in table.find_all('tr'):
            tableRows.append(row)
        # Find the row of the system requested.
        for row in tableRows:
            if systemName in row.text:
                systemRow = row
                print("    system {systemName} information detected".format(
                    systemName = systemName
                ))
        # Check if the system requested is not unavailable.
        if unavailableText not in systemRow.text:
            alert(messageAlert)
        else:
            print("    system {systemName} unavailable".format(
                systemName = systemName
            ))
        # Wait a time before checking the page again.
        print("    wait {time} seconds before checking again".format(
            time = timeCheck
        ))
        time.sleep(timeCheck)

def alert(message):
    print(message)
    speak(message)

def speak(text):
    command =\
        "echo \"" +\
        text +\
        "\" | festival --tts"
    result = subprocess.check_call(
        command,
        shell = True,
        executable = "/bin/bash"
    )

if __name__ == "__main__":
    options = docopt.docopt(__doc__)
    if options["--version"]:
        print(version)
        exit()
    main(options)
