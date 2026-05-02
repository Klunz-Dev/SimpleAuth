# 🔐 SimpleAuth 

Простой сервис авторизации на **FastAPI**, реализующий работу с **JWT** токенами и **Async SQLAlchemy**.

## ✨ Что уже реализовано
*   **Авторизация через JWT**: Генерация Access и Refresh токенов при логине.
*   **Безопасность Cookies**: Использование `AuthX` для автоматической записи токенов в защищенные куки браузера.
*   **Асинхронность**: Работа с базой данных через `AsyncSession` и `SQLAlchemy`.
*   **Валидация паролей**: Поиск пользователя с проверкой хеша и соли.
*   **Rate Limiting**: Ограничение попыток входа для защиты от перебора паролей.

## 🛠 Стек технологий
*   **Python**
*   **FastAPI**
*   **AuthX** (JWT & Cookies)
*   **SQLAlchemy** (Async)
*   **SQLite**

## 🚀 Как запустить проект

1. **Клонировать репозиторий:**
   ```bash
   git clone https://github.com
   cd SimpleAuth
   ```

2. **Установить зависимости:**
   *(Перед этим рекомендуется создать виртуальное окружение)*
   ```bash
   pip install fastapi authx sqlalchemy uvicorn slowapi
   ```

3. **Запустить сервер:**
   ```bash
   uvicorn src.web.server:app --reload
   ```

## 📂 Структура проекта
*   `src/web/server.py` — основной файл приложения и эндпоинты.
*   `src/auth/` — настройки JWT и логика безопасности.
*   `src/database/` — модели SQLAlchemy и подключение к БД.

---
**Project by [Klunz-Dev](https://github.com)**
