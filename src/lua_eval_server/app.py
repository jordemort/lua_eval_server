from typing import Annotated

from fastapi import Cookie, FastAPI, Request, Response, status

from lua_eval_server.evaluator.simple import EvaluatorException
from lua_eval_server.models import ErrorResult, LuaResult
from lua_eval_server.sessions import SessionManager

app = FastAPI()
sessions = SessionManager()


@app.post("/eval")
async def lua_eval(
    request: Request,
    response: Response,
    session_id: Annotated[str | None, Cookie()] = None,
) -> LuaResult | ErrorResult:
    try:
        code = (await request.body()).decode("utf-8")
        session = sessions.get_session(session_id)
        result = await session.evaluator.eval(code)

        response.set_cookie(key="session_id", value=session.session_id)
        return result
    except EvaluatorException as e:
        response.status_code = 400
        return ErrorResult(error_type=e.__class__.__name__, error_msg=str(e))


@app.post("/exit")
async def lua_exit(session_id: Annotated[str, Cookie()]):
    sessions.close_session(session_id)
    response = Response(status_code=status.HTTP_200_OK)
    response.delete_cookie("session_id")

    return response
