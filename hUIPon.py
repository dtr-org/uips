#!/usr/bin/env python3
# Copyright (c) 2018 The Unit-e developers
# Distributed under the MIT software license, see the accompanying
# file COPYING or http://www.opensource.org/licenses/mit-license.php.
#
# This is an adation of hADRon.py
# (https://github.com/dtr-org/unit-e-docs/blob/master/adrs/hADRon.py)

import os
import re

"""A simple script that generates a TOC for all the UIPs"""


class HUIPon:

    def __init__(self):
        pass


    def generate(self):
        toc_filename = "README.md"
        lines =[]
        with open(toc_filename, "r") as toc_file:
            found_table = False
            for line in toc_file:
                if line.startswith('|'):
                    if not found_table:
                        lines += self.generate_table()
                        found_table = True
                else:
                    lines.append(line.rstrip())
        with open(toc_filename, "w") as toc_file:
            for l in lines:
                toc_file.write(l + "\n")

    def generate_table(self):
        header = "| UIP | Title | Status | Created |"
        sub_h = "|---|---|:---:|:---:|"

        lines = [header, sub_h]
        uips = self.list_uips()

        for uip in uips:
            num = "[" + uip[:-3] + "](https://github.com/dtr-org/uips/blob/master/" + uip + ")"
            with open(uip, "r") as file:
                title = ""
                status = ""
                created = ""
                complete = False
                for i in range(1, 10):
                    next_line = file.readline()

                    if not title and re.match("^# UIP-[0-9]*[: ].*$", next_line):
                        title = re.search("^# UIP-[0-9]*[: ](.*)$", next_line).group(1).strip()

                    if not status and re.match("^Status:.*$", next_line):
                        status = re.search("^Status:(.*)$", next_line).group(1).strip()

                    if not created and re.match("^Created:.*$", next_line):
                        created = re.search("^Created:(.*)$", next_line).group(1).strip()
                        complete = True
                        break

                if not complete:
                    raise Exception("Cannot parse file: " + uip)

            new_entry = "|" + num + "|" + title + "|" + status + "|" + created + "|"
            lines.append(new_entry)

        return lines


    def list_uips(self):
        uips = []
        for filename in os.listdir("."):
            if re.match("^UIP-[0-9]{4}\.md", filename) and filename != "UIP-0000.md":
                uips.append(filename)

        uips.sort(key=lambda a: int(re.search("^UIP-([0-9]{4})\.md", a).group(1)))
        return uips


if __name__ == '__main__':
    os.chdir(os.path.dirname(__file__))
    HUIPon().generate()
