import os, json, datetime, requests

ORCID = "0009-0003-1338-6336"
headers = {"Authorization": f"Bearer {os.environ['ADS_API_TOKEN']}"}

r = requests.get(
    "https://api.adsabs.harvard.edu/v1/search/query",
    headers=headers,
    params={"q": f"orcid:{ORCID}", "fl": "bibcode,citation_count", "rows": 200},
)
r.raise_for_status()
docs = r.json()["response"]["docs"]

counts = sorted((d.get("citation_count", 0) for d in docs), reverse=True)
h_index = sum(1 for i, c in enumerate(counts, start=1) if c >= i)

with open("citations.json", "w") as f:
    json.dump({
        "papers": len(docs),
        "citations": sum(counts),
        "h_index": h_index,
        "updated": datetime.date.today().isoformat(),
    }, f)