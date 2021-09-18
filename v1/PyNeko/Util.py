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
import secrets
import random

from typing import List, Tuple, Dict, Set, Callable, TypeVar, Type
from datetime import timedelta, tzinfo, timezone, time, date, datetime

from ._Imports import *

SameType = TypeVar("SameType")


def FirstOrDefault(seq, default: any = None):
    if hasattr(seq, "__len__"):
        if len(seq) == 0:
            return default
        return seq[0]
    else:
        i = iter(seq)
        try:
            return i.next()
        except StopIteration:
            return default


def First(seq):
    if hasattr(seq, "__len__"):
        if len(seq) == 0:
            raise Err(f"First(): no elements.")
        return seq[0]
    else:
        i = iter(seq)
        try:
            return i.next()
        except StopIteration:
            raise Err(f"First(): no elements.")


def Single(seq):
    if hasattr(seq, "__len__"):
        if len(seq) != 1:
            raise Err(f"Single(): len != 1. len = {len(seq)}")
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


class Time:
    TIMEZONE_UTC: timezone = timezone.utc
    TIMEZONE_LOCAL: timezone = datetime.now(
        timezone.utc).astimezone().tzinfo
    TIME64_BASE: datetime = datetime(1970, 1, 1, 9, 0, 0, 0, timezone.utc)
    TICK64_NS_START_BASE: int = systime.perf_counter_ns()

    @staticmethod
    def NowUtc() -> datetime:
        return datetime.now(Time.TIMEZONE_UTC)

    @staticmethod
    def NowLocal() -> datetime:
        return Time.ToLocal(Time.NowUtc())
    
    @staticmethod
    def Now(tz: timezone = None) -> datetime:
        if tz is None:
            tz = Time.TIMEZONE_LOCAL
        return Time.ToTimezone(Time.NowUtc(), tz)

    @staticmethod
    def ToTimezone(src: datetime, tz: timezone) -> datetime:
        return src.astimezone(tz)

    @staticmethod
    def ToLocal(utcDt: datetime) -> datetime:
        return Time.ToTimezone(utcDt, Time.TIMEZONE_LOCAL)

    @staticmethod
    def ToUtc(dt: datetime) -> datetime:
        return Time.ToTimezone(dt, Time.TIMEZONE_UTC)

    @staticmethod
    def ToTime64(dt: datetime) -> int:
        delta = dt - Time.TIME64_BASE
        ms = int(delta.total_seconds() * 1000)
        return Time._SafeTime64(ms)

    @staticmethod
    def FromTime64(ms: int, local: bool = False) -> datetime:
        ms = Time._SafeTime64(ms)
        delta = timedelta(milliseconds=ms)
        ret = Time.TIME64_BASE + delta
        if local:
            ret = Time.ToLocal(ret)
        return ret

    @staticmethod
    def _SafeTime64(ms: int) -> int:
        ms = int(ms)
        ms = max(ms, 0)  # 西暦 1970 年から
        ms = min(ms, 253370732400000)  # 西暦 9999 年まで
        return ms
    
    @staticmethod
    def Tick64() -> int:
        return max(int((systime.perf_counter_ns() - Time.TICK64_NS_START_BASE) / 1000000.0) + 1, 1)

    @staticmethod
    def FloatTick64() -> int:
        return float(max(systime.perf_counter_ns() - Time.TICK64_NS_START_BASE + 1, 1)) / 1000000000.0

    @staticmethod
    def Sleep(ms: int):
        sec = float(ms) / 1000.0
        systime.sleep(sec)

    @staticmethod
    def ToYYYYMMDD(dt: datetime) -> str:
        return dt.strftime("%Y%m%d")

    @staticmethod
    def ToHHMMSS(dt: datetime) -> str:
        return dt.strftime("%H%M%S")

    @staticmethod
    def ToYYYYMMDDHHMMSS(dt: datetime) -> str:
        return Time.ToYYYYMMDD(dt) + Time.ToHHMMSS(dt)

    @staticmethod
    def ToYYYYMMDD_HHMMSS(dt: datetime) -> str:
        return Time.ToYYYYMMDD(dt) + "_" + Time.ToHHMMSS(dt)

    @staticmethod
    def NowYYYYMMDD() -> str:
        return Time.ToYYYYMMDD(Time.NowLocal())
    
    @staticmethod
    def NowYYYYMMDDHHMMSS() -> str:
        return Time.ToYYYYMMDDHHMMSS(Time.NowLocal())
    
    @staticmethod
    def NowYYYYMMDD_HHMMSS() -> str:
        return Time.ToYYYYMMDD_HHMMSS(Time.NowLocal())


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
    
    # 複数の文字列を置換する
    @staticmethod
    def ReplaceMultiStr(src: str, replaceList: Dict[str, str], caseSensitive: bool = False) -> str:
        src = Str.NonNull(src)
        for key, value in replaceList.items():
            src = Str.ReplaceStr(src, key, value, caseSensitive)
        return src

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

        if Util.IsTypeOf(object, Exception):
            return F"{object}"

        if Util.IsSimpleValue(object):
            return str(object)

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
    def GetFirstFilledLine(src: str) -> str:
        src = Str.GetStr(src)
        lines = Str.GetLines(src, removeEmpty=True, trim=True)
        for line in lines:
            return line
        return ""

    @staticmethod
    def OneLine(src: str, splitStr: str = " / ", removeEmpty: bool = True) -> str:
        src = Str.GetStr(src)
        lines = Str.GetLines(src, removeEmpty=True, trim=True)
        return Str.Combine(lines, splitStr, removeEmpty)
    
    @staticmethod
    def NormalizeFqdn(src: str) -> str:
        s = Str.Trim(src).lower()
        tokens = s.split(".")
        o: List[str] = list()
        for token in tokens:
            if Str.IsFilled(token):
                for c in token:
                    if not ((c >= "a" and c <= "z") or (c >= "0" and c <= "9") or c == "-" or c == "_"):
                        raise Err(f"Invalid FQDN: '{src}'")
                o.append(token)
        ret = Str.Combine(o, ".", removeEmpty=True)
        if Str.IsEmpty(ret):
            raise Err(f"Invalid FQDN: '{src}'")
        return ret
    
    @staticmethod
    def DecodeUtf8(src: bytes) -> str:
        if Util.IsNull(src):
            return ""
        return Str.NonNull(src.decode("utf-8"))
    
    @staticmethod
    def EncodeUtf8(src: str) -> bytes:
        src = Str.NonNull(src)
        return src.encode("utf-8")

