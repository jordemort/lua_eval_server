import pytest

from lua_eval_server.evaluator.simple import SimpleLuaEvaluator


@pytest.mark.asyncio
async def test_simple_evaluator_constant():
    evaluator = SimpleLuaEvaluator()
    seven = await evaluator.eval("return 7")
    assert seven == 7
