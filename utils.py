import json
from pathlib import Path

from fastapi import HTTPException


DATA_FILE = Path("data.json")


def ensure_data_file():
    """Проверяем существует ли файл data.json, если нет - создаем его"""
    if not DATA_FILE.exists():
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump({}, f, ensure_ascii=False, indent=4)


def save_data(new_data, item_id=None):
    with open("data.json", 'r', encoding='utf-8') as f:
        data = json.load(f)

    if item_id:
        data[item_id] = new_data
    else:
        data = new_data

    with open("data.json", 'w', encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def load_data():
    ensure_data_file()
    with open("data.json", 'r', encoding="utf-8") as f:
        data = json.load(f)
        return data


def get_todo_by_id(todo_id, username):
    data = load_data()
    todo = data.get(todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Задача не найдена")
    if todo.get("owner") != username:
        raise HTTPException(status_code=403, detail="Доступ запрещен")
    return todo