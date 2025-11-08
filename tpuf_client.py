import os
from typing import Any
import turbopuffer

TPUF_API_KEY = os.getenv("TURBOPUFFER_API_KEY")
TPUF_REGION = os.getenv("TPUF_REGION", "aws-us-west-2")
NAMESPACE_NAME = os.getenv("TPUF_NAMESPACE", "search-test-v4")


def get_namespace():
    if not TPUF_API_KEY:
        raise RuntimeError("TURBOPUFFER_API_KEY not set in environment")
    client = turbopuffer.Turbopuffer(api_key=TPUF_API_KEY, region=TPUF_REGION)
    ns = client.namespace(NAMESPACE_NAME)
    return ns


if __name__ == "__main__":
    ns = get_namespace()
    print("Connected to namespace", NAMESPACE_NAME)