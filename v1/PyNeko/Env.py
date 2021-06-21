﻿#!/usr/bin/env python3
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
import time as systime
from socket import gethostname
from typing import List, Tuple, Dict, Set, Callable, TypeVar, Type
from datetime import timedelta, tzinfo, timezone, time, date, datetime

from ._Imports import *

class Env:
    @staticmethod
    def GetHostName() -> str:
        s = Str.Trim(gethostname())
        if Str.IsEmpty(s):
            s = "_unknown_"
        return s





