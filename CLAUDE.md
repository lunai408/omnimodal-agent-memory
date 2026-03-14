# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A minimal reference implementation of a shared multimodal memory layer for AI agents. Instead of converting images/audio/PDFs/video to text before embedding, all modalities are embedded into a **single vector space** using Gemini Embedding models and stored in Qdrant.

This is an **educational reference architecture**, not a production system.

## Tech Stack

- **Python 3.12+** (see `.python-version`)
- **Gemini Embeddings** (`google-generativeai`) — multimodal embedding model
- **Qdrant** — vector database (Docker, cosine distance, 3072-dim vectors)
- **FastAPI + Uvicorn** — API layer
- **Pydantic** — data models and validation

## Architecture

```
text/image/audio/video/pdf → Gemini multimodal embedding → Qdrant (single collection) → agent semantic search → LLM reasoning
```

Three layers:

1. **Ingestion** (`app/ingest.py`, `app/embed.py`) — load assets, detect modality, generate embeddings, store in Qdrant
2. **Vector Memory** (`app/search.py`) — single `agent_memory` collection in Qdrant with payload fields: modality, source, uri, metadata, timestamp
3. **Agent Retrieval** (`app/agent.py`, `app/prompts.py`) — embed query, vector search, assemble multimodal context, LLM grounded answer

Key modules: `app/config.py` (config), `app/schemas.py` (Pydantic models), `app/api.py` (FastAPI app).

## Commands

```bash
# Start Qdrant
docker compose up

# Load sample data
python scripts/load_sample_data.py

# Ingest into vector DB
python scripts/ingest_dataset.py

# Run interactive demo
python scripts/demo_query.py
```

## Design Specification

`brief.md` contains the full project specification with architecture details, data models, and planned structure. Consult it when implementing new components.

## Notes:

1. Always use Context7 mcp to search documentation and examples
2. Always use the project specification in `brief.md` when implementing new components, and update it as you go
3. Always lint with ruff and format with black and add type hints, and pydantic validation (update pyproject.toml if needed)
