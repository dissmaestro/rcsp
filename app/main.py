"""Main of todo app
"""
import math
from loguru import logger
from fastapi.exceptions import RequestValidationError
from fastapi import FastAPI, Request, Depends, Form, status, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles

from database import init_db, get_db, Session
import models

init_db()

# pylint: disable=invalid-name
templates = Jinja2Templates(directory="templates")

app = FastAPI()

logger = logger.opt(colors=True)
# pylint: enable=invalid-name

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
async def home(request: Request, database: Session = Depends(get_db),
               limit: int = 5, skip: int = 0):
    """Main page with todo list
    """
    logger.info("In home")
    count = database.query(models.Todo) \
        .count()
    pages = math.ceil(count / limit)

    if skip > pages:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No such page")

    todos = database.query(models.Todo) \
        .order_by(models.Todo.id.desc()).offset(skip * limit).limit(limit)
    return templates.TemplateResponse("index.html",
                                      {"request": request, "todos": todos, "page": skip, "pages": pages,
                                       "limit": limit})


@app.post("/add")
async def todo_add(request: Request, task: str = Form(...), database: Session = Depends(get_db)):
    """Add new todo
    """
    if 500 < len(task):
        msg = "Your task contains more than 500 char symbol ;("
        return templates.TemplateResponse("err_msg.html", {"request": request, "err": msg})
    todo = models.Todo(task=task)
    logger.info(f"Creating todo: {todo}")
    database.add(todo)
    database.commit()
    return RedirectResponse(url=app.url_path_for("home"), status_code=status.HTTP_303_SEE_OTHER)


@app.get("/edit/{todo_id}")
async def todo_get(request: Request, todo_id: int, database: Session = Depends(get_db)):
    """Get todo
    """
    todo = database.query(models.Todo).filter(models.Todo.id == todo_id).first()
    logger.info(f"Getting todo: {todo}")
    logger.info(f"{todo.tag}")
    return templates.TemplateResponse("edit.html", {"request": request, "todo": todo, "tags": models.Tags})


@app.post("/edit/{todo_id}")
async def todo_edit(
        request: Request,
        todo_id: int,
        task: str = Form(...),
        completed: bool = Form(False),
        tag: str = Form(None),
        database: Session = Depends(get_db)):
    """Edit todo
    """
    todo = database.query(models.Todo).filter(models.Todo.id == todo_id).first()
    logger.info(f"Editting todo: {todo}")
    todo.task = task
    todo.completed = completed
    todo.tag = tag
    database.commit()
    return RedirectResponse(url=app.url_path_for("home"), status_code=status.HTTP_303_SEE_OTHER)


@app.get("/delete/{todo_id}")
async def todo_delete(request: Request, todo_id: int, database: Session = Depends(get_db)):
    """Delete todo
    """
    todo = database.query(models.Todo).filter(models.Todo.id == todo_id).first()
    if not todo:
        msg = "You cant delete already deleted todo"
        return templates.TemplateResponse("err_msg.html", {"request": request, "err": msg})
    logger.info(f"Deleting todo: {todo}")
    database.delete(todo)
    database.commit()
    return RedirectResponse(url=app.url_path_for("home"), status_code=status.HTTP_303_SEE_OTHER)


@app.exception_handler(RequestValidationError)
async def empty_error(request: Request, database: Session = Depends(get_db)): # proverka dobavleniiya pustogo faila
    return templates.TemplateResponse("error_empty.html", {"request": request})

