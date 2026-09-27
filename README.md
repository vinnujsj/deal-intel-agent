# Deal Intelligence Agent

Built for **HackWithHyderabad 3.0** — an AI sales assistant that remembers every
objection, competitor mention, and pricing discussion across a deal's full call
history, and gets sharper with every interaction using **Hindsight** memory.

## Why memory matters here
- **Without memory:** every call starts from zero — rep re-explains context, forgets what worked last time.
- **With memory:** the agent recalls the full deal history instantly, briefs the rep in seconds, and surfaces which objection-handling tactics actually work — across ALL deals, not just one.

## Setup

```bash
pip install -r requirements.txt
cp .env.example .env
# fill in GROQ_API_KEY (free at https://console.groq.com/)
# fill in HINDSIGHT_API_KEY (get $50 credit with promo code MEMHACK99 at https://ui.hindsight.vectorize.io)
```

Then load the .env before running (or export the vars manually):

```bash
export $(cat .env | xargs)
streamlit run app.py
```

If `HINDSIGHT_API_KEY` is left blank, the app falls back to a local JSON mock
memory store (`.mock_memory/`) so you can build and demo the UI immediately
without waiting on API access.

## ⚠️ Before you submit: confirm the Hindsight API shape

`hindsight_client.py` currently assumes REST endpoints:
- `POST /v1/memories` — store a memory
- `POST /v1/memories/search` — semantic search
- `GET /v1/memories?user_id=...` — fetch full history

**These are placeholders** based on common memory-API patterns — verify the
actual endpoint paths, auth header format, and payload shape against:
- https://hindsight.vectorize.io/ (docs)
- https://github.com/vectorize-io/hindsight (source/examples)
- Hindsight Community Slack (for quick questions)

All Hindsight-specific code lives in `hindsight_client.py` only — once you
confirm the real API, you only need to edit that one file; `app.py` and
`agent.py` don't need to change.

## Demo script (for judges)

1. **Show the problem:** "Imagine you're a rep on your 5th call with a prospect. You don't remember what pricing you quoted or which objection you already handled."
2. **Log 2-3 fake calls** for the same deal with different notes (objections, competitor mentions, pricing) — use realistic synthetic data (see `sample_data.py`).
3. **Generate a briefing** — show it recalling specifics from all 3 calls.
4. **Cross-deal patterns tab** — log calls for 2-3 different deals, then show the agent surfacing which objection-handling tactics work across deals. This is the "memory is the star" moment — 25% of judging criteria.
5. Close with: "This isn't a chatbot that forgets — it's a rep's memory, externalized and getting smarter."

## Push to GitHub

```bash
cd deal-intel-agent
git init
git add .
git commit -m "Deal Intelligence Agent - HackWithHyderabad 3.0"
git branch -M main
git remote add origin https://github.com/vinnujsj/deal-intel-agent.git
git push -u origin main
```

(Create the empty repo on GitHub first, or swap the remote URL for whatever you name it.) `.env` and `.mock_memory/` are already git-ignored so you won't accidentally commit your API keys or local test data.

## Project structure
```
app.py                 # Streamlit UI (3 tabs: log call, briefing, cross-deal patterns)
agent.py               # Groq LLM calls (summarize, brief, find patterns)
hindsight_client.py     # Hindsight memory wrapper (+ local mock fallback)
sample_data.py          # Synthetic deal data for demoing
requirements.txt
.env.example
.gitignore
LICENSE
```

## Verified working

The mock memory layer (no API keys needed) was smoke-tested end-to-end:
storing memories, retrieving full history, and keyword search all work
correctly. Swap in your real `HINDSIGHT_API_KEY` once you've confirmed the
exact endpoint shape against the docs, and everything else keeps working
unchanged.
