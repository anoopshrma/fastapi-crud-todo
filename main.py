from typing import List
from fastapi import FastAPI, status, HTTPException, Depends
from database import Base, engine, SessionLocal
from sqlalchemy.orm import Session
import schemas
import models

# Create the database
Base.metadata.create_all(engine)

# Initialize app
app = FastAPI()

# provides database session to each request upon calling
def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()

@app.get("/")
def root():
    return "Welcome to Todo Application. Built with FastAPI and ❤️. \n Please share https://pythonwarriors.com with your friends"

@app.post("/todo", response_model=schemas.ToDoAll, status_code=status.HTTP_201_CREATED)
def create_todo(todo: schemas.ToDoCreate, session: Session = Depends(get_session)):

    # create an instance of Todo Model
    todo_obj = models.ToDo(task = todo.task)

    # Add the object into our database Table
    session.add(todo_obj)
    session.commit()
    session.refresh(todo_obj)

    # return the todo object
    return todo_obj

@app.get("/todo/{id}", response_model=schemas.ToDoAll)
def read_todo(id: int, session: Session = Depends(get_session)):

    # Fetch todo record using id from the table
    todo_obj = session.query(models.ToDo).get(id)

    # Check if there is record with the provided id, if not then Raise 404 Exception
    if not todo_obj:
        raise HTTPException(status_code=404, detail=f"todo item with id {id} not found")

    return todo_obj

@app.put("/todo/{id}", response_model=schemas.ToDoAll)
def update_todo(id: int, task: str, session: Session = Depends(get_session)):

    # Fetch todo record using id from the table
    todo_obj = session.query(models.ToDo).get(id)

    # If the record is present in our DB table then update 
    if todo_obj:
        todo_obj.task = task
        session.commit()

    # if todo item with given id does not exists, raise exception and return 404 not found response
    if not todo_obj:
        raise HTTPException(status_code=404, detail=f"todo item with id {id} not found")

    return todo_obj

@app.delete("/todo/{id}", response_model = str)
def delete_todo(id: int, session: Session = Depends(get_session)):

    # Fetch todo record using id from the table
    todo_obj = session.query(models.ToDo).get(id)

    # Check if Todo record is present in our Database,If not then raise 404 error
    if todo_obj:
        session.delete(todo_obj)
        session.commit()
    else:
        raise HTTPException(status_code=404, detail=f"todo item with id {id} not found")

    return f"Todo task with id {id} successfully deleted"

@app.get("/todo", response_model = List[schemas.ToDoAll])
def read_todo_list(session: Session = Depends(get_session)):

    # get all todo items
    todo_list = session.query(models.ToDo).all()

    return todo_list
