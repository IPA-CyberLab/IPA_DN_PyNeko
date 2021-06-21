#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 
# IPA-DN-PyNeko-v1
#
# Copyright (c) 2021- IPA CyberLab.
# All Rights Reserved.
#
# Author: Daiyuu Nobori
# ユーティリティ
# 2021/06/02 に生まれて初めて書いたインチキ Python スクリプト！！

import os
import json
import subprocess
import inspect
import typing
import time as systime
import requests
import urllib.request

from typing import List, Tuple, Dict, Set, Callable, TypeVar, Type
from datetime import timedelta, tzinfo, timezone, time, date, datetime

from ._Imports import *

SameType = TypeVar("SameType")

class HttpResponse:
    Code: int
    Body: str

class HttpClient:
    TimeoutSecs = 15

    def Get(self, url: str) -> HttpResponse:
        r = urllib.request.urlopen(url, timeout=self.TimeoutSecs)
        ret = HttpResponse()
        ret.Code = r.getcode()
        data = r.read()
        s = Str.DecodeUtf8(data)
        ret.Body = s
        return ret
    
    def Post(self, url: str, postData: str) -> HttpResponse:
        r = urllib.request.urlopen(
            url, timeout=self.TimeoutSecs, data=Str.EncodeUtf8(postData))
        ret = HttpResponse()
        ret.Code = r.getcode()
        data = r.read()
        s = Str.DecodeUtf8(data)
        ret.Body = s
        return ret

        


