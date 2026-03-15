# brief.md

## Repository

**Name**

```
omnimodal-agent-memory
```

**Tagline**

```
A minimal reference implementation of a shared multimodal memory layer for AI agents using Gemini Embeddings.
```

**Short description**

This repository demonstrates how to build a **shared multimodal memory system** for AI agents.

Instead of converting images, audio, PDFs, and videos into text before indexing them, this project embeds all modalities into a **single vector space** using Gemini Embedding models.

The system allows an agent to retrieve context across text, images, audio, video, and documents using a single semantic query.

---

# Motivation

Most modern AI systems are still **text-first architectures**.

Images become captions.
Audio becomes transcripts.
Documents become extracted text.

Only then are they embedded and stored in vector databases.

This repository demonstrates a different architecture.

A **shared multimodal embedding space** where heterogeneous data can be stored and retrieved directly without forcing everything through text conversion.

This pattern is particularly useful for:

AI agents
multimodal search systems
knowledge assistants
copilot tools
robotics systems
multimedia knowledge bases

---

# Core Idea

Instead of this architecture:

```
image -> caption -> text embedding
audio -> transcript -> text embedding
pdf -> text extraction -> embedding
```

we use this architecture:

```
text
image
audio
video
pdf
   ↓
multimodal embedding model
   ↓
shared vector space
   ↓
agent retrieval
```

This enables:

text → image search
image → document search
audio → text search
video → screenshot search

within a single semantic index.

---

# Repository Goals

This project is designed to be:

Minimal
Educational
Reproducible
Agent-oriented

It is **not intended as a production system**, but as a reference architecture demonstrating how to build multimodal memory for agents.

---

# Architecture Overview

The system has three main components.

### 1 Data Ingestion

Handles ingestion of heterogeneous data.

Supported modalities:

```
text
image
audio
video
pdf
```

Each asset is converted into an embedding using Gemini embedding models.

Metadata is stored alongside the embedding.

---

### 2 Vector Memory Layer

All embeddings are stored in a **single vector database collection**.

Each vector contains:

```
embedding vector
modality
source file
uri
metadata
timestamp
```

This shared index enables cross-modal retrieval.

---

### 3 Agent Retrieval Layer

An agent can query memory using natural language.

The system:

1 embeds the query
2 searches the vector database
3 retrieves top-k results
4 sends context to an LLM
5 generates an answer grounded in the retrieved sources

---

# Technology Stack

Language

```
Python
```

Core libraries

```
google-genai
qdrant-client
fastapi
pydantic
pydantic-settings
numpy
uvicorn
```

Vector database

```
Qdrant
```

Containerization

```
Docker
Docker Compose
```

Optional visualization

```
Jupyter Notebook
```

---

# Repository Structure

```
omnimodal-agent-memory
```

```
omnimodal-agent-memory/
```

```
README.md
brief.md
requirements.txt
docker-compose.yml
.env.example
```

```
data/
```

Example multimodal dataset.

```
data/
    notes/
    images/
    pdfs/
    audio/
    video/
```

---

### Core application code

```
app/
```

```
app/
    config.py
    schemas.py
    embed.py
    ingest.py
    search.py
    agent.py
    prompts.py
    api.py
```

---

### Scripts

```
scripts/
```

```
scripts/
    load_sample_data.py
    ingest_dataset.py
    demo_query.py
```

---

### Visualization

```
notebooks/
```

```
notebooks/
    visualize_embeddings.ipynb
```

Shows embedding clusters in vector space.

---

# Data Model

Each stored object is represented as:

```
MemoryItem
```

```
id
modality
source_file
embedding
uri
metadata
created_at
```

Example:

```
{
 id: "asset_0142",
 modality: "image",
 source_file: "dashboard_error.png",
 uri: "data/images/dashboard_error.png",
 embedding: [ ... vector ... ],
 metadata: {
     description: "screenshot of dashboard error"
 }
}
```

---

# Ingestion Pipeline

