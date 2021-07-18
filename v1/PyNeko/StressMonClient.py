#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 
# IPA-DN-PyNeko-v1
#
# Copyright (c) 2021- IPA CyberLab.
# All Rights Reserved.
#
# Author: Daiyuu Nobori
# StressMon Client

import os
import json
import subprocess
import inspect
import typing
import time as systime
from typing import List, Tuple, Dict, Set, Callable, TypeVar, Type
from datetime import timedelta, tzinfo, timezone, time, date, datetime

from ._Imports import *

SameType = TypeVar("SameType")

class StressMonClient:
    BaseUrl = "http://nd-stressmon-server.ipantt.net:7010/"
    HostName = Env.GetHostName()

    def Report(self, body: str):
        hc = HttpClient()
        r = hc.Post(self.BaseUrl + "?hostname=" + self.HostName, body)



