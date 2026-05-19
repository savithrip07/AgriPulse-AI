"""
Rescore pipeline - demotes visited retailers to LOW_PRIORITY via the API.
Usage:
    python rescore.py RTL_00115
    python rescore.py RTL_00115 RTL_00120 RTL_00113
"""
import sys
import requests

API_URL = 'https://kisaansakhi-api.onrender.com/api/v1/sync/rescore'
TOKEN   = 'agripulse-hackathon-secret-key-2026'

retailer_ids = sys.argv[1:]

if not retailer_ids:
    print("Usage: python rescore.py RTL_00115 [RTL_00120 ...]")
    sys.exit(1)

print(f"Demoting {len(retailer_ids)} retailer(s) to LOW_PRIORITY: {retailer_ids}")

r = requests.post(
    API_URL,
    json=retailer_ids,
    headers={'Authorization': f'Bearer {TOKEN}', 'Content-Type': 'application/json'},
    timeout=30,
)

if r.status_code == 200:
    data = r.json()
    for rid in data.get('updated', []):
        print(f"  Demoted {rid} to LOW_PRIORITY")
    for rid in data.get('not_found', []):
        print(f"  WARNING: {rid} not found in daily_scores")
    print("Done. Refresh the app to see updated scores.")
else:
    print(f"ERROR: API returned {r.status_code}: {r.text}")
    sys.exit(1)
