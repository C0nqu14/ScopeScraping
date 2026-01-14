from concurrent.futures import ThreadPoolExecutor
import requests
from core.logger import log
import os

USERNAME = os.getenv("USERNAME")
API_TOKEN = os.getenv("API_TOKEN")
HEADERS = {"Accept": "application/json"}

def fetch_program_scopes(handle):
    url = f"https://api.hackerone.com/v1/hackers/programs/{handle}"
    try:
        r = requests.get(url, auth=(USERNAME, API_TOKEN), headers=HEADERS, timeout=10)
        if r.status_code != 200:
            log(f"[ERRO] Programa {handle}: HTTP {r.status_code}")
            return set()
        details = r.json()
        data = details.get("relationships", {}).get("structured_scopes", {}).get("data", [])
        scopes = set()
        for s in data:
            a = s.get("attributes", {})
            if a.get("asset_type") == "URL":
                scopes.add(a.get("asset_identifier"))
        log(f"[OK] Programa {handle}: {len(scopes)} escopos encontrados")
        return scopes
    except Exception as e:
        log(f"[EXCEÇÃO] Programa {handle}: {e}")
        return set()

def fetch_all_scopes():
    log("Coletando escopos da HackerOne…")
    url = "https://api.hackerone.com/v1/hackers/programs?page[size]=100&page[number]=1"
    scopes = set()

    while url:
        try:
            r = requests.get(url, auth=(USERNAME, API_TOKEN), headers=HEADERS, timeout=10)
            if r.status_code != 200:
                log(f"[ERRO] Endpoint de programas: HTTP {r.status_code}")
                break

            data = r.json()
            handles = [p["attributes"]["handle"] for p in data["data"]]

            with ThreadPoolExecutor(max_workers=10) as executor:
                results = executor.map(fetch_program_scopes, handles)
                for s in results:
                    scopes.update(s)

            url = data.get("links", {}).get("next")
            if url == data.get("links", {}).get("self"):
                break
        except Exception as e:
            log(f"[EXCEÇÃO] Coleta de programas: {e}")
            break

    log(f"Total de escopos coletados: {len(scopes)}")
    return scopes
