"""
NOMOR 2: MEMBENTUK MATRIKS BOBOT DENGAN TF-IDF
Bobot: 40 poin
"""

import os
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer

# === KONFIGURASI PATH ===
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(BASE_DIR)

# Folder input dari hasil preprocessing (stemming)
input_folder = os.path.join(PROJECT_DIR, "stemming", "hasil_stemming")

# Folder output untuk hasil TF-IDF
output_folder = os.path.join(BASE_DIR, "hasil_tfidf")
os.makedirs(output_folder, exist_ok=True)

print("=" * 70)
print("NOMOR 2: PEMBENTUKAN MATRIKS BOBOT TF-IDF")
print("=" * 70)

# === MEMBACA DOKUMEN HASIL PREPROCESSING ===
print("\n[1] Membaca dokumen hasil preprocessing...")
files = sorted([f for f in os.listdir(input_folder) if f.endswith('.txt')])
documents = []
doc_names = []

for filename in files:
    filepath = os.path.join(input_folder, filename)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        documents.append(content)
        doc_names.append(filename.replace('.txt', ''))

print(f"   ✓ Total dokumen: {len(documents)}")

# === MENGHITUNG TF-IDF ===
print("\n[2] Menghitung TF-IDF Matrix...")

vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(documents)

print(f"   ✓ Shape matrix: {tfidf_matrix.shape}")
print(f"   ✓ Total unique terms: {len(vectorizer.get_feature_names_out())}")

# === MENYIMPAN HASIL ===
print("\n[3] Menyimpan hasil...")

with open(os.path.join(output_folder, 'tfidf_matrix.pkl'), 'wb') as f:
    pickle.dump(tfidf_matrix, f)

with open(os.path.join(output_folder, 'vectorizer.pkl'), 'wb') as f:
    pickle.dump(vectorizer, f)

with open(os.path.join(output_folder, 'doc_names.pkl'), 'wb') as f:
    pickle.dump(doc_names, f)

print(f"   ✓ tfidf_matrix.pkl")
print(f"   ✓ vectorizer.pkl")
print(f"   ✓ doc_names.pkl")

print("\n" + "=" * 70)
print("✅ NOMOR 2 SELESAI - TF-IDF MATRIX BERHASIL DIBUAT")
print("=" * 70)