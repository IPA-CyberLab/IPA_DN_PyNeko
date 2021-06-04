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
from typing import List, Tuple, Dict, Set, Callable, TypeVar, Type, IO
import typing

from ._Imports import *

class Lfs:
    @staticmethod
    def Open(fn: str, write:bool = False, binary:bool = False) -> IO:
        mode = "r"
        mode += "b" if binary else "t"
        mode += "+" if write else ""
        return open(fn, mode)
    
    @staticmethod
    def ReadAllText(fn: str) -> str:
        with Lfs.Open(fn) as f:
            ret = f.read()
            return Str.NonNull(ret)







