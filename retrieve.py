#!/usr/bin/env python3
import json
import argparse
from tpuf_client import get_namespace
from embed import Embedder


def retrieve(query: str, top_k: int = 50, out_file: str = "candidates.json"):
    e = Embedder()
    embeddings = e.embed([query])
    emb = embeddings[0]

    ns = get_namespace()
    res = ns.query(rank_by=("vector", "ANN", emb), top_k=top_k, include_attributes=True)
    rows = [r for r in res.rows]

    # convert to JSON serializable form (rows may be custom objects)
    serial = []
    for r in rows:
        # r is likely a dict-like object; attempt to convert
        if hasattr(r, 'to_dict'):
            serial.append(r.to_dict())
        elif isinstance(r, dict):
            serial.append(r)
        else:
            serial.append(dict(r))

    with open(out_file, 'w') as f:
        json.dump(serial, f, indent=2)
    print(f"Wrote {len(serial)} candidates to {out_file}")


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--query', required=True)
    p.add_argument('--top_k', type=int, default=50)
    p.add_argument('--out', dest='out_file', default='candidates.json')
    args = p.parse_args()
    retrieve(args.query, args.top_k, args.out_file)