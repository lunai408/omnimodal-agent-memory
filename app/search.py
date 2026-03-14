"""Semantic search over the multimodal vector memory."""

from qdrant_client.models import FieldCondition, Filter, MatchValue

from app.config import Settings, get_settings
from app.embed import embed_text
from app.ingest import ensure_collection, get_qdrant_client
from app.schemas import Modality, SearchResult


def search_memory(
    query: str,
    *,
    top_k: int | None = None,
    modality_filter: Modality | None = None,
    settings: Settings | None = None,
) -> list[SearchResult]:
    """Embed a text query and search Qdrant for the most similar memory items."""
    settings = settings or get_settings()
    top_k = top_k or settings.default_top_k

    query_vector = embed_text(query, settings=settings)

    client = get_qdrant_client(settings)
    ensure_collection(client, settings=settings)

    query_filter = None
    if modality_filter is not None:
        query_filter = Filter(
            must=[
                FieldCondition(
                    key="modality",
                    match=MatchValue(value=modality_filter.value),
                )
            ]
        )

    hits = client.query_points(
        collection_name=settings.collection_name,
        query=query_vector,
        limit=top_k,
        query_filter=query_filter,
    ).points

    results: list[SearchResult] = []
    for hit in hits:
        payload = hit.payload or {}
        results.append(
            SearchResult(
                id=str(hit.id),
                score=hit.score,
                modality=Modality(payload.get("modality", "text")),
                source_file=payload.get("source", ""),
                uri=payload.get("uri", ""),
                description=payload.get("description", ""),
                text_content=payload.get("text_content", ""),
                metadata=payload.get("metadata", {}),
            )
        )
    return results
