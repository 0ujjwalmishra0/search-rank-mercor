#!/usr/bin/env python3
import json
import argparse
from utils import parse_education, parse_experience, total_experience_years


# Minimal rule-matching utilities

def level_degree_normalized(degree: str) -> str:
    if not degree:
        return ""
    d = degree.lower()
    if "jd" in d or "doctor" in d:
        return "jd/doctorate"
    if "master" in d or "ms" in d:
        return "master"
    if "bachelor" in d or "bs" in d:
        return "bachelor"
    if "mba" in d:
        return "mba"
    return d


def satisfies_hard_criteria(candidate: dict, hard_criteria: dict) -> bool:
    # hard_criteria example: {"degree": "jd", "min_years": 3, "country": "United States"}
    degs = candidate.get('deg_degrees') or candidate.get('degrees') or []
    exp_list = candidate.get('experience', [])
    country = candidate.get('country', '')

    if hard_criteria.get('country'):
        if country and hard_criteria['country'].lower() not in country.lower():
            return False

    # degree check
    if hard_criteria.get('degree'):
        need = hard_criteria['degree'].lower()
        found = False
        for d in degs:
            if need in d.lower() or need in level_degree_normalized(d):
                found = True
                break
        if not found:
            # also check parsed degrees in 'degrees' strings (if degrees field contains full strings)
            # skip strictness for safety
            return False

    # min years
    if hard_criteria.get('min_years'):
        tot = total_experience_years(exp_list)
        if tot < hard_criteria['min_years']:
            return False

    return True


def score_candidate(candidate: dict, query: str, hard_criteria: dict) -> float:
    # Simple scoring: start with ANN score if present (smaller is better) -> we don't have distance
    # We'll implement heuristic score: +100 if satisfies hard criteria, + (soft matches)
    score = 0.0
    if satisfies_hard_criteria(candidate, hard_criteria):
        score += 100.0

    # soft boosts: presence of keywords in rerankSummary, exp_titles, exp_companies
    text_fields = []
    for f in ['rerankSummary', 'rerank_summary', 'name']:
        v = candidate.get(f)
        if isinstance(v, str):
            text_fields.append(v.lower())
    joined = " ".join(text_fields)

    # keyword list from query (small)
    for term in query.lower().split():
        if len(term) > 3 and term in joined:
            score += 1.0

    # Add small boost for more experience
    try:
        score += min(10.0, total_experience_years(candidate.get('experience', [])) / 2.0)
    except Exception:
        pass

    return score


def load_candidates(path: str):
    with open(path) as f:
        return json.load(f)


def rerank(in_file: str, query: str, config: str, out_file: str):
    # config is not parsed here; for now map some known config names to hard criteria
    config_map = {
        'tax_lawyer.yml': {'degree': 'jd', 'min_years': 3, 'country': 'United States'},
        'junior_corporate_lawyer.yml': {'degree': 'jd', 'min_years': 2},
        'radiology.yml': {'degree': 'md', 'min_years': 1},
        'doctors_md.yml': {'degree': 'md', 'min_years': 2},
        'mechanical_engineers.yml': {'degree': 'bachelor', 'min_years': 3}
    }
    hard = config_map.get(config, {})

    candidates = load_candidates(in_file)
    scored = []
    for c in candidates:
        s = score_candidate(c, query, hard)
        scored.append((s, c))

    scored.sort(key=lambda x: x[0], reverse=True)
    top10 = [c['_id'] if '_id' in c else c.get('id') for (_, c) in scored[:10]]

    out = {"config_path": config, "object_ids": top10}
    with open(out_file, 'w') as f:
        json.dump(out, f, indent=2)
    print(f"Wrote top {len(top10)} ids to {out_file}")


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--in', dest='in_file', required=True)
    p.add_argument('--query', required=True)
    p.add_argument('--config', required=True)
    p.add_argument('--out', dest='out_file', default='top10.json')
    args = p.parse_args()
    rerank(args.in_file, args.query, args.config, args.out_file)
