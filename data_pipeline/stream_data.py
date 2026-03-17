"""
stream_data.py — Stream from ALL specified data sources
========================================================
Streams real data from 6 sources for the CA Insurance Chatbot MVP.
Prints raw chunks as they arrive, saves to external_data/.

Sources (all free, zero API keys):
  1. Data.gov        — CA insurance datasets (CKAN API)
  2. US Census       — CA county housing + demographics
  3. Stack Exchange   — Insurance Q&A from Money.SE
  4. World Bank      — US economic/financial indicators (replaces Nasdaq)
  5. Reddit          — r/insurance conversations
  6. Bitext-style    — Synthetic objection utterances (local)

Usage:  python data_pipeline/stream_data.py
"""
import io, sys, json, time, random
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

try:
    import requests
except ImportError:
    print("Run: pip install requests"); sys.exit(1)

OUT = Path(__file__).parent / "external_data"
OUT.mkdir(exist_ok=True)


# ═══════════════════════════════════════════════════════════
#  GENERIC STREAM HELPER
# ═══════════════════════════════════════════════════════════

def stream(name, url, desc, max_show=3):
    """Stream URL, print raw chunks live, return raw text or None."""
    print(f"\n── [{name}] {desc}")
    print(f"   URL: {url[:90]}{'...' if len(url)>90 else ''}")

    try:
        t0 = time.perf_counter()
        r = requests.get(url, timeout=20, stream=True,
                         headers={"User-Agent": "CA-InsuranceChatbot-MVP/1.0"})
        r.raise_for_status()

        raw = b""
        n = 0
        for chunk in r.iter_content(chunk_size=512):
            if not chunk: continue
            n += 1
            raw += chunk
            if n <= max_show:
                preview = chunk.decode("utf-8", errors="replace").replace("\n"," ").strip()[:68]
                ms = (time.perf_counter()-t0)*1000
                print(f"   [{ms:7.1f}ms] chunk #{n:02d}  \"{preview}...\"")

        ms = (time.perf_counter()-t0)*1000
        if n > max_show:
            print(f"   ... +{n-max_show} more chunks streamed")
        print(f"   DONE: {n} chunks | {len(raw):,} bytes | {ms:.0f}ms")
        return raw.decode("utf-8", errors="replace")

    except requests.exceptions.HTTPError as e:
        print(f"   FAIL: {e}")
        return None
    except requests.exceptions.ConnectionError:
        print(f"   FAIL: Connection refused / DNS error")
        return None
    except requests.exceptions.Timeout:
        print(f"   FAIL: Timeout after 20s")
        return None
    except Exception as e:
        print(f"   FAIL: {type(e).__name__}: {e}")
        return None


def save(name, data):
    """Save parsed data as JSON, return file size."""
    path = OUT / f"{name}.json"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    return path.stat().st_size / 1024


# ═══════════════════════════════════════════════════════════
#  SOURCE 1: DATA.GOV — CA Insurance Datasets
# ═══════════════════════════════════════════════════════════

def stream_data_gov():
    raw = stream("DATA.GOV",
        "https://data.ca.gov/api/3/action/package_search?q=insurance&rows=25",
        "California open data portal — insurance datasets")
    if not raw: return None

    data = json.loads(raw)
    results = data.get("result", {}).get("results", [])
    parsed = []
    for r in results:
        parsed.append({
            "title": r.get("title", ""),
            "notes": (r.get("notes", "") or "")[:250],
            "org": r.get("organization", {}).get("title", ""),
            "tags": [t["name"] for t in r.get("tags", [])],
        })
    print(f"   PARSED: {len(parsed)} CA insurance datasets")
    return parsed


# ═══════════════════════════════════════════════════════════
#  SOURCE 2: US CENSUS BUREAU — CA Housing + Demographics
# ═══════════════════════════════════════════════════════════

def stream_census():
    raw = stream("CENSUS",
        "https://api.census.gov/data/2022/acs/acs5?get=NAME,B25003_001E,B25003_002E,B25003_003E,B19013_001E&for=county:*&in=state:06",
        "US Census ACS 5yr — CA counties: housing, owners, renters, median income")
    if not raw: return None

    data = json.loads(raw)
    if len(data) < 2: return None
    headers = data[0]
    counties = []
    for row in data[1:]:
        rec = dict(zip(headers, row))
        total = int(rec.get("B25003_001E", 0) or 0)
        owners = int(rec.get("B25003_002E", 0) or 0)
        counties.append({
            "county": rec.get("NAME", ""),
            "total_units": total,
            "owners": owners,
            "renters": int(rec.get("B25003_003E", 0) or 0),
            "homeowner_pct": round(owners/total*100, 1) if total > 0 else 0,
            "median_income": int(rec.get("B19013_001E", 0) or 0),
        })
    counties.sort(key=lambda x: x["homeowner_pct"], reverse=True)
    print(f"   PARSED: {len(counties)} CA counties")
    if counties:
        top = counties[0]
        print(f"   TOP: {top['county']} — {top['homeowner_pct']}% homeowner, ${top['median_income']:,} income")
    return counties


