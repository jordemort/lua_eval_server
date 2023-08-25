import asyncio
from concurrent.futures import ThreadPoolExecutor
from typing import Any

from lupa import LuaRuntime  # type: ignore

from lua_eval_server.evaluator.base import BaseLuaEvaluator, EvalError
from lua_eval_server.models import LuaResult


class SimpleLuaEvaluator(BaseLuaEvaluator):
    """
    A simple Lua evaluator.

    Expressions are evaluated in a separate thread, to avoid stalling the API server.
    """

    def __init__(self):
        super().__init__()
        self._executor = ThreadPoolExecutor(max_workers=1)
        self._runtime = LuaRuntime()  # type: ignore

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
