from typing import Literal

from pydantic import BaseModel


class LuaBoolean(BaseModel):
    type: Literal["boolean"] = "boolean"
    value: bool


class LuaString(BaseModel):
    type: Literal["string"] = "string"
    value: str


class LuaNumber(BaseModel):
    type: Literal["number"] = "number"
    value: int | float


class LuaNil(BaseModel):
    type: Literal["nil"] = "nil"


class LuaTableReference(BaseModel):
    table_id: str


LuaKey = LuaBoolean | LuaString | LuaNumber | LuaTableReference
LuaValue = LuaKey | LuaNil


class LuaTableEntry(BaseModel):
    key: LuaKey
    value: LuaValue


class LuaResult(BaseModel):
    tables: dict[str, list[LuaTableEntry]] = {}
    root: LuaValue


class ErrorResult(BaseModel):
    error_type: str
    error_msg: str
