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
import inspect
from typing import List, Tuple, Dict, Set, Callable, TypeVar, Type
import typing

from ._Imports import *

SameType = TypeVar("SameType")


def Single(seq):
    if hasattr(seq, "__len__"):
        assert len(seq) == 1
        return seq[0]
    else:
        i = iter(seq)
        try:
            value = i.next()
        except StopIteration:
            raise AssertionError()
        try:
            i.next()
        except StopIteration:
            return value
        else:
            raise AssertionError()


class Err(Exception):
    def __init__(self, str: str):
        pass


class Str:
    NEWLINE_CELF = "\r\n"
    NEWLINE_CR = "\r"
    NEWLINE_LF = "\n"

    # 文字列を大文字・小文字を区別して比較
    @staticmethod
    def IsSame(s1: str, s2: str) -> bool:
        return Str.StrCmp(s1, s2)

    @staticmethod
    def StrCmp(s1: str, s2: str) -> bool:
        s1 = Str.NonNull(s1)
        s2 = Str.NonNull(s2)
        return s1 == s2

    @staticmethod
    def Cmp(s1: str, s2: str) -> int:
        return Str.StrCmpRetInt(s1, s2)

    @staticmethod
    def StrCmpRetInt(s1: str, s2: str) -> int:
        s1 = Str.NonNull(s1)
        s2 = Str.NonNull(s2)
        if (s1 == s2):
            return 0
        if (s1 < s2):
            return 1
        return -1

    # 文字列を大文字・小文字を区別せずに比較
    @staticmethod
    def IsSamei(s1: str, s2: str) -> bool:
        return Str.StrCmpi(s1, s2)

    @staticmethod
    def StrCmpi(s1: str, s2: str) -> bool:
        s1 = Str.NonNull(s1).lower()
        s2 = Str.NonNull(s2).lower()
        return s1 == s2

    @staticmethod
    def Cmpi(s1: str, s2: str) -> int:
        return Str.StrCmpRetInti(s1, s2)

    @staticmethod
    def StrCmpRetInti(s1: str, s2: str) -> int:
        s1 = Str.NonNull(s1).lower()
        s2 = Str.NonNull(s2).lower()
        if (s1 == s2):
            return 0
        if (s1 < s2):
            return 1
        return -1

    # 文字列を置換する
    @staticmethod
    def ReplaceStr(str: str, oldKeyword: str, newKeyword: str, caseSensitive: bool = False) -> str:
        str = Str.NonNull(str)
        if Str.IsNullOrZeroLen(str):
            return ""
        oldKeyword = Str.NonNull(oldKeyword)
        newKeyword = Str.NonNull(newKeyword)
        if Str.IsNullOrZeroLen(oldKeyword):
            return str

        i = 0
        j = 0
        num = 0
        sb = ""

        len_string = len(str)
        len_old = len(oldKeyword)
        len_new = len(newKeyword)

        while True:
            i = Str.SearchStr(str, oldKeyword, i, caseSensitive)
            if i == -1:
                sb += str[j:]
                break
            num += 1
            sb += str[j:i]
            sb += newKeyword

            i += len_old
            j = i

        return sb

    # 文字列を検索する
    @staticmethod
    def SearchStr(str: str, keyword: str, start: int = 0, caseSensitive: bool = False) -> int:
        str = Str.NonNull(str)
        keyword = Str.NonNull(keyword)
        if Str.IsNullOrZeroLen(str) or Str.IsNullOrZeroLen(keyword):
            return -1
        if not caseSensitive:
            str = str.lower()
            keyword = keyword.lower()
        return str.find(keyword, start)

    # 文字列が含まれるか?
    @staticmethod
    def InStr(str: str, keyword: str, caseSensitive: bool = False) -> bool:
        str = Str.NonNull(str)
        keyword = Str.NonNull(keyword)
        if Str.IsNullOrZeroLen(str) or Str.IsNullOrZeroLen(keyword):
            return False
        if not caseSensitive:
            str = str.lower()
            keyword = keyword.lower()
        return keyword in str

    @staticmethod
    def GetLines(src: str, removeEmpty: bool = False, trim: bool = False) -> List[str]:
        ret: List[str] = list()
        for line in Str.NonNull(src).splitlines():
            if trim:
                line = Str.Trim(line)

            if not removeEmpty or Str.IsFilled(line):
                ret.append(line)
        return ret

    @staticmethod
    def IsNullOrZeroLen(str: str) -> bool:
        if Str.IsNull(str) or len(str) == 0:
            return True
        return False

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

    @staticmethod
    def Combine(strList: list, splitStr: str = ", ", removeEmpty: bool = False) -> str:
        ret = ""
        tmpList: List[str] = list()

        for item in strList:
            s = Str.GetStr(item)
            if not removeEmpty or Str.IsFilled(s):
                tmpList.append(s)

        num = len(tmpList)
        for i in range(num):
            ret += tmpList[i]

            if i != (num - 1):
                ret += splitStr

        return ret

    @staticmethod
    def OneLine(src: str, splitStr: str = " / ", removeEmpty: bool = True) -> str:
        src = Str.GetStr(src)
        lines = Str.GetLines(src, removeEmpty=True, trim=True)
        return Str.Combine(lines, splitStr, removeEmpty)


def Print(obj: any) -> str:
    s = Str.GetStr(obj)
    print(s)
    return s