def Print(obj: any) -> str:
    s = Str.GetStr(obj)
    print(s)
    return s

def PrintLog(obj:any) -> str:
    s = Str.GetStr(obj)
    print(f"{Time.NowLocal()}: {s}")
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
    def IsBinary(object: any) -> bool:
        return Util.IsType(object, "bytes")

    @staticmethod
    def IsClass(object: any) -> bool:
        return hasattr(object, "__dict__")

    @staticmethod
    def IsPrimitive(object: any) -> bool:
        if Util.IsNull(object):
            return True
        return isinstance(object, (int, float, bool, str, bytes, bytearray, memoryview))

    @staticmethod
    def IsSimpleValue(object: any) -> bool:
        if Util.IsPrimitive(object):
            return True
        return isinstance(object, (datetime))

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
    
    @staticmethod
    def GenRandInterval(standard: float, plusMinusPercentage: float = 30.0) -> float:
        rate = plusMinusPercentage * (Rand.SInt31() % 10000) / 10000.0 / 100.0
        v = standard * rate
        if (v == 0.0):
            return standard
        b = Rand.Bool()
        if b:
            ret = standard + standard * rate
        else:
            ret = standard - standard * rate
        return max(ret, 0.001)
    
    @staticmethod
    def GetSingleHostCertAndIntermediateCertsFromCombinedCert(src: str) -> Tuple[str, str]:
        lines = Str.GetLines(src, trim=True)
        flag = 0

        cert0_body = ""
        cert1_body = ""

        current_cert = ""
        cert_index = 0

        for line in lines:
            if line == "-----BEGIN CERTIFICATE-----":
                flag = 1
                current_cert += line + "\n"
            elif line == "-----END CERTIFICATE-----":
                flag = 0
                current_cert += line + "\n"
                if cert_index == 0:
                    cert0_body = current_cert
                else:
                    cert1_body += current_cert
                    cert1_body += "\n"
                cert_index += 1
                current_cert = ""
            else:
                if flag == 1:
                    current_cert += line + "\n"
        
        return (cert0_body, cert1_body)

       


