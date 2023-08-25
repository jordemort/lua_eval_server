import pytest

from lua_eval_server.evaluator.simple import SimpleLuaEvaluator
from lua_eval_server.models import LuaNil, LuaNumber, LuaResult, LuaString


@pytest.mark.asyncio
async def test_simple_evaluator_int():
    evaluator = SimpleLuaEvaluator()
    value = await evaluator.eval("return 7")
    assert isinstance(value, LuaResult)
    assert isinstance(value.root, LuaNumber)
    assert value.root.type == "number"
    assert value.tables == {}
    assert isinstance(value.root.value, int)
    assert value.root.value == 7


@pytest.mark.asyncio
async def test_simple_evaluator_float():
    evaluator = SimpleLuaEvaluator()
    value = await evaluator.eval("return 7.1")
    assert isinstance(value, LuaResult)
    assert isinstance(value.root, LuaNumber)
    assert value.root.type == "number"
    assert value.tables == {}
    assert isinstance(value.root.value, float)
    assert value.root.value == 7.1  # XXX: possible float precision gremlins


@pytest.mark.asyncio
async def test_simple_evaluator_str():
    evaluator = SimpleLuaEvaluator()
    value = await evaluator.eval("return 'chicken'")
    assert isinstance(value, LuaResult)
    assert isinstance(value.root, LuaString)
    assert value.root.type == "string"
    assert value.tables == {}
    assert isinstance(value.root.value, str)
    assert value.root.value == "chicken"


@pytest.mark.asyncio
async def test_simple_evaluator_nil():
    evaluator = SimpleLuaEvaluator()
    value = await evaluator.eval("return nil")
    assert isinstance(value, LuaResult)
    assert isinstance(value.root, LuaNil)
    assert value.root.type == "nil"
    assert value.tables == {}
