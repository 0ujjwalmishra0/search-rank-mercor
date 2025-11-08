import os
from typing import List
import voyageai

VOYAGE_API_KEY = os.getenv("VOYAGE_API_KEY")
VOYAGE_MODEL = os.getenv("VOYAGE_MODEL", "voyage-3")


class Embedder:
    def __init__(self, api_key: str = None, model: str = None):
        api_key = api_key or VOYAGE_API_KEY
        model = model or VOYAGE_MODEL
        if not api_key:
            raise RuntimeError("VOYAGE_API_KEY not set in environment")
        self.client = voyageai.Client(api_key=api_key)
        self.model = model

    def embed(self, texts: List[str]):
        # voyageai Client returns embeddings in .embeddings
        response = self.client.embed(texts, model=self.model)
        return response.embeddings


if __name__ == "__main__":
    e = Embedder()
    v = e.embed(["software engineer"])
    print("embedding len", len(v[0]))