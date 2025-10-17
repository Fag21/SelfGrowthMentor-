import requests
import random
from .models import Quote, Biography

def fetch_random_quote():
    try:
        resp = requests.get("https://api.quotable.io/random", timeout=8)
        if resp.status_code == 200:
            data = resp.json()
            return {"text": data.get("content"), "author": data.get("author")}
    except Exception as e:
        print("⚠️ Quote fetch error:", e)

    # fallback to local DB
    local = Quote.objects.order_by("?").first()
    if local:
        return {"text": local.text, "author": local.author or "Unknown"}
    else:
        return {"text": "Keep moving forward.", "author": "Unknown"}


def fetch_biography_from_wikipedia(name):
    try:
        url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{name.replace(' ', '%20')}"
        resp = requests.get(url, timeout=8)
        if resp.status_code == 200:
            data = resp.json()
            return {
                "title": data.get("title"),
                "summary": data.get("extract"),
                "image_url": data.get("thumbnail", {}).get("source"),
            }
    except Exception as e:
        print("⚠️ Biography fetch error:", e)

    # fallback to local DB
    local = Biography.objects.filter(name__icontains=name).first() or Biography.objects.order_by("?").first()
    if local:
        return {
            "title": local.name,
            "summary": local.full_story[:400] + "...",
            "image_url": local.image.url if local.image else None,
        }
    else:
        return {
            "title": "Unknown",
            "summary": "Every successful person starts somewhere — write your own story.",
            "image_url": None,
        }
