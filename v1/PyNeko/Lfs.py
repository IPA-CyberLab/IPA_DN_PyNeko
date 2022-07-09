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
from typing import List, Tuple, Dict, Set, Callable, TypeVar, Type, IO
import typing
import shutil

from ._Imports import *

class Lfs:
    @staticmethod
    def Open(fn: str, write:bool = False, binary:bool = False) -> IO:
        mode = "r"
        mode += "b" if binary else "t"
        mode += "+" if write else ""
        return open(fn, mode)

    @staticmethod
    def Create(fn: str, binary: bool = False) -> IO:
        mode = "w"
        mode += "b" if binary else "t"
        Lfs._CreateDirectoryForFilePath(fn)
        return open(fn, mode)

    @staticmethod
    def ReadAllText(fn: str) -> str:
        with Lfs.Open(fn) as f:
            ret = f.read()
            return Str.NonNull(ret)
    
    @staticmethod
    def WriteAllText(fn: str, body: str):
        with Lfs.Create(fn) as f:
            f.write(body)
    
    @staticmethod
    def ReadAllData(fn: str) -> bytes:
        with Lfs.Open(fn, binary=True) as f:
            ret = f.read()
            return ret

    @staticmethod
    def WriteAllData(fn: str, body: bytes):
        with Lfs.Create(fn, binary=True) as f:
            f.write(body)

    @staticmethod
    def CreateDirectory(dir: str):
        if Lfs.IsDirectoryExists(dir):
            return
        os.makedirs(dir, exist_ok=True)
    
    @staticmethod
    def IsDirectoryExists(dir: str):
        return os.path.isdir(dir)

    @staticmethod
    def DeleteDirectoryRecursively(dir: str):
        if not Lfs.IsDirectoryExists(dir):
            return
        if Str.IsEmpty(dir) or Str.IsSamei(dir, "/"):
            raise "dir is root dir."
        shutil.rmtree(dir)

    @staticmethod
    def _CreateDirectoryForFilePath(fn: str):
        dirPath = os.path.dirname(fn)
        if Str.IsFilled(dirPath):
            Lfs.CreateDirectory(dirPath)










