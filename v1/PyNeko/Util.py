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



 
