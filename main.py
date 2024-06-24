import json
from typing import Annotated
from fastapi import Body, FastAPI, Form, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field
from fastapi.templating import Jinja2Templates

from auth import authenticate, register
from first_program import compile_prompt, send_prompt_to_nn

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


class CompileQnA(BaseModel):
    questions: dict
    raw_prompt: str = Field(alias="rawPrompt")


@app.post("/compile")
async def compile(body: Annotated[str, Body()]):
    questions = json.loads(body)["questions"]
    return compile_prompt(questions)


@app.get("/main", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse(request=request, name="home.html", context={})


@app.get("/login", response_class=HTMLResponse)
async def login(request: Request):
    if request.headers.get('X-auth-user'):
        return templates.TemplateResponse(request=request, name="primer.html", context={})
    return templates.TemplateResponse(request=request, name="login.html", context={})


@app.post("/login", response_class=HTMLResponse)
async def auth(request: Request, username: Annotated[str, Form()], password: Annotated[str, Form()]):
    if request.headers.get('X-auth-user'):
        return templates.TemplateResponse(request=request, name="primer.html", context={})
    return authenticate(username, password)

@app.get("/", response_class=HTMLResponse)
async def landing(request: Request):
    return templates.TemplateResponse(request=request, name="primer.html", context={})

@app.post("/register", response_class=HTMLResponse)
async def reg(
    username: Annotated[str, Form()],
    password: Annotated[str, Form()],
    phone: Annotated[str, Form()],
    surname: Annotated[str, Form()],
    name: Annotated[str, Form()],
):
    return register(name, surname, username, password, phone)


@app.post("/")
async def promt(textInput: Annotated[str, Body()]):
    return json.dumps(send_prompt_to_nn(textInput))
