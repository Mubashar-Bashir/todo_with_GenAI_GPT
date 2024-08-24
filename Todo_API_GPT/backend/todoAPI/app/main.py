from contextlib import asynccontextmanager
from typing import Optional,Annotated
from app.Configuration import settings
from sqlmodel import Field, SQLModel, create_engine, select,Session
from fastapi import FastAPI, HTTPException, Depends
from app.Database import database
from app.Models import models
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime

Todo = models.Todo
TodoCreate = models.TodoCreate
TodoUpdate = models.TodoUpdate

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Creating tables..")
    database.create_db_and_tables()
    yield

def get_session():
    with Session(database.engine) as session:
        yield session

app = FastAPI(lifespan=lifespan, title="Hello World API with NeonDB", 
    version="0.0.1",
    servers=[
        {
            "url": "https://faces-relates-heads-manually.trycloudflare.com", # ADD LIVE URL Here Before Creating GPT Action
            "description": "Production Server TODO GPT"
        }
        ])

# Set up CORS
origins = [
    "http://localhost:3000",
    "http://localhost:8001",
    "http://backend:8001",
    "http://frontend:3000",
    "https://web.wania.xyz"
    # Add other origins if needed
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"Message": "Todo GPT"}


@app.get("/todos/", response_model=list[Todo])
def read_todos(session: Annotated[Session, Depends(get_session)]):
        todos = session.exec(select(Todo)).all()
        return todos
    
@app.post("/todos/", response_model=Todo)
def create_todo(todo_create: TodoCreate, session: Annotated[Session, Depends(get_session)]):
        todo = Todo.model_validate(todo_create)  # Convert TodoCreate to Todo
        session.add(todo)
        session.commit()
        session.refresh(todo)
        return todo

@app.put("/todos/{todo_id}", response_model=Todo)
def update_todo(todo_id: int, updated_todo: TodoUpdate, session: Annotated[Session, Depends(get_session)]):
        # Fetch existing todo from DB
        existing_todo = session.get(Todo, todo_id)

        # If the todo does not exist - raise an HTTPException 
        if existing_todo is None:
            raise HTTPException(status_code=404, detail="Todo not found")

        
        # Update the fields if provided in the request
        if updated_todo.content is not None:
            existing_todo.content = updated_todo.content
        if updated_todo.status is not None:
            existing_todo.status = updated_todo.status
        if updated_todo.priority is not None:
            existing_todo.priority = updated_todo.priority
        if updated_todo.due_date is not None:
            existing_todo.due_date = updated_todo.due_date


        # Update the updated_at field to the current datetime
        existing_todo.updated_at = datetime.utcnow()
        session.commit()
        session.refresh(existing_todo)
        return existing_todo

@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int, session: Annotated[Session, Depends(get_session)]):
        #Fetch existing todo from DB
        existing_todo = session.get(Todo, todo_id)

        if existing_todo is None:
            raise HTTPException(status_code=404, detail="Todo not found")

        # Delete the todo from DB
        session.delete(existing_todo)
        session.commit()
        return {"message": "Todo successfully deleted"}