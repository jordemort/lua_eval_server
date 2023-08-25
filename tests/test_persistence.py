import pytest

from lua_eval_server.evaluator.simple import SimpleLuaEvaluator
from lua_eval_server.models import LuaNumber

SCRIPT_1 = """
x = 7
return x
"""

SCRIPT_2 = """
x = x + 3
return x
"""


@pytest.mark.asyncio
async def test_persistence():
    evaluator = SimpleLuaEvaluator()
    value = await evaluator.eval(SCRIPT_1)
    assert isinstance(value.root, LuaNumber)
    assert isinstance(value.root.value, int)
    assert value.root.value == 7

    value = await evaluator.eval(SCRIPT_2)
    assert isinstance(value.root, LuaNumber)
    assert isinstance(value.root.value, int)
    assert value.root.value == 10
