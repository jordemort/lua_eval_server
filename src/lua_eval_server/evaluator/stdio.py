import asyncio
import json
import sys
from typing import Any

from lua_eval_server.evaluator.simple import SimpleLuaEvaluator
from lua_eval_server.models import ErrorResult


class StdioLuaEvaluator(SimpleLuaEvaluator):
    def print_error(self, error_type: str, error_msg: str):
        print(ErrorResult(error_type=error_type, error_msg=error_msg).model_dump_json())
        sys.stdout.flush()

    async def main(self):
        for line in sys.stdin:
            try:
                data = json.loads(line)
            except Exception as e:
                self.print_error(e.__class__.__name__, str(e))
                continue

            if not isinstance(data, dict):
                self.print_error("MalformedInput", "Input is not a dict")
                continue

            if "code" not in data:
                self.print_error("MalformedInput", "No code in input")
                continue

            code: Any = data["code"]
            if not isinstance(code, str):
                self.print_error("MalformedInput", "Code is not a string")
                continue

            try:
                result = await self.eval(code)
                print(result.model_dump_json())
                sys.stdout.flush()
            except Exception as e:
                self.print_error(e.__class__.__name__, str(e))


if __name__ == "__main__":
    asyncio.run(StdioLuaEvaluator().main())
