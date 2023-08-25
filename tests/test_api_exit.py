from typing import Any

import pytest
from fastapi.testclient import TestClient

from lua_eval_server.app import app

SCRIPT_1 = """
x = 7
return x
"""


@pytest.fixture
def client():
    return TestClient(app)


def test_api_exit(client: TestClient):
    response = client.post("/eval", content=SCRIPT_1)
    assert "session_id" in response.cookies
    session_id = response.cookies["session_id"]
    assert response.status_code == 200

    result = response.json()
    assert isinstance(result, dict)
    assert "tables" in result
    assert "root" in result

    tables: Any = result["tables"]
    assert isinstance(tables, dict)
    assert len(tables) == 0  # type: ignore

    root: Any = result["root"]
    assert isinstance(root, dict)
    assert len(root) == 2  # type: ignore

    assert "type" in root
    assert root["type"] == "number"

    assert "value" in root
    assert root["value"] == 7

    response = client.post("/exit", cookies=response.cookies)
    assert response.status_code == 200

    response = client.post(
        "/eval", content="return x", cookies={"session_id": session_id}
    )
    assert "session_id" in response.cookies
    assert response.cookies["session_id"] != session_id

    result = response.json()
    assert isinstance(result, dict)
    assert "tables" in result
    assert "root" in result

    root: Any = result["root"]
    assert isinstance(root, dict)
    assert len(root) == 1  # type: ignore

    assert "type" in root
    assert root["type"] == "nil"
