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
    pass

class DockerContainerItem:
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
    DOCKER_CMD_PATH = "/usr/bin/docker"
    DOCKER_CMD_TIMEOUT_SECS = 60
    DOCKER_APPEND_JSON_FORMAT_STR = "--format={{json .}}"

    @staticmethod
    def StopContainer(name: str):
        Docker.RunDockerCommand(["stop", name], json=False)

    @staticmethod
    def RestartContainer(name: str):
        Docker.RunDockerCommand(["restart", name], json=False)

    @staticmethod
    def DeleteContainer(name: str):
        Docker.RunDockerCommand(["rm", "-f", name], json=False)

    @staticmethod
    def IsContainerExists(name: str, containerList: List[DockerContainerItem] = None) -> bool:
        c = Docker.GetContainer(name, containerList)
        if c is None:
            return False
        return True

    @staticmethod
    def GetContainer(name: str, containerList: List[DockerContainerItem] = None) -> DockerContainerItem:
        if containerList is None:
            containerList = Docker.GetContainerList()

        return FirstOrDefault([x for x in containerList if x.Names == name])

    @staticmethod
    def GetContainerList() -> List[DockerContainerItem]:
        return Docker.RunDockerCommandJson(["ps", "-a"], DockerContainerItem)
    
    @staticmethod
    def RunDockerCommandJsonDebug(argsList: List[str], timeoutSecs=None) -> EasyExecResults:
        res = Docker.RunDockerCommand(argsList, False, timeoutSecs, True)
        data = Json.JsonLinesToDataList(res.StdOut)
        Print(data)
        return res

    @staticmethod
    def RunDockerCommandJson(argsList: List[str], cls: Type[SameType] = None, timeoutSecs=None, exact: bool = False) -> List[SameType]:
        res = Docker.RunDockerCommand(argsList, False, timeoutSecs, True)
        return Json.JsonLinesToObjectList(res.StdOut, cls, exact)

    @staticmethod
    def RunDockerCommand(argsList: List[str], ignoreError: bool = False, timeoutSecs=None, json: bool = True) -> EasyExecResults:
        if timeoutSecs is None:
            timeoutSecs = Docker.DOCKER_CMD_TIMEOUT_SECS
        newArgs = argsList.copy()
        newArgs.insert(0, Docker.DOCKER_CMD_PATH)
        if json:
            newArgs.append(Docker.DOCKER_APPEND_JSON_FORMAT_STR)

        return EasyExec.RunPiped(newArgs, shell=False,
                                 ignoreError=ignoreError, timeoutSecs=timeoutSecs)

    @staticmethod
    def RunDockerCommandInteractive(argsList: List[str], ignoreError: bool = False, timeoutSecs=None):
        if timeoutSecs is None:
            timeoutSecs = Docker.DOCKER_CMD_TIMEOUT_SECS
        newArgs = argsList.copy()
        newArgs.insert(0, Docker.DOCKER_CMD_PATH)

        return EasyExec.Run(newArgs, shell=False,
                                 ignoreError=ignoreError)
