"""FastAPI application with ingest, search, and query endpoints."""

from pathlib import Path

from fastapi import FastAPI, HTTPException

from app.agent import query_memory
from app.ingest import ingest_file
from app.schemas import (
    IngestRequest,
    IngestResponse,
    QueryRequest,
    QueryResponse,
    SearchResult,
)
from app.search import search_memory

app = FastAPI(
    title="Omnimodal Agent Memory",
    description="Shared multimodal memory layer for AI agents.",
    version="0.1.0",
)


@app.get("/health")
def health() -> dict[str, str]:
    """Liveness check."""
    return {"status": "ok"}


@app.post("/ingest", response_model=IngestResponse)
def ingest(request: IngestRequest) -> IngestResponse:
    """Ingest a file into vector memory."""
    file_path = Path(request.file_path)
    try:
        item = ingest_file(file_path, description=request.description)
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    return IngestResponse(item=item)


@app.post("/search", response_model=list[SearchResult])
def search(request: QueryRequest) -> list[SearchResult]:
    """Raw vector search — returns top-k results without LLM reasoning."""
    return search_memory(
        request.query,
        top_k=request.top_k,
        modality_filter=request.modality_filter,
    )


@app.post("/query", response_model=QueryResponse)
def query(request: QueryRequest) -> QueryResponse:
    """Agent query — search memory then generate a grounded LLM answer."""
    return query_memory(
        request.query,
        top_k=request.top_k,
        modality_filter=request.modality_filter,
    )
