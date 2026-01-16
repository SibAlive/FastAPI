Установка:
1. Клонируйте репозиторий
    git clone <ваш-репозиторий>
    cd secure-todo-api
2. Создайте виртуальное окружение и установите зависимости:
    .venv\Scripts\activate
    pip install -r requirements.txt
3. Создайте .env файл в корне проекта:
    SECRET_KEY=ваш_надёжный_секретный_ключ_длиной_32_символа
    ALGORITHM=HS256
4. Запустите сервер:
    uvicorn main:app --reload
5. Получите токен:
    В endpoint'е /login введите логин: admin, пароль: qwerty
    Скопируте токен, нажмите Autorize и вставьте его в поле Value.