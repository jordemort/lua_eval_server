from typing import Annotated

from fastapi import Cookie, FastAPI, Request

app = FastAPI()


@app.post("/eval")
async def lua_eval(session_id: Annotated[str | None, Cookie()], request: Request):
    pass


@app.post("/exit")
async def lua_exit(session_id: Annotated[str, Cookie()]):
    pass
