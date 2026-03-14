#!/usr/bin/env python3
"""Ingest all files in the data/ directory into Qdrant."""

from pathlib import Path

from app.config import get_settings
from app.ingest import ensure_collection, get_qdrant_client, ingest_directory


def main() -> None:
    settings = get_settings()
    data_dir = Path(settings.data_dir)

    if not data_dir.exists():
        print(f"Data directory '{data_dir}' not found.")
        print("Run `python scripts/load_sample_data.py` first.")
        return

    print(f"Connecting to Qdrant at {settings.qdrant_host}:{settings.qdrant_port}")
    client = get_qdrant_client(settings)
    ensure_collection(client, settings=settings)

    print(f"Ingesting files from {data_dir}/\n")
    items = ingest_directory(data_dir, client=client, settings=settings)

    print(f"\nIngested {len(items)} items into collection '{settings.collection_name}'")

    # Print summary by modality
    modalities: dict[str, int] = {}
    for item in items:
        modalities[item.modality.value] = modalities.get(item.modality.value, 0) + 1
    for mod, count in sorted(modalities.items()):
        print(f"  {mod}: {count}")


if __name__ == "__main__":
    main()
