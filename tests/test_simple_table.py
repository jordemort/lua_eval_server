import pytest

from lua_eval_server.evaluator.simple import SimpleLuaEvaluator
from lua_eval_server.models import (
    LuaNumber,
    LuaResult,
    LuaString,
    LuaTableEntry,
    LuaTableReference,
)


@pytest.mark.asyncio
async def test_simple_table():
    evaluator = SimpleLuaEvaluator()
    value = await evaluator.eval("return {a=1,b=2,c=3}")
    assert isinstance(value, LuaResult)
    assert isinstance(value.root, LuaTableReference)
    assert len(value.tables) == 1
    assert value.root.table_id in value.tables

    table = value.tables[value.root.table_id]
    assert isinstance(table, list)
    assert len(table) == 3

    find_in_table = {"a": 1, "b": 2, "c": 3}

    for entry in table:
        assert isinstance(entry, LuaTableEntry)
        assert isinstance(entry.key, LuaString)
        assert isinstance(entry.value, LuaNumber)
        assert entry.key.value in find_in_table
        assert entry.value.value == find_in_table[entry.key.value]
        del find_in_table[entry.key.value]

    assert len(find_in_table) == 0
