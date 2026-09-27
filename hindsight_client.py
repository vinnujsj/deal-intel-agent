"""
Hindsight memory client wrapper.

Hindsight (https://hindsight.vectorize.io/) is the required memory layer for
this hackathon. This wrapper isolates ALL Hindsight-specific calls in one
place, so if the exact endpoint names/payloads differ from what's assumed
here, you only need to edit this one file.

Docs to check before the hackathon deadline:
    https://hindsight.vectorize.io/
    https://github.com/vectorize-io/hindsight

Set these env vars (or edit .env):
    HINDSIGHT_API_KEY   - from Hindsight Cloud (use promo code MEMHACK99 for $50 credit)
    HINDSIGHT_BASE_URL  - defaults to the Hindsight Cloud API base
"""

import os
import requests

HINDSIGHT_BASE_URL = os.environ.get("HINDSIGHT_BASE_URL", "https://api.hindsight.vectorize.io")
HINDSIGHT_API_KEY = os.environ.get("HINDSIGHT_API_KEY", "")


class HindsightClient:
    def __init__(self, user_id: str, base_url: str = HINDSIGHT_BASE_URL, api_key: str = HINDSIGHT_API_KEY):
        """
        user_id: use the deal/contact name (e.g. "acme-corp") as a namespace so each
                 deal's memory can be recalled independently, or use a single
                 namespace like "sales-agent" and rely on metadata filtering.
        """
        self.user_id = user_id
        self.base_url = base_url.rstrip("/")
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }

    def add_memory(self, text: str, metadata: dict | None = None):
        """Store a new memory (e.g. a call summary) for this deal."""
        payload = {
            "user_id": self.user_id,
            "content": text,
            "metadata": metadata or {},
        }
        resp = requests.post(f"{self.base_url}/v1/memories", json=payload, headers=self.headers, timeout=30)
        resp.raise_for_status()
        return resp.json()

    def search_memory(self, query: str, limit: int = 10):
        """Recall relevant memories for this deal given a query (e.g. 'objections raised')."""
        payload = {
            "user_id": self.user_id,
            "query": query,
            "limit": limit,
        }
        resp = requests.post(f"{self.base_url}/v1/memories/search", json=payload, headers=self.headers, timeout=30)
        resp.raise_for_status()
        return resp.json().get("results", [])

    def get_all_memories(self):
        """Fetch full memory history for this deal (used for the 'brief me' view)."""
        resp = requests.get(f"{self.base_url}/v1/memories", params={"user_id": self.user_id}, headers=self.headers, timeout=30)
        resp.raise_for_status()
        return resp.json().get("results", [])


class MockHindsightClient:
    """
    Local fallback so you can build/demo the UI before your Hindsight Cloud key
    is set up, or if you're offline. Swap this out for HindsightClient once
    your API key + confirmed endpoints are ready. Stores memories in a local
    JSON file per user_id under .mock_memory/.
    """

    def __init__(self, user_id: str, **kwargs):
        self.user_id = user_id
        os.makedirs(".mock_memory", exist_ok=True)
        self.path = f".mock_memory/{user_id}.json"
        if not os.path.exists(self.path):
            import json
            with open(self.path, "w") as f:
                json.dump([], f)

    def _load(self):
        import json
        with open(self.path) as f:
            return json.load(f)

    def _save(self, data):
        import json
        with open(self.path, "w") as f:
            json.dump(data, f, indent=2)

    def add_memory(self, text: str, metadata: dict | None = None):
        import datetime
        data = self._load()
        entry = {
            "content": text,
            "metadata": metadata or {},
            "timestamp": datetime.datetime.utcnow().isoformat(),
        }
        data.append(entry)
        self._save(data)
        return entry

    def search_memory(self, query: str, limit: int = 10):
        # naive keyword match for the mock version
        data = self._load()
        query_words = set(query.lower().split())
        scored = []
        for entry in data:
            content_words = set(entry["content"].lower().split())
            score = len(query_words & content_words)
            scored.append((score, entry))
        scored.sort(key=lambda x: -x[0])
        return [e for _, e in scored[:limit]]

    def get_all_memories(self):
        return self._load()


def get_client(user_id: str) -> "HindsightClient | MockHindsightClient":
    """Returns the real Hindsight client if an API key is set, else the mock fallback."""
    if HINDSIGHT_API_KEY:
        return HindsightClient(user_id)
    return MockHindsightClient(user_id)
