from apify_client import ApifyClient
import pandas as pd
import os

# Ganti dengan API token kamu dari apify.com
APIFY_TOKEN = os.environ.get("APIFY_TOKEN")

client = ApifyClient(APIFY_TOKEN)

# Ganti dengan link video TikTok yang mau di-scrape
video_url = "https://www.tiktok.com/@detikcom/video/7683558338289782036?is_from_webapp=1&sender_device=pc"

# Konfigurasi input untuk actor scraper komentar
run_input = {
    "postURLs": [video_url],
    "commentsPerPost": 100,
    "maxRepliesPerComment": 0,
}

print("Menjalankan scraper di Apify...")

# ID actor "TikTok Comments Scraper" dari Apify Store
run = client.actor("clockworks/tiktok-comments-scraper").call(run_input=run_input)

# Ambil hasilnya dari dataset
comments = []
for item in client.dataset(run["defaultDatasetId"]).iterate_items():
    comments.append({
        "username": item.get("uniqueId", ""),
        "comment_text": item.get("text", ""),
        "likes_count": item.get("diggCount", 0),
        "create_time": item.get("createTimeISO", ""),
    })

df = pd.DataFrame(comments)
df.to_csv("tiktok_comments_prabowo.csv", index=False, encoding="utf-8-sig")

print(f"Berhasil scraping {len(df)} komentar")
print(f"Tersimpan di: tiktok_comments_prabowo.csv")
print(df.head())