# ═══════════════════════════════════════════════════════════
#  SOURCE 3: STACK EXCHANGE — Insurance Q&A
# ═══════════════════════════════════════════════════════════

def stream_stackexchange():
    raw = stream("STACK EXCHANGE",
        "https://api.stackexchange.com/2.3/search?order=desc&sort=votes&tagged=insurance&site=money&pagesize=30&filter=withbody",
        "Money.SE — Top voted insurance questions + answers")
    if not raw: return None

    data = json.loads(raw)
    items = data.get("items", [])
    parsed = []
    for i in items:
        # Strip HTML from body for clean text
        import re
        body = re.sub(r"<[^>]+>", "", i.get("body", ""))[:500]
        parsed.append({
            "title": i.get("title", ""),
            "body_preview": body,
            "score": i.get("score", 0),
            "tags": i.get("tags", []),
            "answered": i.get("is_answered", False),
            "answer_count": i.get("answer_count", 0),
        })
    print(f"   PARSED: {len(parsed)} insurance Q&A pairs")
    return parsed


# ═══════════════════════════════════════════════════════════
#  SOURCE 4: WORLD BANK — US Economic/Financial Indicators
# ═══════════════════════════════════════════════════════════

def stream_worldbank():
    """
    World Bank Open Data — zero auth, always free.
    Streams US economic indicators relevant to insurance pricing:
      - NY.GDP.MKTP.CD = US GDP (current US$)
      - FP.CPI.TOTL.ZG = Inflation rate (CPI)
    """
    # US GDP — key financial baseline
    raw = stream("WORLD BANK",
        "https://api.worldbank.org/v2/country/US/indicator/NY.GDP.MKTP.CD?format=json&per_page=30&date=2000:2024",
        "World Bank — US GDP (current US$), 2000-2024")

    if raw:
        try:
            data = json.loads(raw)
            # World Bank returns [metadata, records]
            records_raw = data[1] if len(data) > 1 else []
            records = []
            for r in records_raw:
                if r.get("value") is not None:
                    records.append({
                        "year": r.get("date", ""),
                        "indicator": r.get("indicator", {}).get("value", ""),
                        "value": r.get("value"),
                        "country": r.get("country", {}).get("value", ""),
                    })
            print(f"   PARSED: {len(records)} US GDP data points")

            # Also grab inflation/CPI for pricing context
            raw2 = stream("WORLD BANK CPI",
                "https://api.worldbank.org/v2/country/US/indicator/FP.CPI.TOTL.ZG?format=json&per_page=30&date=2000:2024",
                "World Bank — US Inflation rate (CPI %), 2000-2024")

            cpi_records = []
            if raw2:
                data2 = json.loads(raw2)
                recs2 = data2[1] if len(data2) > 1 else []
                for r in recs2:
                    if r.get("value") is not None:
                        cpi_records.append({
                            "year": r.get("date", ""),
                            "cpi_inflation_pct": round(r["value"], 2),
                        })
                print(f"   PARSED: {len(cpi_records)} CPI inflation data points")

            return {
                "source": "World Bank Open Data",
                "gdp": {"indicator": "NY.GDP.MKTP.CD", "records": records, "count": len(records)},
                "cpi": {"indicator": "FP.CPI.TOTL.ZG", "records": cpi_records, "count": len(cpi_records)},
                "count": len(records) + len(cpi_records),
            }
        except (json.JSONDecodeError, IndexError, KeyError) as e:
            print(f"   PARSE ERROR: {e}")

    return None


# ═══════════════════════════════════════════════════════════
#  SOURCE 5: REDDIT — r/insurance Conversations
# ═══════════════════════════════════════════════════════════

def stream_reddit():
    """
    Reddit's public JSON API — no auth needed for read-only.
    Pulls top posts from r/insurance for conversational training data.
    """
    raw = stream("REDDIT",
        "https://www.reddit.com/r/insurance/top.json?t=month&limit=25",
        "Reddit r/insurance — Top insurance discussions this month")
    if not raw: return None

    try:
        data = json.loads(raw)
        posts = data.get("data", {}).get("children", [])
        parsed = []
        for post in posts:
            d = post.get("data", {})
            parsed.append({
                "title": d.get("title", ""),
                "selftext": (d.get("selftext", "") or "")[:400],
                "score": d.get("score", 0),
                "num_comments": d.get("num_comments", 0),
                "subreddit": d.get("subreddit", "insurance"),
                "created_utc": d.get("created_utc", 0),
            })
        print(f"   PARSED: {len(parsed)} reddit posts from r/insurance")
        return parsed
    except (json.JSONDecodeError, KeyError) as e:
        print(f"   PARSE ERROR: {e}")
        return None


