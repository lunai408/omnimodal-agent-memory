"""Embedding generation using Gemini multimodal embedding model."""

from pathlib import Path

from google import genai
from google.genai import types

from app.config import Settings, get_settings
from app.schemas import EXTENSION_TO_MIME, Modality


def _get_client(settings: Settings | None = None) -> genai.Client:
    """Create a Gemini API client."""
    settings = settings or get_settings()
    return genai.Client(api_key=settings.gemini_api_key)


def embed_text(text: str, *, settings: Settings | None = None) -> list[float]:
    """Generate an embedding for a text string."""
    settings = settings or get_settings()
    client = _get_client(settings)
    result = client.models.embed_content(
        model=settings.embedding_model,
        contents=text,
    )
    return list(result.embeddings[0].values)


def embed_file(
    file_path: Path,
    *,
    description: str = "",
    settings: Settings | None = None,
) -> list[float]:
    """Generate an embedding for a binary file (image, audio, video, PDF).

    If a description is provided, it is fused with the file into a single
    embedding via a multi-part Content object.
    """
    settings = settings or get_settings()
    client = _get_client(settings)

    suffix = file_path.suffix.lower()
    mime_type = EXTENSION_TO_MIME.get(suffix, "application/octet-stream")
    data = file_path.read_bytes()

    file_part = types.Part.from_bytes(data=data, mime_type=mime_type)

    if description:
        # Fuse description text + file into one embedding
        contents: list[types.Content] = [
            types.Content(
                parts=[
                    types.Part(text=description),
                    file_part,
                ]
            )
        ]
    else:
        contents = [file_part]  # type: ignore[list-item]

    result = client.models.embed_content(
        model=settings.embedding_model,
        contents=contents,
    )
    return list(result.embeddings[0].values)


def embed_content(
    file_path: Path,
    modality: Modality,
    *,
    description: str = "",
    settings: Settings | None = None,
) -> list[float]:
    """Unified embedding router: text files are read as text, others as binary."""
    if modality == Modality.TEXT:
        text = file_path.read_text(encoding="utf-8")
        if description:
            text = f"{description}\n\n{text}"
        return embed_text(text, settings=settings)
    return embed_file(file_path, description=description, settings=settings)
