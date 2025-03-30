import os
import json
import asyncio
from collections import defaultdict
from dotenv import load_dotenv
from google import generativeai as genai
from aiolimiter import AsyncLimiter
import math
import re
import time

load_dotenv(override=True)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
CLEANED_DATA_DIR = "./cleaned_Knot_Data"
OUTPUT_PATH = "./profiles/key_profiles_gemini.json"
os.makedirs('./profiles', exist_ok=True)

genai.configure(api_key=GEMINI_API_KEY)
MODEL = genai.GenerativeModel("gemini-1.5-pro")

limiter = AsyncLimiter(1, 2)  
BATCH_SIZE = 5

def merge_user_data_by_id():
    user_data = defaultdict(lambda: defaultdict(list))
    for filename in os.listdir(CLEANED_DATA_DIR):
        if filename.endswith('.json'):
            platform = filename.replace('.json', '')
            with open(os.path.join(CLEANED_DATA_DIR, filename), 'r', encoding='utf-8') as f:
                try:
                    data = json.load(f)
                    if isinstance(data, dict):
                        data = list(data.values())
                    for entry in data:
                        if not isinstance(entry, dict):
                            continue
                        uid = str(entry.get("id") or entry.get("user_id"))
                        if not uid:
                            continue
                        user_data[uid][platform].append(entry)
                except Exception as e:
                    print(f"❌ Error reading {filename}: {e}")
    return user_data


async def generate_profile_async(user_id, record):
    prompt = f"""
You are an assistant helping to extract key user preferences from multi-platform activity data. 
Given the raw data from various services like Uber, Spotify, Netflix, UberEats, Walmart, Doordash, and Instacart, identify the following:

1. interest: list of interests or passions the user has.
2. avoid: topics or content the user likely dislikes.
3. Per-platform summary: For each platform, list 2-4 most important signals, such as favorite foods, music genres, shopping items, or locations.

Return the result as a JSON object like this:

{{
  "user_id": "{user_id}",
  "interest": [...],
  "avoid": [...],
  "Spotify": [...],
  "UberEats": [...],
  "Netflix": [...],
  "Uber": [...],
  "Walmart": [...],
  "Doordash": [...],
  "Instacart": [...]
}}

Here is the raw user data:

{json.dumps(record, indent=2)}
"""
    async with limiter:
        try:
            response = await MODEL.generate_content_async(prompt)
            text = response.text.strip()
            if text.startswith("```json"):
                text = re.sub(r"^```json\s*", "", text)  
                text = re.sub(r"\s*```$", "", text)  

            if not text.startswith("{") or not text.endswith("}"):
                raise ValueError("Gemini response is not valid JSON.")
            return json.loads(text)
        except Exception as e:
            msg = str(e)

            if "429" in msg:
                retry_match = re.search(r"retry_delay\s*{\s*seconds:\s*(\d+)", msg)
                wait_time = int(retry_match.group(1)) if retry_match else 20
                print(f"⏳ Hit rate limit for user {user_id}, retrying after {wait_time}s...")
                await asyncio.sleep(wait_time)
                return await generate_profile_async(user_id, record)
            else:
                print(f"❌ Error for user {user_id}: {e}")
                return {"user_id": user_id, "error": str(e)}


async def main():
    all_user_data = merge_user_data_by_id()
    user_items = list(all_user_data.items())
    total_batches = math.ceil(len(user_items) / BATCH_SIZE)
    all_profiles = []

    for i in range(total_batches):
        batch = user_items[i * BATCH_SIZE : (i + 1) * BATCH_SIZE]
        print(f"\n🚀 Processing batch {i+1}/{total_batches} with {len(batch)} users...")
        tasks = [generate_profile_async(uid, data) for uid, data in batch]
        results = await asyncio.gather(*tasks)
        all_profiles.extend(results)

        with open(f"./profiles/batch_{i+1}.json", "w", encoding="utf-8") as f:
            json.dump(results, f, ensure_ascii=False, indent=2)

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(all_profiles, f, ensure_ascii=False, indent=2)

    print(f"\n✅ Done! Saved {len(all_profiles)} profiles to {OUTPUT_PATH}")

if __name__ == "__main__":
    asyncio.run(main())
