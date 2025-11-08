#!/usr/bin/env python3
import os
import json
import argparse
import requests
from dotenv import load_dotenv

# Load .env variables if present
load_dotenv()

EVAL_ENDPOINT = os.getenv("EVAL_ENDPOINT", "https://mercor-dev--search-eng-interview.modal.run/evaluate")
USER_EMAIL = os.getenv("USER_EMAIL")

def evaluate(config_path: str, in_file: str):
    if not USER_EMAIL:
        raise RuntimeError("USER_EMAIL not set in environment (used as Authorization header)")

    # Load object IDs from file
    with open(in_file) as f:
        payload = json.load(f)

    # Normalize format
    if isinstance(payload, dict) and "object_ids" in payload:
        body = {
            "config_path": payload.get("config_path", config_path),
            "object_ids": payload["object_ids"]
        }
    else:
        body = {"config_path": config_path, "object_ids": payload}

    # ✅ EXACTLY replicate Postman headers
    headers = requests.structures.CaseInsensitiveDict()
    headers["Content-Type"] = "application/json"
    headers["Authorization"] = USER_EMAIL.strip()  # ensure no trailing space

    print(f"\nSubmitting evaluation for config: {config_path}")
    print(f"Endpoint: {EVAL_ENDPOINT}")
    print(f"Auth Header: {headers['Authorization']}")
    print(f"Body: {json.dumps(body, indent=2)}")

    response = requests.post(EVAL_ENDPOINT, headers=headers, json=body)

    print(f"\nStatus Code: {response.status_code}")
    try:
        print(json.dumps(response.json(), indent=2))
    except Exception:
        print(response.text)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Evaluate ranked candidates for Mercor search assignment.")
    parser.add_argument("--config", required=True, help="Config YAML file name (e.g., bankers.yml)")
    parser.add_argument("--in", dest="in_file", required=True, help="Input JSON file (e.g., top10.json)")
    args = parser.parse_args()
    evaluate(args.config, args.in_file)
