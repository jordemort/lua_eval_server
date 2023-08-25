import pytest

from lua_eval_server.evaluator.simple import SimpleLuaEvaluator
from lua_eval_server.models import (
    LuaNumber,
    LuaResult,
    LuaString,
    LuaTableEntry,
    LuaTableReference,
)

SCRIPT = """
x = {}
x.foo = 3
x.self = x
return x
"""


@pytest.mark.asyncio
async def test_self_referential():
    evaluator = SimpleLuaEvaluator()
    value = await evaluator.eval(SCRIPT)
    assert isinstance(value, LuaResult)
    assert isinstance(value.root, LuaTableReference)
    assert len(value.tables) == 1
    assert value.root.table_id in value.tables

    table = value.tables[value.root.table_id]
    assert isinstance(table, list)
    assert len(table) == 2

    for entry in table:
        assert isinstance(entry, LuaTableEntry)
        assert isinstance(entry.key, LuaString)
        if entry.key.value == "foo":
            assert isinstance(entry.value, LuaNumber)
            assert entry.value.value == 3
        else:
            assert entry.key.value == "self"
            assert isinstance(entry.value, LuaTableReference)
            assert entry.value.table_id == value.root.table_id