The ingestion pipeline performs the following steps.

1 Load asset
2 Detect modality
3 Generate embedding
4 Store embedding in vector database
5 Store metadata

Pseudo pipeline

```
asset -> detect modality -> embedding model -> vector db
```

Example flow:

```
image -> gemini embedding -> qdrant
pdf -> gemini embedding -> qdrant
audio -> gemini embedding -> qdrant
```

#### Description Manifest

A `data/manifest.json` file maps relative file paths to human-written
descriptions.  During ingestion, each description is fused into the
embedding request alongside the raw file bytes (via `embed_file`).  This
produces richer semantic vectors — especially for modalities like short
video clips where the model alone may not extract strong textual signal.

```json
{
  "video/dashboard_demo.mp4": "Dashboard demo showing Churn Rate 4.7%",
  "images/pricing_slide.png": "Slide showing +40% price increase"
}
```

The manifest is generated by `scripts/load_sample_data.py` and consumed by
`scripts/ingest_dataset.py`.

---

# Embedding Generation

Embeddings are generated using Gemini models.

Example interface:

```
embed_text(text)
embed_image(image)
embed_audio(audio)
embed_video(video)
```

All embeddings share the same dimensionality and vector space.

---

# Vector Database

Qdrant is used as the vector store.

Collection:

```
agent_memory
```

Vector parameters:

```
size: 3072
distance: cosine
```

Payload fields:

```
modality
source
uri
metadata
timestamp
```

---

# Retrieval

Agent retrieval flow:

```
user query
↓
query embedding
↓
vector search
↓
top-k results
↓
context assembly
↓
LLM reasoning
```

Example search result:

```
1 screenshot_dashboard.png
2 pricing_update.pdf page 3
3 customer_call_audio.m4a segment 12
```

---

# Agent Interface

The agent uses a simple retrieval tool:

```
search_memory(query, top_k)
```

Example

```
search_memory("Where did the customer complain about pricing?")
```

Returns multimodal context.

The LLM then produces a grounded answer.

---

# Example Query

```
python scripts/demo_query.py
```

Input

```
"What issue did the customer mention regarding pricing?"
```

Output

```
Top results

1 screenshot_support_chat.png
2 pricing_update.pdf page 3
3 customer_call_audio segment 22

Answer

The customer complaint appears in the support screenshot and the call recording.
The issue relates to a price increase described in the PDF update.
```

---

# Demo Workflow

Step 1

Start vector database

```
docker compose up
```

---

Step 2

Load sample dataset

```
python scripts/load_sample_data.py
```

For a richer dataset with 32 files across 5 semantic themes (pricing complaint,
onboarding, security incident, product launch, hiring & culture), use:

```
python scripts/load_sample_data.py --advanced
```

The advanced dataset produces clearly visible topic-based clusters in the t-SNE
visualization notebook, demonstrating that files cluster by **semantic meaning**
rather than by modality.

---

Step 3

Ingest dataset

```
python scripts/ingest_dataset.py
```

---

Step 4

Run demo query

```
python scripts/demo_query.py
```

---

# Visualization Notebook

Notebook shows:

vector clusters
modality distribution
semantic proximity

Example experiment

Query

```
"pricing complaint"
```

Results may include:

```
audio recording
screenshot
pdf page
text note
```

---

# Why This Matters

This architecture enables a **shared semantic memory layer**.

Agents can reason across heterogeneous information sources without modality-specific pipelines.

Benefits

Lower pipeline complexity
Fewer translation steps
Better signal preservation
Unified retrieval interface

---

# Potential Extensions

Future improvements:

Temporal memory indexing
Video segment embeddings
Speech segmentation
Multimodal summarization
Agent planning with memory queries

---

# Related Concepts

Multimodal embeddings
Vector search
Retrieval augmented generation
AI agent memory
Semantic indexing

---

# License

```
MIT
```

---

# Future Roadmap

Possible next features:

web UI
agent tool interface
langchain integration
llamaindex integration
streaming ingestion
