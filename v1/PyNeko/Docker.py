# IPA-DN-PyNeko-v1
#
# Copyright (c) 2021- IPA CyberLab.
# All Rights Reserved.
#
# Author: Daiyuu Nobori
# Docker Utility

from typing import List, Tuple, Dict, Set
import typing

from ._Imports import *

class DockerConsts:
    _DOCKER_CMD_PATH = "/usr/bin/docker"
    _DOCKER_CMD_TIMEOUT_SECS = 15
    _DOCKER_APPEND_JSON_FORMAT_STR = "--format='{{json .}}'"

class Docker:

    @staticmethod
    def RunDockerCommand(argsList: List[str], ignoreError=False, timeoutSecs=DockerConsts._DOCKER_CMD_TIMEOUT_SECS) -> EasyExecResults:
        newArgs = argsList.copy()
        newArgs.insert(0, DockerConsts._DOCKER_CMD_PATH)
        newArgs.append(DockerConsts._DOCKER_APPEND_JSON_FORMAT_STR)

        return EasyExec.RunPiped(newArgs, shell=False,
                                 ignoreError=ignoreError, timeoutSecs=timeoutSecs)

    
