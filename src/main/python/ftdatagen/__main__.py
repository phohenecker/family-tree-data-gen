#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Launches the generator for creating family tree datasets."""


import os
import random

import argmagic
import streamtologger

from ftdatagen import config
from ftdatagen import generator


__author__ = "Patrick Hohenecker"
__copyright__ = (
        "Copyright (c) 2018, Patrick Hohenecker\n"
        "All rights reserved.\n"
        "\n"
        "Redistribution and use in source and binary forms, with or without\n"
        "modification, are permitted provided that the following conditions are met:\n"
        "\n"
        "1. Redistributions of source code must retain the above copyright notice, this\n"
        "   list of conditions and the following disclaimer.\n"
        "2. Redistributions in binary form must reproduce the above copyright notice,\n"
        "   this list of conditions and the following disclaimer in the documentation\n"
        "   and/or other materials provided with the distribution.\n"
        "\n"
        "THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS \"AS IS\" AND\n"
        "ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED\n"
        "WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE\n"
        "DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR\n"
        "ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES\n"
        "(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;\n"
        "LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND\n"
        "ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT\n"
        "(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS\n"
        "SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE."
)
__license__ = "BSD-2-Clause"
__version__ = "2018.1"
__date__ = "May 30, 2018"
__maintainer__ = "Patrick Hohenecker"
__email__ = "mail@paho.at"
__status__ = "Development"


APP_NAME = "run-data-gen.sh"
"""str: The name that is displayed in the synopsis of this application."""

APP_DESCRIPTION = (
        "This is a tool for generating datasets of reasoning tasks about family trees. "
        "For additional details, have a look at the project repository at "
        "https://github.com/phohenecker/family-tree-data-gen."
)
"""str: The description that is displayed in this application's help text."""

LOG_FILE_HEADER = "[{timestamp:%Y-%m-%d %H:%M:%S} - {level:6}]  "
"""str: The header that starts every line of the log file."""

LOG_FILE_NAME = "out.log"
"""str: The name of the log file."""


def _print_config(conf: config.Config) -> None:
    """Prints the provided configuration as table to the screen.

    Args:
        conf (:class:`config.Config`): The configuration to print.
    """
    # parse and sort the config into (name, value) pairs
    str_conf = sorted(argmagic.get_config(conf).items(), key=lambda x: x[0])
    
    # compute the maximum (string) lengths of all names and values, respectively
    max_name_len = max((len(n) for n, _ in str_conf))
    max_value_len = max((len(v) for _, v in str_conf))
    
    # assemble a horizontal separator
    h_line = "=" * (max_name_len + max_value_len + 3)
    
    # print the config to the screen
    print(h_line)
    print("CONFIGURATION")
    print(h_line)
    for name, value in str_conf:
        print(("{:" + str(max_name_len) + "} : {}").format(name, value))
    print(h_line)
    print()


def main(conf: config.Config):
    
    # create output directory if it does not exist yet
    if not os.path.isdir(conf.output_dir):
        os.mkdir(conf.output_dir)
    
    # set up logging
    streamtologger.redirect(
            os.path.join(conf.output_dir, LOG_FILE_NAME),
            print_to_screen=not conf.quiet,
            append=False,
            header_format=LOG_FILE_HEADER
    )
    
    # seed RNG
    random.seed(conf.seed)
    
    # print user-defined configuration to screen
    _print_config(conf)
    
    # run generator
    generator.Generator.generate(conf)


main(argmagic.parse_args(config.Config, app_name=APP_NAME, app_description=APP_DESCRIPTION, positional_args=True))
