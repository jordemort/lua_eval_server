import asyncio
from collections.abc import Mapping
from concurrent.futures import ThreadPoolExecutor
from typing import Any, cast

from lupa import LuaRuntime, lua_type  # type: ignore

from lua_eval_server.models import (
    LuaBoolean,
    LuaNil,
    LuaNumber,
    LuaResult,
    LuaString,
    LuaTableEntry,
    LuaTableReference,
    LuaValue,
)


class EvaluatorException(Exception):
    pass


class EvalError(EvaluatorException):
    pass


class UnknownType(EvaluatorException):
    def __init__(self, kind: str, unknown_type: str) -> None:
        self.kind = kind
        self.unknown_type = unknown_type
        super().__init__(f"Unknown {kind} type: {unknown_type}", unknown_type)


class NilKey(EvaluatorException):
    def __init__(self, *args: object) -> None:
        super().__init__("Encounterd a table key that appears to be nil", *args)


class SimpleLuaEvaluator:
    """
    A simple Lua evaluator.

    Expressions are evaluated in a separate thread, to avoid stalling the API server.
    """

    def __init__(self):
        self._executor = ThreadPoolExecutor(max_workers=1)
        self._runtime = LuaRuntime()  # type: ignore
        self._tables: dict[str, list[LuaTableEntry]]

    def _eval(self, expr: str) -> Any:
        try:
            return self._runtime.execute(expr)  # type: ignore
        except Exception as e:
            raise EvalError(f"Error evaluating Lua: {e}") from e

    async def eval(self, expr: str) -> LuaResult:
        self._tables = {}
        value: Any = await asyncio.get_running_loop().run_in_executor(
            self._executor, self._eval, expr
        )
        root = self._decode(value)
        return LuaResult(tables=self._tables, root=root)

    def _decode_python(self, value: Any) -> LuaNil | LuaBoolean | LuaString | LuaNumber:
        match value:
            case None:
                return LuaNil()
            case bool():
                return LuaBoolean(value=value)
            case str():
                return LuaString(value=value)
            case int():
                return LuaNumber(value=value)
            case float():
                return LuaNumber(value=value)
            case _:
                raise UnknownType("Python", value.__class__.__name__)

    def _decode_table(self, table: Mapping[Any, Any]) -> LuaTableReference:
        table_id = repr(table)
        if table_id not in self._tables:
            self._tables[table_id] = []
            for key, value in table.items():
                decoded_key = self._decode(key)
                if isinstance(key, LuaNil):
                    raise NilKey()

                self._tables[table_id].append(
                    LuaTableEntry(
                        key=decoded_key, value=self._decode(value)  # type: ignore
                    )
                )

        return LuaTableReference(table_id=table_id)

    def _decode(self, value: Any) -> LuaValue:
        my_type = cast(str | None, lua_type(value))  # type : ignore
        if my_type is None:
            return self._decode_python(value)

        if my_type != "table":
            raise UnknownType("Lua", my_type)

        return self._decode_table(cast(Mapping[Any, Any], value))
