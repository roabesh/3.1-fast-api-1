# Сервис объявлений купли/продажи

REST API сервис для управления объявлениями, реализованный на FastAPI с PostgreSQL.

## Поля объявления

| Поле | Тип | Описание |
|------|-----|----------|
| `id` | int | Уникальный идентификатор |
| `title` | string | Заголовок |
| `description` | string | Описание |
| `price` | float | Цена (≥ 0) |
| `author` | string | Автор |
| `created_at` | datetime | Дата создания |

## API

| Метод | Эндпоинт | Описание |
|-------|----------|----------|
| POST | `/advertisement` | Создание объявления |
| PATCH | `/advertisement/{id}` | Обновление объявления |
| DELETE | `/advertisement/{id}` | Удаление объявления |
| GET | `/advertisement/{id}` | Получение по id |
| GET | `/advertisement?title=&author=&price_min=&price_max=` | Поиск по полям |

## Запуск

```bash
docker-compose up --build
```

API доступен на `http://localhost:8000`

Документация: `http://localhost:8000/docs`
