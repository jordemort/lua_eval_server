import pytest

from lua_eval_server.evaluator.simple import EvalError, SimpleLuaEvaluator


@pytest.mark.asyncio
async def test_simple_evaluator_int():
    evaluator = SimpleLuaEvaluator()
    with pytest.raises(EvalError):
        await evaluator.eval("a*(F#NCOwe898731*#1-)asdf871#!#$()P((!)$)")
