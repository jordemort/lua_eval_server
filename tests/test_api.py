from typing import Any

import pytest
from fastapi.testclient import TestClient

from lua_eval_server.app import app


@pytest.fixture
def client():
    return TestClient(app)


def test_new_session(client: TestClient):
    response = client.post("/eval", content="return 1+1")

    assert "session_id" in response.cookies
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
    assert root["value"] == 2


def test_no_chosen_session_id(client: TestClient):
    response = client.post(
        "/eval", content="return 1+1", cookies={"session_id": "garbage"}
    )
    assert response.status_code == 200
    assert "session_id" in response.cookies
    assert response.cookies["session_id"] != "garbage"
