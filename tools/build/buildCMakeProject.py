#!/usr/bin/env python
# Eclipse SUMO, Simulation of Urban MObility; see https://eclipse.org/sumo
# Copyright (C) 2017-2018 German Aerospace Center (DLR) and others.
# This program and the accompanying materials
# are made available under the terms of the Eclipse Public License v2.0
# which accompanies this distribution, and is available at
# http://www.eclipse.org/legal/epl-v20.html

# @file    buildCMakeProject.py
# @author  Pablo Alvarez Lopez
# @date    2017
# @version $Id$

from __future__ import absolute_import
from __future__ import print_function

import os
import sys
import subprocess
import shutil

SUMO_HOME = os.environ.get("SUMO_HOME", os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

# First check that CMake was correctly installed
if "cmake" in os.environ["PATH"].lower():
    print("""CMake executable wasn't found.
    Please install the last version of Cmake from https://cmake.org/download/,
    or add the folder of cmake executable to PATH""")
else:
    # start to find libraries
    print("Searching libraries...")

    # obtain all path of folder
    pathFolders = os.environ["PATH"].split(os.pathsep)
    if os.path.exists(os.path.join(SUMO_HOME, "lib"))
        pathFolders += os.listdir(os.path.join(SUMO_HOME, "lib"))

    # iterate over folder of path
    for folder in pathFolders:
        if "fox-1.6" in folder.lower():
            os.environ["FOX_DIR"] = folder[:-3]
            os.environ["FOX_LIBRARY"] = folder
            os.environ["FOX_INCLUDE_DIR"] = folder[:-3] + "include"
        elif "xerces-c-3" in folder.lower():
            os.environ["XERCES_BIN"] = folder
            os.environ["XERCES_INCLUDE"] = folder[:-3] + "include"
            os.environ["XERCES_LIB"] = folder[:-3] + "lib"
        elif "proj_gdal" in folder.lower():
            os.environ["GDAL_BIN"] = folder
            os.environ["GDAL_INCLUDE"] = folder[:-3] + "include"
            os.environ["GDAL_LIB"] = folder[:-3] + "lib"
        elif "python27" in folder.lower() and "scripts" not in folder.lower():
            os.environ["PYTHON_LIB"] = folder + "libs\python27.lib"
            os.environ["PYTHON_INCLUDE"] = folder + "include"
        elif "python36" in folder.lower() and "scripts" not in folder.lower():
            os.environ["PYTHON_LIB"] = folder + "libs\python36.lib"
            os.environ["PYTHON_INCLUDE"] = folder + "include"

    generator = sys.argv[1] if len(sys.argv) > 1 else "Visual Studio 14 2015 Win64"
    buildDir = os.path.join(SUMO_HOME, "cmake-build-" + generator.replace(" ", "-"))
    # Create directory or clear it if already exists
    if os.path.exists(buildDir):
        print ("Cleaning directory of", generator)
        shutil.rmtree(buildDir)
    os.makedirs(buildDir)
    print ("Creating solution for", generator)
    subprocess.call(["cmake", "..", "-G", generator], cwd=buildDir)
