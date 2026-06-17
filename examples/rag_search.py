#!/usr/bin/env python3
"""Minimal RAG retrieval core: embed notes, index them, retrieve context for an LLM.
   pip install sentence-transformers faiss-cpu numpy
"""
import faiss, numpy as np
from sentence_transformers import SentenceTransformer

MODEL = SentenceTransformer("all-MiniLM-L6-v2")

def build_index(chunks):
    emb = MODEL.encode(chunks, normalize_embeddings=True)
    index = faiss.IndexFlatIP(emb.shape[1])           # cosine via normalized dot-product
    index.add(np.asarray(emb, dtype="float32"))
    return index

def context_for(question, chunks, index, k=5):
    q = MODEL.encode([question], normalize_embeddings=True)
    _, ids = index.search(np.asarray(q, dtype="float32"), k)
    return [chunks[i] for i in ids[0]]                # feed THESE to the LLM as grounding

if __name__ == "__main__":
    docs = ["example runbook chunk A", "example runbook chunk B"]
    idx = build_index(docs)
    print(context_for("how do I ...?", docs, idx))
