import asyncio
import json

import pydantic

from lua_eval_server.evaluator.base import BaseLuaEvaluator
from lua_eval_server.models import ErrorResult, LuaResult


class SubprocessEvaluator(BaseLuaEvaluator):
    def __init__(self):
        super().__init__()
        self._child: asyncio.subprocess.Process | None = None

    async def eval(self, expr: str) -> LuaResult | ErrorResult:
        if self._child is None:
            self._child = await asyncio.create_subprocess_exec(
                "/usr/bin/env",
                "PYTHONPATH=/usr/src/lua-eval-server/src",
                "/home/devuser/venv/bin/python3",
                "-m",
                "lua_eval_server.evaluator.stdio",
                stdin=asyncio.subprocess.PIPE,
                stdout=asyncio.subprocess.PIPE,
            )

        assert self._child.stdin is not None
        assert self._child.stdout is not None

        message = json.dumps({"code": expr})
        self._child.stdin.write(f"{message}\n".encode())
        await self._child.stdin.drain()

        result = await self._child.stdout.readline()

        try:
            data = json.loads(result)
        except json.JSONDecodeError as e:
            return ErrorResult(error_type=e.__class__.__name__, error_msg=str(e))

        try:
            return LuaResult.model_validate(data)
        except pydantic.ValidationError as e:
            try:
                return ErrorResult.model_validate(data)
            except pydantic.ValidationError:
                pass
            return ErrorResult(error_type=e.__class__.__name__, error_msg=str(e))
