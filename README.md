# Omnimodal Agent Memory

A minimal reference implementation of a **shared multimodal memory layer** for AI agents.

Instead of converting images, audio, PDFs, and videos into text before embedding, this project embeds all modalities into a **single vector space** using [Gemini Embeddings](https://ai.google.dev/gemini-api/docs/embeddings) and stores them in [Qdrant](https://qdrant.tech/).

```
text / image / audio / video / pdf
            ↓
   Gemini multimodal embedding
            ↓
     Qdrant (single collection)
            ↓
   agent semantic search → LLM answer
```

## Quickstart

### 1. Install

```bash
pip install -e ".[dev,samples]"
cp .env.example .env          # add your GEMINI_API_KEY
```

### 2. Start Qdrant

```bash
docker compose up -d
```

### 3. Generate sample data

```bash
python scripts/load_sample_data.py
```

### 4. Ingest into vector memory

```bash
python scripts/ingest_dataset.py
```

### 5. Query interactively

```bash
python scripts/demo_query.py
```

### 6. Start the API

```bash
python main.py
```

```bash
# Health check
curl http://localhost:8000/health

# Agent query
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"query": "pricing complaint", "top_k": 3}'
```

## Architecture

| Layer | Files | Purpose |
|-------|-------|---------|
| **Config** | `app/config.py`, `app/schemas.py` | Settings, Pydantic models, modality mappings |
| **Embedding** | `app/embed.py` | Gemini multimodal embeddings (text, image, audio, video, PDF) |
| **Ingestion** | `app/ingest.py` | Validate, detect modality, embed, store in Qdrant |
| **Search** | `app/search.py` | Semantic vector search with optional modality filter |
| **Agent** | `app/agent.py`, `app/prompts.py` | Search + LLM reasoning for grounded answers |
| **API** | `app/api.py`, `main.py` | FastAPI endpoints (`/health`, `/ingest`, `/search`, `/query`) |

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/health` | Liveness check |
| `POST` | `/ingest` | Ingest a file by path |
| `POST` | `/search` | Raw vector search (top-k results) |
| `POST` | `/query` | Agent query (search + LLM answer) |

## Tech Stack

- **Python 3.12+**
- **Gemini Embeddings** (`google-genai`) — `gemini-embedding-2-preview` (3072-dim, natively multimodal)
- **Qdrant** — vector database (cosine distance)
- **FastAPI** — API layer
- **Pydantic** — data models and validation

## Visualization

```bash
pip install -e ".[notebook]"
jupyter notebook notebooks/visualize_embeddings.ipynb
```

Plots a t-SNE projection of all embeddings colored by modality.

## License

MIT