# ═══════════════════════════════════════════════════════════
#  SOURCE 6: BITEXT-STYLE SYNTHETIC — Objection Utterances
# ═══════════════════════════════════════════════════════════

def generate_synthetic():
    """
    Generate semantically equivalent objection variants locally.
    Simulates what Bitext/Gretel APIs produce for NLP training.
    No external API needed — deterministic template expansion.
    """
    print(f"\n── [SYNTHETIC] Bitext-style objection utterance generation")
    print(f"   Method: template × prefix × suffix combinatorial expansion")

    templates = {
        "already_have_insurance": [
            "I already have life insurance",
            "I'm covered already",
            "My employer provides coverage",
            "I have a policy through work",
            "I got insurance last year",
        ],
        "just_looking": [
            "I'm just looking",
            "Just browsing",
            "Not ready to buy yet",
            "I'm exploring my options",
            "Just doing some research",
        ],
        "too_expensive": [
            "It's too expensive",
            "I can't afford insurance right now",
            "That's out of my budget",
            "Insurance costs too much",
            "I don't have the money for that",
        ],
        "not_interested": [
            "I'm not interested",
            "No thanks",
            "Maybe later",
            "Not for me right now",
            "I don't think I need this",
        ],
        "need_to_think": [
            "I need to think about it",
            "Let me discuss with my spouse",
            "I'll get back to you",
            "Give me some time to decide",
            "I want to compare other options first",
        ],
    }

    prefixes = ["", "Well, ", "Actually, ", "Hmm, ", "Look, ", "You know, ",
                "To be honest, ", "Um, "]
    suffixes = ["", ".", "...", ", thanks.", ", thank you."]

    all_data = {}
    total = 0
    for obj_type, seeds in templates.items():
        variants = set()
        for seed in seeds:
            for pre in prefixes:
                for suf in suffixes:
                    v = f"{pre}{seed}{suf}".strip()
                    if v: variants.add(v)
        # Keep it manageable — sample 30 per type
        v_list = sorted(variants)
        if len(v_list) > 30:
            random.seed(42)
            v_list = random.sample(v_list, 30)
        # Always include the original seeds
        for s in seeds:
            if s not in v_list: v_list.append(s)

        all_data[obj_type] = {
            "canonical": seeds[0],
            "variants": v_list,
            "count": len(v_list),
        }
        total += len(v_list)
        print(f"   [{obj_type}] {len(v_list)} variants")

    print(f"   TOTAL: {total} synthetic utterances generated")
    return {"objections": all_data, "total": total, "method": "bitext-style template expansion"}


# ═══════════════════════════════════════════════════════════
#  MAIN — Stream all, checkpoint, report
# ═══════════════════════════════════════════════════════════

def main():
    print("=" * 58)
    print("  DATA STREAMING — ALL SOURCES")
    print("  California Insurance Chatbot MVP")
    print("=" * 58)
    print(f"  Time: {time.strftime('%Y-%m-%d %H:%M:%S')}")

    sources = {
        "data_gov":       ("Data.gov CA Insurance",    stream_data_gov),
        "census":         ("US Census CA Housing",     stream_census),
        "stack_exchange":  ("Stack Exchange Q&A",       stream_stackexchange),
        "worldbank":       ("World Bank Indicators",   stream_worldbank),
        "reddit":         ("Reddit r/insurance",       stream_reddit),
        "synthetic":      ("Bitext Synthetic",         generate_synthetic),
    }

    results = {}
    for key, (label, func) in sources.items():
        data = func()
        results[key] = data

    # ── CHECKPOINT ────────────────────────────────────────
    print(f"\n{'='*58}")
    print("  CHECKPOINT — Saving & Verifying")
    print(f"{'='*58}")

    passed = 0
    for key, data in results.items():
        if data is None:
            path = OUT / f"{key}.json"
            with open(path, "w") as f:
                json.dump({"status": "failed", "source": key}, f, indent=2)
            print(f"  [FAIL] {key}")
        else:
            kb = save(key, data)
            count = len(data) if isinstance(data, list) else data.get("total", data.get("count", "ok"))
            print(f"  [SAVE] {key + '.json':<25} {kb:>6.1f} KB  |  {count} records")
            passed += 1

    total = len(sources)
    ok = passed >= 4  # need at least 4 of 6

    print(f"\n  Streamed: {passed}/{total} sources")
    print(f"  Status : {'PASS' if ok else 'FAIL'}")
    if not ok:
        print(f"  Need at least 4/{total} sources to proceed.")
    print(f"{'='*58}")
    return ok


if __name__ == "__main__":
    ok = main()
    sys.exit(0 if ok else 1)
