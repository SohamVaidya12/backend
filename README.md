# XAU Backend (FastAPI + PostgreSQL)

A minimal backend for your Hugging Face (Gradio) app to store users, strategy settings, and trade logs.

## Features
- API-key authentication using `X-API-Key` header
- Users table, Runs table, Trades table
- Save a run with params + summary + generated files
- Bulk insert trade rows
- Query previous runs per user

## Quick Start (Local)
1. Create a PostgreSQL database and set `DATABASE_URL` in `.env` (or use Neon/Supabase/Railway).
2. `pip install -r requirements.txt`
3. `cp .env.example .env` and edit values.
4. `python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000`

## Deploy (Render/Railway/Heroku)
- Use this repo as the source.
- Set env vars (`DATABASE_URL`, `BACKEND_SECRET`).
- Start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`

## Auth
- Create a user to get an API key: `POST /auth/signup`
- Provide the key on all requests in header: `X-API-Key: <key>`

## Endpoints
- `GET  /health`
- `POST /auth/signup` → returns `api_key`
- `POST /runs` (auth) → save one strategy run
- `POST /runs/{run_id}/trades` (auth) → bulk insert trade rows
- `GET  /runs` (auth) → list runs for the caller
- `GET  /runs/{run_id}` (auth) → run details
- `GET  /runs/{run_id}/trades` (auth) → trade rows