class EasyExecResults:
    Result: subprocess.CompletedProcess
    IsOk: bool
    StdOut: str
    StdErr: str
    StdOutAndErr: str
    ExitCode: int
    Cmd: List[str]

    def InitFromCompletedProcess(self, res: subprocess.CompletedProcess, cmd: List[str]):
        self.Result = res
        self.ExitCode = res.returncode
        self.IsOk = (res.returncode == 0)
        self.StdOut = Str.ToStr(res.stdout)
        self.StdErr = Str.ToStr(res.stderr)
        self.StdOutAndErr = self.StdOut + "\n" + self.StdErr + "\n"
        self.Cmd = cmd

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
    # 注意! timeoutSecs でタイムアウトを指定し、タイムアウト発生時には kill するためには、shell = False にしなければならない。
    def Run(command: List[str], shell: bool = True, ignoreError: bool = False, timeoutSecs: int = None):
        if shell and timeoutSecs is not None:
            raise Err("shell == True and timeoutSecs is not None.")

        res = subprocess.run(command, shell=shell,
                             encoding="utf-8", text=True, timeout=timeoutSecs)
        
        if not ignoreError:
            res.check_returncode()

    @staticmethod
    # 注意! timeoutSecs でタイムアウトを指定し、タイムアウト発生時には kill するためには、shell = False にしなければならない。
    def RunPiped(command: List[str], shell: bool = True, ignoreError: bool = False, timeoutSecs: int = None) -> EasyExecResults:
        if shell and timeoutSecs is not None:
            raise Err("shell == True and timeoutSecs is not None.")

        res = subprocess.run(command, shell=shell, encoding="utf-8", text=True,
                             timeout=timeoutSecs, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        ret = EasyExecResults()
        ret.InitFromCompletedProcess(res, command)

        if not ignoreError:
            ret.ThrowIfError()

        return ret

    @staticmethod
    def RunBackground(command: List[str], shell: bool = True, cwd: str = None, stdin=None, stdout=None, stderr=None) -> subprocess.Popen:
        res = subprocess.Popen(command, shell=shell, text=True,
                               cwd=cwd, stdin=stdin, stdout=stdout, stderr=stderr)

        return res

class Rand:
    @staticmethod
    def SInt31() -> int:
        return secrets.randbelow(2147483648)
    
    @staticmethod
    def Bool() -> bool:
        b = Rand.SInt31()
        if (b % 2) == 1:
            return True
        return False


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

class OpenSslUtil:

    @staticmethod
    def OcspIsCertificateRevokedInternal(certPath: str, interPath: str) -> bool:
        url = GetOcspServerUrlFromCert(certPath)

        res = EasyExec.RunPiped(
            F"openssl ocsp -issuer {interPath} -cert {certPath} -text -url {url}".split(),
            shell=False,
            timeoutSecs=15)

        lines = Str.GetLines(res.StdOutAndErr)

        for line in lines:
            if (Str.InStr(line, "Cert Status: revoked")):
                return True

        return False


    @staticmethod
    def OcspIsCertificateRevoked(certPath: str, interPath: str) -> bool:
        try:
            Print(F"Checking OCSP for '{certPath}' ...")
            ret = OcspIsCertificateRevokedInternal(certPath, interPath)
            Print(F"OCSP Result: Is revoked: {ret}")
            return ret
        except:
            Print(F"OCSP Check Error.")
            return False
