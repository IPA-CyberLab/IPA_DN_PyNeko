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


class Util:

    @staticmethod
    # シェルコマンドの実行
    def ShellExecute(command: str, ignoreError: bool = False):
        res = subprocess.run(command, shell=True, encoding="utf-8", text=True)

        if not ignoreError:
            res.check_returncode()


