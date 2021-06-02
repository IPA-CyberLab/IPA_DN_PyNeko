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

from ._Imports import *

class Str:
    @staticmethod
    def IsNull(str:str)->bool:
        return Util.IsNull(str)

    @staticmethod
    def IsNonNull(str:str)->bool:
        return not IsNull(str)
    
    @staticmethod
    def ToStr(str: any) -> str:
        if (Util.IsNull(str)):
            return ""

        if Util.IsType(str, "str"):
            print("a")
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
        if object == None:
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


class EasyExecResults:
    Result: subprocess.CompletedProcess = None
    IsOk: bool = False
    StdOut: str = ""
    StdErr: str = ""
    StdOutAndErr: str = ""
    ExitCode: int = -1

    def InitFromCompletedProcess(self, res: subprocess.CompletedProcess):
        self.Result = res
        self.ExitCode = res.returncode
        self.IsOk = (res.returncode == 0)
        self.StdOut = str(res.stdout)
        self.StdErr = str(res.stderr)
        self.StdOutAndErr = self.StdOut + "\n" + self.StdErr + "\n"

    def ThrowIfError(self):
        self.Result.check_returncode()


class EasyExec:
    @staticmethod
    def ShellExecute(command: str, ignoreError: bool = False, timeoutSecs: int = None):
        res = subprocess.run(command, shell=True, encoding="utf-8", text=True, timeout=timeoutSecs)

        if not ignoreError:
            res.check_returncode()

    @staticmethod
    def ShellExecutePiped(command: str, ignoreError: bool = False, timeoutSecs: int = None) -> EasyExecResults:
        res = subprocess.run(command, shell=True, encoding="utf-8", text=True, timeout=timeoutSecs,stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        ret = EasyExecResults()
        ret.InitFromCompletedProcess(res)

        if not ignoreError:
            ret.ThrowIfError()
        
        return ret



 
