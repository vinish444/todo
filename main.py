from fastapi import FastAPI, Request, Form, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# In-memory store for tasks
todos = []

@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "todos": todos})

@app.post("/add")
def add_task(task: str = Form(...)):
    todos.append(task)
    return RedirectResponse("/", status_code=303)

@app.post("/delete")
def delete_task(task: str = Form(...)):
    if task in todos:
        todos.remove(task)
    return RedirectResponse("/", status_code=303)
