# Книжный магазин (учебный проект на Flask)

## Начало работы

### Установка виртуального окружения и зависимостей

1. Создайте виртуальное окружение:
   ```bash
   python -m venv .venv
   ```

2. Активируйте окружение:
   - Для Linux/MacOS:
     ```bash
     source .venv/bin/activate
     ```
   - Для Windows:
     ```bash
     .venv\Scripts\activate
     ```

3. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```

### Запуск проекта
Создайте файл .env, который будет содержать ваши данные:
SECRET_KEY=
SQLALCHEMY_DATABASE_URI=
(без пробелов и кавычек)

Выполните следующую команду из корневой директории проекта:
```bash
python run.py
```

После успешного запуска приложение будет доступно по адресу: [http://localhost:5000](http://localhost:5000)