def GetStr(obj: any) -> str:
    return Str.GetStr(obj)


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
        if Util.IsNull(object):
            return True
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
    Result: subprocess.CompletedProcess
    IsOk: bool
    StdOut: str
    StdErr: str
    StdOutAndErr: str
    ExitCode: int
    Cmd: str

    def InitFromCompletedProcess(self, res: subprocess.CompletedProcess, cmd: str):
        self.Result = res
        self.ExitCode = res.returncode
        self.IsOk = (res.returncode == 0)
        self.StdOut = Str.ToStr(res.stdout)
        self.StdErr = Str.ToStr(res.stderr)
        self.StdOutAndErr = self.StdOut + "\n" + self.StdErr + "\n"
        self.Cmd = Str.NonNull(cmd)

    def ThrowIfError(self):
        if not self.IsOk:
            errOneLine = Str.OneLine(self.StdErr)
            outOneLine = Str.OneLine(self.StdOut)
            tmp = f"Command '{self.Cmd}' returned exit code {self.ExitCode}."
            if Str.IsFilled(errOneLine):
                tmp += f" Error string: {errOneLine}"
            if Str.IsFilled(outOneLine):
                tmp += f" Output string: {outOneLine}"

            raise Err(tmp)


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
        ret.InitFromCompletedProcess(res, command)

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

    @staticmethod
    def JsonToObject(str: str, cls: Type[SameType] = None, exact: bool = False) -> SameType:
        if cls is None or cls is any:
            return Json.JsonToData(str)

        data = Json.JsonToData(str)
        return Json._ConvertJsonDataToClassInternal(data, cls, exact)

    @staticmethod
    def JsonLinesToDataList(str: str) -> List[SameType]:
        lines = Str.GetLines(str, removeEmpty=True)
        ret = list()
        for line in lines:
            obj = Json.JsonToData(line)
            ret.append(obj)
        return ret

    @staticmethod
    def JsonLinesToObjectList(str: str, cls: Type[SameType] = None, exact: bool = False) -> List[SameType]:
        lines = Str.GetLines(str, removeEmpty=True)
        ret: List[cls] = list()
        for line in lines:
            obj = Json.JsonToObject(line, cls, exact)
            ret.append(obj)
        return ret

    @staticmethod
    # 参考: https://stackoverflow.com/questions/15476983/deserialize-a-json-string-to-an-object-in-python
    def _ConvertJsonDataToClassInternal(data: any, cls: Type[SameType], exact: bool = False) -> SameType:
        annotations: dict = cls.__annotations__ if hasattr(
            cls, '__annotations__') else None

        if isinstance(cls, typing._GenericAlias):
            # アノテーションとして指定されているものが typing の Generics 型である
            baseClass = cls.__origin__
            if issubclass(baseClass, List):
                # List 型である
                listType = cls.__args__[0]
                instance = list()
                for value in data:
                    instance.append(
                        Json._ConvertJsonDataToClassInternal(value, listType), exact)
                return instance
            elif issubclass(baseClass, Dict):
                # Dict 型である
                keyType = cls.__args__[0]
                valueType = cls.__args__[1]
                instance = dict()
                for key, value in data.items():
                    instance[Json._ConvertJsonDataToClassInternal(
                        key, keyType, exact)] = Json._ConvertJsonDataToClassInternal(value, valueType, exact)
                return instance
            else:
                typeName = baseClass.__name__
                raise Err(f"Unsupported generics: {typeName}")

        elif issubclass(cls, list):
            # アノテーションとして指定されているものが組み込み list 型である
            list_type = cls.__args__[0]
            instance: list = list()
            for value in data:
                instance.append(
                    Json._ConvertJsonDataToClassInternal(value, list_type, exact))
            return instance

        elif issubclass(cls, Dict):
            # アノテーションとして指定されているものが組み込み dict 型である
            key_type = cls.__args__[0]
            val_type = cls.__args__[1]
            instance: dict = dict()
            for key, value in data.items():
                instance[Json._ConvertJsonDataToClassInternal(
                    key, key_type)] = Json._ConvertJsonDataToClassInternal(value, val_type, exact)
            return instance

        else:
            # 指定された型のクラスのインスタンスを生成する
            instance: cls = cls()

            if Util.IsPrimitive(instance):
                # プリミティブな単一の値である
                return data

            # 入力される JSON データの項目を列挙する
            for name, value in data.items():
                # 列挙された項目と同じ名前のアノテーションが存在するかどうか検索する
                field_type = annotations.get(name)

                if not field_type:
                    # アノテーションが見つからない
                    if not exact:
                        setattr(instance, name, value)
                else:
                    if inspect.isclass(field_type) and isinstance(value, (dict, tuple, list, set, frozenset)) and not isinstance(field_type, typing._GenericAlias):
                        # アノテーションによると、型はクラスのインスタンスである
                        setattr(instance, name, Json._ConvertJsonDataToClassInternal(
                            value, field_type, exact))
                    elif isinstance(field_type, typing._GenericAlias):
                        # アノテーションによると、型は Generics のインスタンスである
                        setattr(instance, name, Json._ConvertJsonDataToClassInternal(
                            value, field_type, exact))

                    else:
                        # アノテーションによると、型は str, int 等の普通の型である
                        setattr(instance, name, value)

            return instance
