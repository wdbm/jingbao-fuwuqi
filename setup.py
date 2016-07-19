#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import setuptools
import pypandoc

def main():

    setuptools.setup(
        name             = "jingbao_fuwuqi",
        version          = "2016.07.19.1341",
        description      = "alert when server available",
        long_description = pypandoc.convert("README.md", "rst"),
        url              = "https://github.com/wdbm/jingbao-fuwuqi",
        author           = "Will Breaden Madden",
        author_email     = "w.bm@cern.ch",
        license          = "GPLv3",
        py_modules       = [
                           "jingbao_fuwuqi"
                           ],
        install_requires = [
                           "bs4",
                           "docopt"
                           ],
        scripts          = [
                           "jingbao_fuwuqi.py"
                           ],
        entry_points     = """
            [console_scripts]
            jingbao_fuwuqi = jingbao_fuwuqi:jingbao_fuwuqi
        """
    )

def read(*paths):
    with open(os.path.join(*paths), "r") as filename:
        return filename.read()

if __name__ == "__main__":
    main()
