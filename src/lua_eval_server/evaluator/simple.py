import asyncio
from concurrent.futures import ThreadPoolExecutor

from lupa import LuaRuntime  # type: ignore


class SimpleLuaEvaluator:
    def __init__(self):
        self._executor = ThreadPoolExecutor(max_workers=1)
        self._runtime = LuaRuntime()  # type: ignore

    async def eval(self, expr: str):
        return await asyncio.get_running_loop().run_in_executor(
            self._executor, self._runtime.execute, expr
        )
