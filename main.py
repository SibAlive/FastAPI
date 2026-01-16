from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from starlette import status

from auth import (create_access_token, authenticate_user, get_current_user,
                  ACCESS_TOKEN_EXPIRE_MINUTES, timedelta)
from models import TodoCreate, TodoUpdate, UserLogin
from utils import save_data, load_data, get_todo_by_id


app = FastAPI(title="Secure TODO API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PATCH", "DELETE"],
    allow_headers=["Content-Type", "Authorization"],
)


@app.post("/login")
def login(user: UserLogin):
    authenticated = authenticate_user(user.username, user.password)
    if not authenticated:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"}
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.post('/todos')
async def create_todo(todo: TodoCreate, user = Depends(get_current_user)):
    data = load_data()
    new_id = str(max([int(k) for k in data.keys()], default=0) + 1)
    todo_dict = todo.model_dump(mode='json')
    todo_dict['owner'] = user['username'] # Привязка к пользователю
    data[new_id] = todo_dict
    save_data(data)
    return {"id": new_id, **todo_dict}


@app.get('/todos')
async def read_todos(user = Depends(get_current_user)):
    data = load_data()
    data = {k: v for k, v in data.items() if v.get('owner') == user.get('username')}
    return list(data.values())


@app.get('/todos/{todo_id}')
def read_todo(todo_id, user = Depends(get_current_user)):
    return get_todo_by_id(todo_id, user.get("username"))


@app.patch('/todos/{todo_id}')
async def patch_todo(todo_id, todo_update: TodoUpdate, user = Depends(get_current_user)):
    data = load_data()
    get_todo_by_id(todo_id, user.get("username")) # Проверка доступа

    update_data = todo_update.model_dump(exclude_unset=True)
    todo = data[todo_id]

    for k, v in update_data.items():
        if v is not None:
            todo[k] = v

    save_data(data)
    return {"message": f"Задача с id = {todo_id} обновлена"}

@app.delete('/todos/{todo_id}')
async def delete_todo(todo_id, user = Depends(get_current_user)):
    data = load_data()
    get_todo_by_id(todo_id, user.get("username"))  # Проверка доступа
    del data[todo_id]
    save_data(data)
    return {"message": f"Задача с id = {todo_id} удалена"}