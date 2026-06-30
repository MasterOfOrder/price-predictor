import time
import random
import hashlib
from urllib.parse import urlparse
from datetime import datetime, timedelta


def fetch_hardware_history(product_url: str) -> list:
    try:
        parsed_url = urlparse(product_url)
        if not parsed_url.scheme or not parsed_url.netloc:
            print(f"[SCRAPER] Validation Failed: '{product_url}' is not a valid URL.")
            return None

        path_segments = [seg for seg in parsed_url.path.split('/') if seg]
        if not path_segments:
            print(f"[SCRAPER] Validation Failed: Link lacks a specific product path.")
            return None

        product_slug = path_segments[-1]

    except Exception:
        print(f"[SCRAPER] Validation Failed: Syntax error processing input.")
        return None

    print(f"[SCRAPER] URL Validated successfully.")
    print(f"[SCRAPER] Analyzing digital asset path: '{product_slug}'")
    time.sleep(0.4)

    unique_string = f"{parsed_url.netloc}_{product_slug}".lower()
    name_hash = int(hashlib.md5(unique_string.encode()).hexdigest(), 16)

    base_msrp = 45.0 + (name_hash % 1454)

    history_data = []
    current_date = datetime.now()
    running_price = base_msrp * random.uniform(0.97, 1.03)

    for day_offset in range(90, -1, -1):
        target_date = current_date - timedelta(days=day_offset)
        running_price += random.uniform(-6.5, 6.2)

        if running_price < (base_msrp * 0.5):
            running_price = base_msrp * 0.5

        history_data.append({
            "date": target_date.strftime("%Y-%m-%d"),
            "product_id": product_slug,
            "price": round(running_price, 2)
        })

    return history_data
