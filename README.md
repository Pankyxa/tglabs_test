# NL-to-SQL Telegram Bot (OpenRouter + LangChain)

Телеграм-бот, который преобразует запросы на естественном языке в SQL-запросы к PostgreSQL, используя модель **Gemini 2.0 Flash** (через OpenRouter).

Проект разработан в рамках тестового задания.

## Стек технологий

*   **Language:** Python 3.11
*   **Framework:** Aiogram 3.x
*   **LLM Orchestration:** LangChain
*   **Model Provider:** OpenRouter (Google Gemini 2.0 Flash)
*   **Database:** PostgreSQL 15 (AsyncPG + SQLAlchemy)
*   **Infrastructure:** Docker & Docker Compose

## Функциональность

1.  **Естественный язык в SQL:** Пользователь пишет "покажи топ 5 видео по просмотрам", бот генерирует и выполняет SQL.
2.  **Умная работа с данными:**
    *   Различает кумулятивные метрики (всего просмотров) и дельты (прирост за час).
    *   Автоматически конвертирует UTC (в базе) в Europe/Moscow (для пользователя).
3.  **Безопасность:** Работает в режиме `read-only` (через промпт-инжиниринг).

## Установка и запуск

### 1. Клонирование и настройка
```bash
git clone https://github.com/Pankyxa/tglabs_test.git
cd tglabs_test
cp .env.example .env
```

### 2. Конфигурация (.env)
Заполните файл `.env` своими данными:

```ini
# Telegram
TELEGRAM_TOKEN=ваш_токен_бота

# LLM (OpenRouter)
OPENROUTER_API_KEY=sk-or-v1-...
OPENROUTER_MODEL=google/gemini-2.0-flash-001

# Database
POSTGRES_USER=postgres
POSTGRES_PASSWORD=password
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DATABASE=tg_labs_db
```

### 3. Запуск в Docker (Рекомендуется)
```bash
docker compose up --build -d
```

### 4. Инициализация БД и загрузка данных
Скрипт `src/utils/loader.py` выполняет две функции:
1.  **Создает таблицы** в базе данных (если их нет).
2.  **Загружает данные** из JSON-файла.

**Инструкция:**
1. Положите ваш файл с данными в корень проекта (например, `videos.json`).
2. Запустите скрипт внутри контейнера:
```bash
# Если файл называется videos.json и лежит в корне
docker compose exec bot python -m src.utils.loader
```

## Архитектура решения

### 1. Схема данных и Промпт-инжиниринг
Используется подход **Schema-Aware Prompting**. В системный промпт (`src/ai_engine/prompts.py`) динамически подставляется DDL таблиц.

**Ключевые правила, заложенные в промпт:**
*   **Timezone Handling:** База хранит время в UTC. Промпт заставляет модель приводить время к `Europe/Moscow` для запросов типа "сегодня", "вчера", "в 18:00".
*   **Data Logic:** Модель обучена различать таблицу `videos` (текущее состояние) и `video_snapshots` (история). Для расчета роста ("на сколько выросли просмотры") модель суммирует поле `delta_views_count`, а не `views_count`.

### 2. LangChain Pipeline
Обработка запроса происходит через цепочку:
`User Query` -> `Prompt Template (with Schema)` -> `OpenRouter API` -> `SQL Parsing` -> `Execution` -> `Answer Generation`.

## Структура проекта
*   `src/ai_engine/` — Логика работы с LLM (промпты, цепочки LangChain).
*   `src/db/` — Настройки подключения к БД (SQLAlchemy).
*   `src/utils/loader.py` — Скрипт инициализации таблиц и заливки данных.
*   `main.py` — Точка входа (Aiogram bot).