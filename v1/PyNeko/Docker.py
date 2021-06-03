# IPA-DN-PyNeko-v1
#
# Copyright (c) 2021- IPA CyberLab.
# All Rights Reserved.
#
# Author: Daiyuu Nobori
# Docker Utility

from typing import List, Tuple, Dict, Set, Callable, TypeVar, Type
import typing

from ._Imports import *

SameType = TypeVar("SameType")


class DockerConsts:
    _DOCKER_CMD_PATH = "/usr/bin/docker"
    _DOCKER_CMD_TIMEOUT_SECS = 15
    _DOCKER_APPEND_JSON_FORMAT_STR = "--format={{json .}}"


class DockerProcessItem:
    Command: str
    CreatedAt: str
    ID: str
    Image: str
    Labels: str
    LocalVolumes: str
    Mounts: str
    Names: str
    Networks: str
    Ports: str
    RunningFor: str
    Size: str
    State: str
    Status: str

class Docker:

    @staticmethod
    def RunDockerCommand(argsList: List[str], ignoreError: bool = False, timeoutSecs=DockerConsts._DOCKER_CMD_TIMEOUT_SECS, json: bool = True) -> EasyExecResults:
        newArgs = argsList.copy()
        newArgs.insert(0, DockerConsts._DOCKER_CMD_PATH)
        if json:
            newArgs.append(DockerConsts._DOCKER_APPEND_JSON_FORMAT_STR)

        return EasyExec.RunPiped(newArgs, shell=False,
                                 ignoreError=ignoreError, timeoutSecs=timeoutSecs)
    
    @staticmethod
    def RunDockerCommandJsonDebug(argsList: List[str], timeoutSecs=DockerConsts._DOCKER_CMD_TIMEOUT_SECS) -> EasyExecResults:
        res = Docker.RunDockerCommand(argsList, False, timeoutSecs, True)
        data = Json.JsonLinesToDataList(res.StdOut)
        Print(data)
        return res

    @staticmethod
    def RunDockerCommandJson(argsList: List[str], cls: Type[SameType] = None, timeoutSecs=DockerConsts._DOCKER_CMD_TIMEOUT_SECS, exact: bool = False) -> List[SameType]:
        res = Docker.RunDockerCommand(argsList, False, timeoutSecs, True)
        return Json.JsonLinesToObjectList(res.StdOut, cls, exact)

    
