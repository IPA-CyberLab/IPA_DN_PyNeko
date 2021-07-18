#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# IPA-DN-PyNeko-v1
# 
# Copyright (c) 2021- IPA CyberLab.
# All Rights Reserved.
# 
# Author: Daiyuu Nobori
# Description

import os
import json
import subprocess
import inspect
import typing
import time as time2
from typing import List, Tuple, Dict, Set, Callable, TypeVar, Type

from ._Imports import *

class Kernel:
    @staticmethod
    def Sleep(secs: float):
        time2.sleep(secs)
    
    @staticmethod
    def SleepRandInterval(secs: float, plusMinusPercentage: float = 30.0):
        Kernel.Sleep(Util.GenRandInterval(secs, plusMinusPercentage))







