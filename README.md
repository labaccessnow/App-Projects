# Application Projects

Practical software that makes infrastructure and network operations easier to run — small,
dependable tools, increasingly with a retrieval/LLM layer so operational knowledge is searchable.

## What it looks like in practice

A minimal RAG core: embed your real runbooks/notes, index them, and retrieve the relevant chunks
to hand an LLM as context — so answers come from *your* reality, not the model's imagination:

```python
from sentence_transformers import SentenceTransformer
import faiss, numpy as np

model  = SentenceTransformer("all-MiniLM-L6-v2")
chunks = load_runbook_chunks()                       # your real notes, chunked
emb    = model.encode(chunks, normalize_embeddings=True)

index = faiss.IndexFlatIP(emb.shape[1])              # cosine via normalized dot-product
index.add(np.asarray(emb, dtype="float32"))

def context_for(question, k=5):
    q = model.encode([question], normalize_embeddings=True)
    _, ids = index.search(np.asarray(q, dtype="float32"), k)
    return [chunks[i] for i in ids[0]]               # feed THESE to the LLM; don't let it guess
```

## Best practices I follow
- **Small, composable, cron-safe.** Unix-y tools that do one thing and exit with a meaningful code.
- **Ground the model in real data.** For RAG: sane chunking, a decent embedding model, a vector
  store, and evaluation — never let an LLM freelance over infrastructure.
- **Read-only by default for ops tooling.** Observe and report before anything is allowed to mutate.
- **Secrets and state handled explicitly** — nothing in code, deterministic output.

## Lessons learned
- **Ungrounded, an LLM will confidently invent a CLI flag that doesn't exist.** RAG over the real
  docs is the difference between a useful assistant and a plausible liar. Retrieval quality —
  chunking and the embedding model — matters more than which LLM you point at it.
- **Respect the physical layer.** Opening the serial port to a microcontroller over a CH340 bridge
  *resets the board every single time* — there is no "passive read." A tool that claims to be
  read-only has to account for the transport's side effects, or your harmless check reboots the
  thing you were trying to observe.
- **The boring 20% is the reliability.** Timeouts, retries, exit codes, and "what happens when the
  device is unreachable" are what make a tool safe to run unattended from cron.

## Where the field went (dated)
- **2023–2024:** **RAG** moves from novelty to standard practice — embeddings + vector search
  (FAISS, vector databases) grounding LLM answers in your own data.
- **2024–2025:** **LLM-assisted AIOps** gets real — incident triage, root-cause analysis, and
  log-anomaly detection built on retrieval over runbooks and telemetry.
