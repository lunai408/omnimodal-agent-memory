"""Pydantic models and enums for the memory system."""

from datetime import UTC, datetime
from enum import Enum

from pydantic import BaseModel, Field


class Modality(str, Enum):
    """Supported data modalities."""

    TEXT = "text"
    IMAGE = "image"
    AUDIO = "audio"
    VIDEO = "video"
    PDF = "pdf"


EXTENSION_TO_MODALITY: dict[str, Modality] = {
    ".txt": Modality.TEXT,
    ".md": Modality.TEXT,
    ".csv": Modality.TEXT,
    ".json": Modality.TEXT,
    ".png": Modality.IMAGE,
    ".jpg": Modality.IMAGE,
    ".jpeg": Modality.IMAGE,
    ".gif": Modality.IMAGE,
    ".webp": Modality.IMAGE,
    ".mp3": Modality.AUDIO,
    ".wav": Modality.AUDIO,
    ".m4a": Modality.AUDIO,
    ".ogg": Modality.AUDIO,
    ".mp4": Modality.VIDEO,
    ".avi": Modality.VIDEO,
    ".mov": Modality.VIDEO,
    ".webm": Modality.VIDEO,
    ".pdf": Modality.PDF,
}

EXTENSION_TO_MIME: dict[str, str] = {
    ".txt": "text/plain",
    ".md": "text/markdown",
    ".csv": "text/csv",
    ".json": "application/json",
    ".png": "image/png",
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".gif": "image/gif",
    ".webp": "image/webp",
    ".mp3": "audio/mpeg",
    ".wav": "audio/wav",
    ".m4a": "audio/mp4",
    ".ogg": "audio/ogg",
    ".mp4": "video/mp4",
    ".avi": "video/x-msvideo",
    ".mov": "video/quicktime",
    ".webm": "video/webm",
    ".pdf": "application/pdf",
}


# --- Data models ---


class MemoryItem(BaseModel):
    """A single item stored in vector memory."""

    id: str
    modality: Modality
    source_file: str
    uri: str
    description: str = ""
    metadata: dict[str, str] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))


class SearchResult(BaseModel):
    """A single search hit returned from Qdrant."""

    id: str
    score: float
    modality: Modality
    source_file: str
    uri: str
    description: str = ""
    text_content: str = ""
    metadata: dict[str, str] = Field(default_factory=dict)


# --- API models ---


class QueryRequest(BaseModel):
    """Request body for the /query endpoint."""

    query: str
    top_k: int = Field(default=5, ge=1, le=20)
    modality_filter: Modality | None = None


class QueryResponse(BaseModel):
    """Response body for the /query endpoint."""

    query: str
    answer: str
    sources: list[SearchResult]


class IngestRequest(BaseModel):
    """Request body for the /ingest endpoint."""

    file_path: str
    description: str = ""


class IngestResponse(BaseModel):
    """Response body for the /ingest endpoint."""

    item: MemoryItem
    message: str = "Ingested successfully"
