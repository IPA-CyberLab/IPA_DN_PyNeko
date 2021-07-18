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

    def Get(self, url: str, ignoreError: bool = False) -> HttpResponse:
        r = requests.get(url, timeout=self.TimeoutSecs)
        if not ignoreError:
            r.raise_for_status()
        ret = HttpResponse()
        ret.Code = r.status_code
        ret.Body = Str.DecodeUtf8(r.content)
        return ret
    
    def Post(self, url: str, postData: str, ignoreError: bool = False) -> HttpResponse:
        r = requests.post(url, data=Str.EncodeUtf8(
            postData), timeout=self.TimeoutSecs)
        if not ignoreError:
            r.raise_for_status()
        ret = HttpResponse()
        ret.Code = r.status_code
        ret.Body = Str.DecodeUtf8(r.content)
        return ret

        


