"""Prompt templates for the agent retrieval layer."""

from pathlib import Path

from app.schemas import EXTENSION_TO_MIME, Modality, SearchResult

AGENT_SYSTEM_PROMPT = """\
You are a knowledge assistant with access to a multimodal memory store.
You answer questions based on retrieved context that may include text notes, \
images, audio recordings, videos, and PDF documents.

Always ground your answers in the provided sources. If the retrieved context \
does not contain enough information, say so explicitly rather than guessing.\
"""

AGENT_ANSWER_PROMPT = """\
The user asked: {query}

Here is the relevant context retrieved from memory:

{context}

Based on the above sources, provide a concise and accurate answer.\
"""


def format_context(results: list[SearchResult]) -> str:
    """Format search results into a text block for the LLM prompt."""
    if not results:
        return "(no relevant sources found)"

    lines: list[str] = []
    for i, r in enumerate(results, 1):
        header = f"[{i}] ({r.modality.value}) {r.source_file}  (score: {r.score:.3f})"
        lines.append(header)
        if r.text_content:
            lines.append(r.text_content)
        elif r.description:
            lines.append(f"Description: {r.description}")
        lines.append("")  # blank separator
    return "\n".join(lines)


def build_multimodal_content(
    query: str, results: list[SearchResult]
) -> list[str | tuple[bytes, str]]:
    """Build a list of content parts for multimodal LLM generation.

    Returns a mix of text strings and (bytes, mime_type) tuples for binary files.
    """
    parts: list[str | tuple[bytes, str]] = []
    parts.append(f"The user asked: {query}\n\nRetrieved context from memory:\n\n")

    for i, r in enumerate(results, 1):
        header = f"[{i}] ({r.modality.value}) {r.source_file}  (score: {r.score:.3f})\n"
        parts.append(header)

        if r.text_content:
            parts.append(r.text_content + "\n\n")
        elif r.modality != Modality.TEXT:
            # Read binary file and include as multimodal part
            file_path = Path(r.uri)
            if file_path.exists():
                mime = EXTENSION_TO_MIME.get(
                    file_path.suffix.lower(), "application/octet-stream"
                )
                parts.append((file_path.read_bytes(), mime))
                parts.append("\n")
            if r.description:
                parts.append(f"Description: {r.description}\n\n")
        elif r.description:
            parts.append(f"Description: {r.description}\n\n")

    parts.append("\nBased on the above sources, provide a concise and accurate answer.")
    return parts
