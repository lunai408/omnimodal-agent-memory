"""Data ingestion pipeline: validate, detect modality, embed, store in Qdrant."""

import uuid
from datetime import UTC, datetime
from pathlib import Path

from qdrant_client import QdrantClient
from qdrant_client.models import Distance, PointStruct, VectorParams

from app.config import Settings, get_settings
from app.embed import embed_content
from app.schemas import EXTENSION_TO_MODALITY, MemoryItem, Modality

SUPPORTED_EXTENSIONS = set(EXTENSION_TO_MODALITY.keys())


def get_qdrant_client(settings: Settings | None = None) -> QdrantClient:
    """Create a Qdrant client from settings."""
    settings = settings or get_settings()
    return QdrantClient(host=settings.qdrant_host, port=settings.qdrant_port)


def ensure_collection(
    client: QdrantClient, *, settings: Settings | None = None
) -> None:
    """Create the vector collection if it does not already exist."""
    settings = settings or get_settings()
    collections = [c.name for c in client.get_collections().collections]
    if settings.collection_name not in collections:
        client.create_collection(
            collection_name=settings.collection_name,
            vectors_config=VectorParams(
                size=settings.vector_size,
                distance=Distance.COSINE,
            ),
        )
        print(f"Created collection '{settings.collection_name}'")


def detect_modality(file_path: Path) -> Modality:
    """Detect modality from file extension."""
    suffix = file_path.suffix.lower()
    if suffix not in EXTENSION_TO_MODALITY:
        raise ValueError(
            f"Unsupported file extension '{suffix}'. "
            f"Supported: {sorted(SUPPORTED_EXTENSIONS)}"
        )
    return EXTENSION_TO_MODALITY[suffix]


def validate_file(file_path: Path, *, settings: Settings | None = None) -> None:
    """Validate that file exists and is within the size limit."""
    settings = settings or get_settings()
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    size_mb = file_path.stat().st_size / (1024 * 1024)
    if size_mb > settings.max_file_size_mb:
        raise ValueError(
            f"File too large ({size_mb:.1f} MB). "
            f"Max allowed: {settings.max_file_size_mb} MB"
        )


def ingest_file(
    file_path: Path,
    *,
    description: str = "",
    client: QdrantClient | None = None,
    settings: Settings | None = None,
) -> MemoryItem:
    """Full ingestion pipeline for a single file.

    Validates the file, detects modality, generates embedding, and stores in Qdrant.
    """
    settings = settings or get_settings()
    file_path = Path(file_path).resolve()

    validate_file(file_path, settings=settings)
    modality = detect_modality(file_path)

    text_content = ""
    if modality == Modality.TEXT:
        text_content = file_path.read_text(encoding="utf-8")

    embedding = embed_content(
        file_path, modality, description=description, settings=settings
    )

    point_id = str(uuid.uuid4())
    now = datetime.now(UTC)

    item = MemoryItem(
        id=point_id,
        modality=modality,
        source_file=file_path.name,
        uri=str(file_path),
        description=description,
        metadata={"description": description} if description else {},
        created_at=now,
    )

    if client is None:
        client = get_qdrant_client(settings)
    ensure_collection(client, settings=settings)

    client.upsert(
        collection_name=settings.collection_name,
        points=[
            PointStruct(
                id=point_id,
                vector=embedding,
                payload={
                    "modality": modality.value,
                    "source": item.source_file,
                    "uri": item.uri,
                    "description": description,
                    "text_content": text_content,
                    "metadata": item.metadata,
                    "timestamp": now.isoformat(),
                },
            )
        ],
    )
    return item


def ingest_directory(
    directory: Path,
    *,
    client: QdrantClient | None = None,
    settings: Settings | None = None,
) -> list[MemoryItem]:
    """Ingest all supported files from a directory tree."""
    settings = settings or get_settings()
    directory = Path(directory).resolve()

    if client is None:
        client = get_qdrant_client(settings)
    ensure_collection(client, settings=settings)

    items: list[MemoryItem] = []
    files = sorted(
        f
        for f in directory.rglob("*")
        if f.is_file() and f.suffix.lower() in SUPPORTED_EXTENSIONS
    )

    for i, file_path in enumerate(files, 1):
        print(f"  [{i}/{len(files)}] {file_path.name} ...", end=" ", flush=True)
        try:
            item = ingest_file(file_path, client=client, settings=settings)
            items.append(item)
            print(f"OK ({item.modality.value})")
        except Exception as e:
            print(f"FAILED: {e}")

    return items
