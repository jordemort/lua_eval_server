from decimal import Decimal
from typing import Literal

from pydantic import BaseModel


class LuaBoolean(BaseModel):
    type: Literal["boolean"]
    value: bool


class LuaString(BaseModel):
    type: Literal["string"]
    value: str


class LuaNumber(BaseModel):
    type: Literal["number"]
    value: Decimal


class LuaUndefined(BaseModel):
    type: Literal["undefined"]


class LuaTableReference(BaseModel):
    table_id: str


LuaKey = LuaBoolean | LuaString | LuaNumber | LuaTableReference
LuaValue = LuaKey | LuaUndefined


class LuaTableEntry(BaseModel):
    key: LuaKey
    value: LuaValue


class EvalOutput(BaseModel):
    session_id: str
    tables: dict[str, list[LuaTableEntry]]
    root: LuaValue


class EvalError(BaseModel):
    error_type: str
    error_msg: str
    line: int | None
    column: int | None
