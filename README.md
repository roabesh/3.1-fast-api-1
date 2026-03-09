# Сервис объявлений купли/продажи

REST API сервис для управления объявлениями с авторизацией, реализованный на FastAPI + PostgreSQL.

## Поля объявления

| Поле | Тип | Описание |
|------|-----|----------|
| `id` | int | Уникальный идентификатор |
| `title` | string | Заголовок |
| `description` | string | Описание |
| `price` | float | Цена (≥ 0) |
| `author` | string | Автор (username создателя) |
| `created_at` | datetime | Дата создания |

## Пользователи

Поля: `id`, `username`, `password`, `group` (`user` / `admin`)

## API

### Аутентификация

| Метод | Эндпоинт | Описание |
|-------|----------|----------|
| POST | `/login` | Получить токен (48 ч) |

Токен передаётся в заголовке: `Authorization: Bearer <token>`

### Пользователи

| Метод | Эндпоинт | Доступ |
|-------|----------|--------|
| POST | `/user` | все |
| GET | `/user/{id}` | все |
| GET | `/user` | admin |
| PATCH | `/user/{id}` | владелец / admin |
| DELETE | `/user/{id}` | владелец / admin |

### Объявления

| Метод | Эндпоинт | Доступ |
|-------|----------|--------|
| GET | `/advertisement/{id}` | все |
| GET | `/advertisement?title=&author=&price_min=&price_max=` | все |
| POST | `/advertisement` | user / admin |
| PATCH | `/advertisement/{id}` | владелец / admin |
| DELETE | `/advertisement/{id}` | владелец / admin |

### Коды ошибок

- `401` — не передан или истёк токен
- `403` — недостаточно прав
- `404` — объект не найден

## Запуск

```bash
docker-compose up --build
```

API: `http://localhost:8000` | Документация: `http://localhost:8000/docs`
