from dataclasses import dataclass
from uuid import uuid4

from lua_eval_server.evaluator.simple import SimpleLuaEvaluator


@dataclass
class Session:
    """
    Represents a current session.

    This is a dataclass instead of a BaseModel because this is not user-facing.
    We don't need all the overhead of validation.
    """

    session_id: str
    evaluator: SimpleLuaEvaluator


class SessionManager:
    def __init__(self):
        self._sessions: dict[str, SimpleLuaEvaluator] = {}

    def get_session(self, session_id: str | None) -> Session:
        if session_id is None or session_id not in self._sessions:
            session_id = str(uuid4())
            self._sessions[session_id] = SimpleLuaEvaluator()

        return Session(session_id=session_id, evaluator=self._sessions[session_id])

    def close_session(self, session_id: str) -> None:
        if session_id in self._sessions:
            del self._sessions[session_id]
