import os
import time
import json
import hashlib
from dotenv import load_dotenv
from langdetect import detect
from openai import OpenAI

# ================== KONFIGURASI ==================
load_dotenv()
API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=API_KEY)

# Path universal
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(BASE_DIR)

input_folder = os.path.join(PROJECT_DIR, "bahan")
output_folder = os.path.join(BASE_DIR, "hasil_translate")
cache_file = os.path.join(BASE_DIR, "translate_cache.json")

os.makedirs(output_folder, exist_ok=True)

# ================== LOAD CACHE ==================
if os.path.exists(cache_file):
    with open(cache_file, "r", encoding="utf-8") as f:
        cache = json.load(f)
else:
    cache = {}

# ================== FUNGSI ==================
def hash_text(text):
    """Buat hash unik dari teks untuk dijadikan key cache"""
    return hashlib.md5(text.encode("utf-8")).hexdigest()

def translate_batch(lines):
    """Terjemahkan beberapa baris sekaligus, gunakan cache jika ada"""
    result = []
    for line in lines:
        line_key = hash_text(line)
        if line.strip() == "":
            result.append("")
            continue
        if line_key in cache:
            result.append(cache[line_key])
            continue

        # Detect bahasa
        try:
            lang = detect(line)
        except:
            result.append(line)
            cache[line_key] = line
            continue

        if lang == "id":
            result.append(line)
            cache[line_key] = line
            continue

        # Terjemahkan via OpenAI
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a translator that outputs simple, literal Indonesian text. "
                                   "Keep terminology consistent, do not add extra words, and do not change names or numbers."
                    },
                    {
                        "role": "user",
                        "content": f"Translate this text to Indonesian, suitable for text retrieval:\n{line}"
                    }
                ],
                temperature=0.3
            )
            translated = response.choices[0].message.content.strip()
            result.append(translated)
            cache[line_key] = translated
            time.sleep(1)  # delay aman dari rate limit
        except Exception as e:
            print(f"Terjadi error saat translate: {e}")
            result.append(line)
            cache[line_key] = line

    return result

# ================== PROSES FILE ==================
for filename in os.listdir(input_folder):
    if filename.endswith(".txt"):
        input_path = os.path.join(input_folder, filename)
        output_path = os.path.join(output_folder, filename)

        try:
            with open(input_path, "r", encoding="utf-8") as f:
                content = f.read()

            lines = content.splitlines()
            translated_lines = translate_batch(lines)
            result_text = "\n".join(translated_lines)

            with open(output_path, "w", encoding="utf-8") as f:
                f.write(result_text)

            print(f"Berhasil translate: {filename}")

        except Exception as e:
            print(f"Gagal proses {filename}: {e}")

# ================== SIMPAN CACHE ==================
with open(cache_file, "w", encoding="utf-8") as f:
    json.dump(cache, f, ensure_ascii=False, indent=2)
