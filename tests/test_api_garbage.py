import pytest
from fastapi.testclient import TestClient

from lua_eval_server.app import app


@pytest.fixture
def client():
    return TestClient(app)


def test_api_garbage(client: TestClient):
    response = client.post("/eval", content="a*(F#NCOwe898731*#1-)asdf871#!#$()P((!)$)")

    assert response.status_code == 400

    result = response.json()
    assert isinstance(result, dict)
    assert "error_type" in result
    assert isinstance(result["error_type"], str)
    assert "error_msg" in result
    assert isinstance(result["error_msg"], str)

    assert result["error_type"] == "EvalError"
