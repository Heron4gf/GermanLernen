# GermanLernen

A FastAPI backend that serves German vocabulary cards and runs a background daemon that generates a new card every 24 hours using an LLM. A Vue 3 frontend provides daily study (learn + exercise modes) and a history browser.

***

## Requirements

- Docker + Docker Compose, **or** Python 3.12+
- An OpenAI API key

***

## Setup

### 1. Configure environment

```bash
cp .env.example .env
```

Edit `.env`:

```env
OPENAI_API_KEY="sk-..."
MODEL="gpt-4o-mini"
DB_URL="sqlite:///./cards.db"
```

> When running via Docker Compose, `DB_URL` is overridden to use the persistent volume path.

### 2. Run with Docker Compose

```bash
docker compose up --build
```

- API: `http://localhost:8000`
- Frontend: `http://localhost:3000`

### 3. Run locally (without Docker)

```bash
pip install -r requirements.txt
cd backend/app
uvicorn main:app --reload
```

***

## API

### `GET /cards`

Returns all cards in descending creation order.

**Response** `200 OK`
```json
[
  {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "title": "Farben",
    "content": "A card about colors in German.",
    "createdAt": "2026-04-19T18:00:00Z"
  }
]
```

***

### `GET /cards/latest`

Returns the most recently created card.

**Response** `200 OK`
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "title": "Farben",
  "content": "A card about colors in German.",
  "createdAt": "2026-04-19T18:00:00Z"
}
```

**Response** `404 Not Found` — when no cards exist yet.

***

## Daemon

On startup, a background coroutine runs inside FastAPI's lifespan. Every 24 hours it:

1. Reads `app/prompts/prompt.md` as the system prompt
2. Appends all existing word pairs to the prompt (to avoid repetition)
3. Calls the configured OpenAI model
4. Parses the JSON response into a `CardSchema`
5. Persists the new card to the SQLite database

The LLM is expected to return JSON in this shape:

```json
{
  "title": "Farben",
  "content": "Colors used in everyday German.",
  "words": [
    { "word": "rot", "translation": "red" },
    { "word": "blau", "translation": "blue" }
  ]
}
```

Make sure `app/prompts/prompt.md` instructs the model to return this format.

***

## Database

SQLite is used via SQLAlchemy ORM. The database file is stored at:

- **Local:** path configured in `DB_URL` (default `./cards.db`)
- **Docker:** `/app/data/cards.db` on a named volume (`sqlite_data`)

The schema is auto-created on startup via `Base.metadata.create_all()`.

***

## Environment variables

| Variable         | Description                | Example                |
|------------------|----------------------------|------------------------|
| `OPENAI_API_KEY` | Your OpenAI secret key     | `sk-...`               |
| `MODEL`          | OpenAI model name          | `gpt-4o-mini`          |
| `DB_URL`         | SQLAlchemy database URL    | `sqlite:///./cards.db` |