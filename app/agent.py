"""Agent retrieval layer: search memory then generate a grounded answer."""

from google import genai
from google.genai import types

from app.config import Settings, get_settings
from app.prompts import AGENT_SYSTEM_PROMPT, build_multimodal_content
from app.schemas import Modality, QueryResponse, SearchResult
from app.search import search_memory


def generate_answer(
    query: str,
    results: list[SearchResult],
    *,
    settings: Settings | None = None,
) -> str:
    """Call Gemini LLM with retrieved context to produce a grounded answer."""
    settings = settings or get_settings()
    client = genai.Client(api_key=settings.gemini_api_key)

    raw_parts = build_multimodal_content(query, results)
    contents: list[types.Part | str] = []
    for part in raw_parts:
        if isinstance(part, tuple):
            data, mime_type = part
            contents.append(types.Part.from_bytes(data=data, mime_type=mime_type))
        else:
            contents.append(part)

    response = client.models.generate_content(
        model=settings.generation_model,
        contents=contents,
        config=types.GenerateContentConfig(
            system_instruction=AGENT_SYSTEM_PROMPT,
            temperature=0.3,
            max_output_tokens=1024,
        ),
    )
    return response.text or "(no answer generated)"


def query_memory(
    query: str,
    *,
    top_k: int | None = None,
    modality_filter: Modality | None = None,
    settings: Settings | None = None,
) -> QueryResponse:
    """Full agent pipeline: search memory, then generate a grounded answer."""
    settings = settings or get_settings()
    top_k = top_k or settings.default_top_k

    results = search_memory(
        query, top_k=top_k, modality_filter=modality_filter, settings=settings
    )
    answer = generate_answer(query, results, settings=settings)

    return QueryResponse(query=query, answer=answer, sources=results)
