from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
import os

todo_app = FastAPI()

BASE_DIR = os.path.dirname(__file__)
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))
todo_app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "static")), name="static")

todos = []

@todo_app.get("/")
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "todos": todos})

@todo_app.post("/add")
def add(task: str = Form(...)):
    todos.append(task)
    return RedirectResponse(url="/gui/todo/", status_code=303)

@todo_app.post("/delete")
def delete(task: str = Form(...)):
    if task in todos:
        todos.remove(task)
    return RedirectResponse(url="/gui/todo/", status_code=303)
