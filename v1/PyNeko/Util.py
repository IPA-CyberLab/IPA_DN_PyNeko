# IPA-DN-PyNeko-v1
#
# Copyright (c) 2021- IPA CyberLab.
# All Rights Reserved.
#
# Author: Daiyuu Nobori
# ユーティリティ

import os
import json
import subprocess
from typing import List, Tuple, Dict, Set
import typing

from ._Imports import *


class Err(Exception):
    pass
    

class Str:
    @staticmethod
    def IsNull(str: str) -> bool:
        return Util.IsNull(str)

    @staticmethod
    def IsNonNull(str: str) -> bool:
        return not Str.IsNull(str)

    @staticmethod
    def ToStr(str: any) -> str:
        if Util.IsNull(str):
            return ""

        if Util.IsType(str, "str"):
            return str

        return F"{str}"

    @staticmethod
    def NonNull(str: str) -> str:
        if Str.IsNull(str):
            return ""

        return str

    @staticmethod
    def StrToInt(str: str) -> int:
        try:
            if Str.IsNull(str):
                return 0
            i = int(str)
            return i
        except:
            return 0

    @staticmethod
    def Trim(str: str) -> str:
        return Str.NonNull(str).strip()

    @staticmethod
    def IsEmpty(str: str) -> bool:
        if Str.Len(Str.Trim(str)) == 0:
            return True
        return False

    @staticmethod
    def IsFilled(str: str) -> bool:
        return not Str.IsEmpty(str)

    @staticmethod
    def Len(str: str) -> int:
        if Str.IsNull(str):
            return 0

        return len(str)

    @staticmethod
    def ToBool(str: str) -> bool:
        i = Str.StrToInt(str)
        if i != 0:
            return True

        tmp = Str.Trim(str).lower()

        if Str.Len(tmp) >= 1:
            if tmp[0] == 'y' or tmp[0] == 't':
                return True
            if tmp.startswith("ok") or tmp.startswith("on") or tmp.startswith("enable"):
                return True

        return False

    @staticmethod
    def GetStr(object: any) -> str:
        if object is None:
            return "None"

        if Util.IsTypeOf(object, str):
            return object

        return Json.ObjectToJson(object)

def Print(obj: any) -> str:
    s = Str.GetStr(obj)
    print(s)
    return s

class Util:
    @staticmethod
    def ToBool(object: any) -> bool:
        if Util.IsType(object, "str"):
            return Str.ToBool(str)

        if not (object):
            return False

        return True

    @staticmethod
    def IsNull(object: any) -> bool:
        if object is None:
            return True

        return False

    @staticmethod
    def GetTypeName(object: any) -> str:
        return type(object).__name__

    @staticmethod
    def IsType(object: any, typeName: str) -> bool:
        if Util.GetTypeName(object) == typeName:
            return True

        return False
    
    @staticmethod
    def IsTypeOf(object: any, baseType: type) -> bool:
        return isinstance(object, baseType)
    
    @staticmethod
    def IsClass(object: any) -> bool:
        return hasattr(object, "__dict__")
    
    @staticmethod
    def IsPrimitive(object: any) -> bool:
        if Util.IsNull(object): return True
        return isinstance(object, (int, float, bool, str, bytes, bytearray, memoryview))

    @staticmethod
    def GetClassAttributes(object: any) -> dict:
        if Util.IsClass(object):
            return object.__dict__
        raise Err("Not a class object.")
    
    @staticmethod
    def GetClassAttributesOrItself(object: any):
        if Util.IsClass(object):
            return Util.GetClassAttributes(object)
        return object


class EasyExecResults:
    def __init__(self):
        self.Result: subprocess.CompletedProcess = None
        self.IsOk: bool = False
        self.StdOut: str = ""
        self.StdErr: str = ""
        self.StdOutAndErr: str = ""
        self.ExitCode: int = -1

    def InitFromCompletedProcess(self, res: subprocess.CompletedProcess):
        self.Result = res
        self.ExitCode = res.returncode
        self.IsOk = (res.returncode == 0)
        self.StdOut = Str.ToStr(res.stdout)
        self.StdErr = Str.ToStr(res.stderr)
        self.StdOutAndErr = self.StdOut + "\n" + self.StdErr + "\n"

    def ThrowIfError(self):
        self.Result.check_returncode()


class EasyExec:
    @staticmethod
    def Run(command: str, shell: bool = True, ignoreError: bool = False, timeoutSecs: int = None):
        res = subprocess.run(command, shell=shell,
                             encoding="utf-8", text=True, timeout=timeoutSecs)

        if not ignoreError:
            res.check_returncode()

    @staticmethod
    def RunPiped(command: str, shell: bool = True, ignoreError: bool = False, timeoutSecs: int = None) -> EasyExecResults:
        res = subprocess.run(command, shell=shell, encoding="utf-8", text=True,
                             timeout=timeoutSecs, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        ret = EasyExecResults()
        ret.InitFromCompletedProcess(res)

        if not ignoreError:
            ret.ThrowIfError()

        return ret

    @staticmethod
    def RunBackground(command: str, shell: bool = True) -> subprocess.Popen:
        res = subprocess.Popen(command, shell=shell, text=True)

        return res


class Json:
    @staticmethod
    def ObjectToJson(obj: any, compact: bool = False, skipKeys: bool = False) -> str:
        return Str.NonNull(json.dumps(obj, indent=1 if not compact else None, skipkeys=skipKeys, default=Util.GetClassAttributesOrItself))
    
    @staticmethod
    def JsonToData(str: str):
        return json.loads(str)



