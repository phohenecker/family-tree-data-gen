#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from distutils.core import setup


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
__license__ = "Simplified BSD License"
__version__ = "2018.1"
__date__ = "May 28, 2018"
__maintainer__ = "Patrick Hohenecker"
__email__ = "mail@paho.at"
__status__ = "Development"


# read the long description from the read me file
long_description = open("README.md").read()

setup(
        author="Patrick Hohenecker",
        author_email="mail@paho.at",
        classifiers=[
                "Programming Language :: Python :: 3"
        ],
        copyright="Copyright (c) 2018 Patrick Hohenecker",
        data_files=[
                (".", ["LICENSE", "README.md"])
        ],
        description="A dataset generator for family tree data.",
        download_url="https://github.com/phohenecker/family-tree-data-gen/archive/v2018.1.tar.gz",
        install_requires=[
                "argmagic>=2017.1",
                "aspwrapper>=2018.1",
                "insanity>=2017.1",
                "reldata>=2017.1",
                "streamtologger>=2017.1"
        ],
        license="Simplified BSD License",
        long_description=long_description,
        name="ftdatagen",
        package_dir={"": "src/main/python"},
        packages=["ftdatagen"],
        python_requires=">=3",
        url="https://github.com/phohenecker/family-tree-data-gen",
        version="2018.1"
)
