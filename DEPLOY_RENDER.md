# 🚀 Инструкция по деплою на Render.com (Бесплатно / Free Tier)

Сайт **APEX NUTRITION** полностью адаптирован и готов к 1-кликовому деплою на платформу [Render.com](https://render.com).

---

## ⚡ Вариант 1: Самый быстрый способ (Через Web Service в панели Render)

### Шаг 1. Загрузите проект на GitHub
1. Если проект еще не в Git, откройте терминал в папке проекта:
   ```bash
   git init
   git add .
   git commit -m "Initial commit for Render deployment"
   ```
2. Создайте новый репозиторий на [GitHub.com](https://github.com/new).
3. Привяжите репозиторий и запушьте код:
   ```bash
   git remote add origin https://github.com/ВАШ_ЛОГИН/ВАШ_РЕПОЗИТОРИЙ.git
   git branch -M main
   git push -u origin main
   ```

---

### Шаг 2. Создание Web Service на Render
1. Зарегистрируйтесь / войдите на [Render.com](https://dashboard.render.com).
2. Нажмите синюю кнопку **«New +»** в правом верхнем углу и выберите **«Web Service»**.
3. Выберите **«Build and deploy from a Git repository»** и подключите ваш репозиторий на GitHub.
4. Заполните настройки сервиса:
   - **Name:** `apex-nutrition-store` (или любое другое имя)
   - **Language / Runtime:** `Python 3`
   - **Branch:** `main`
   - **Region:** Frankfurt (EU) или любой ближайший
   - **Build Command:**
     ```bash
     ./build.sh
     ```
   - **Start Command:**
     ```bash
     gunicorn apex_project.wsgi:application
     ```
   - **Plan Type:** `Free`

5. Разверните вкладку **«Advanced»** ➔ **«Environment Variables»** (Переменные окружения):
   - `PYTHON_VERSION` = `3.12.8`
   - `DJANGO_DEBUG` = `False`
   - `DJANGO_SECRET_KEY` = `(нажмите Generate или введите любой длинный случайный ключ)`

6. Нажмите **«Create Web Service»**.

---

### Шаг 3. (Опционально) Подключение базы данных PostgreSQL на Render
Если вы хотите использовать полноценную базу данных PostgreSQL вместо SQLite:
1. В панели Render нажмите **«New +»** ➔ **«PostgreSQL»**.
2. Введите имя (например `apex-db`), выберите план **Free** и нажмите **«Create Database»**.
3. Скопируйте **«Internal Database URL»**.
4. Вернитесь в ваш **Web Service** ➔ вкладка **«Environment»** ➔ добавьте переменную:
   - `DATABASE_URL` = `значение Internal Database URL`
5. Нажмите **«Save Changes»** — Render автоматически перезапустит билд, накатит миграции и заполнит базу товарами и администратором!

---

## 🔑 Данные для входа в админ-панель
Скрипт `build.sh` автоматически создаст администратора при первом запуске:
- **URL админки:** `https://ваш-проект.onrender.com/admin/`
- **Логин:** `admin`
- **Пароль:** `admin123`

---

## 🛠️ Что было настроено для Render
- `build.sh` — автоматически устанавливает зависимости, собирает статику через WhiteNoise, применяет миграции и наполняет базу товарами и фото (`populate_db.py`).
- `render.yaml` — готовый Blueprint для автоматического развертывания Web Service + PostgreSQL в 1 клик.
- `runtime.txt` & `Procfile` — указание версии Python и точки входа Gunicorn.
- `settings.py` — автоматическое определение `DATABASE_URL`, настройка `CSRF_TRUSTED_ORIGINS` для доменов `*.onrender.com`, WhiteNoise кэширование и безопасные заголовки.
- `urls.py` — автоматическая раздача медиа-файлов и изображений товаров.
