"""
NOMOR 3: MENGHITUNG COSINE SIMILARITY DENGAN KATA KUNCI
Query: "Universitas Primakara"
Bobot: 40 poin
"""

import os
import pickle
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

# === KONFIGURASI PATH ===
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(BASE_DIR)

# Folder input dari hasil TF-IDF (nomor 2)
tfidf_folder = os.path.join(PROJECT_DIR, "tf-idf", "hasil_tfidf")

# Folder output untuk hasil Cosine Similarity
output_folder = os.path.join(BASE_DIR, "hasil_cosine")
os.makedirs(output_folder, exist_ok=True)

print("=" * 70)
print("NOMOR 3: MENGHITUNG COSINE SIMILARITY DENGAN QUERY")
print("=" * 70)

# === LOAD DATA TF-IDF DARI NOMOR 2 ===
print("\n[1] Memuat data TF-IDF dari Nomor 2...")

with open(os.path.join(tfidf_folder, 'tfidf_matrix.pkl'), 'rb') as f:
    tfidf_matrix = pickle.load(f)

with open(os.path.join(tfidf_folder, 'vectorizer.pkl'), 'rb') as f:
    vectorizer = pickle.load(f)

with open(os.path.join(tfidf_folder, 'doc_names.pkl'), 'rb') as f:
    doc_names = pickle.load(f)

print(f"   ✓ TF-IDF Matrix: {tfidf_matrix.shape}")
print(f"   ✓ Total dokumen: {len(doc_names)}")

# === QUERY INPUT (SESUAI SOAL) ===
QUERY = "Universitas Primakara"

print(f"\n[2] Query: '{QUERY}'")

# === TRANSFORM QUERY ===
print("\n[3] Memproses query dengan vectorizer...")

query_vector = vectorizer.transform([QUERY])

print(f"   ✓ Query vector shape: {query_vector.shape}")

# === MENGHITUNG COSINE SIMILARITY ===
print("\n[4] Menghitung Cosine Similarity...")

# Cosine similarity query dengan dokumen
query_cosine_scores = cosine_similarity(query_vector, tfidf_matrix).flatten()

# Cosine similarity antar dokumen
doc_cosine_sim = cosine_similarity(tfidf_matrix)

print(f"   ✓ Query similarity calculated")
print(f"   ✓ Document similarity matrix: {doc_cosine_sim.shape}")

# === MENYIMPAN HASIL ===
print("\n[5] Menyimpan hasil...")

# Simpan query info
with open(os.path.join(output_folder, 'query.txt'), 'w', encoding='utf-8') as f:
    f.write(QUERY)

# Simpan query vector
with open(os.path.join(output_folder, 'query_vector.pkl'), 'wb') as f:
    pickle.dump(query_vector, f)

# Simpan cosine scores
np.save(os.path.join(output_folder, 'query_cosine_scores.npy'), query_cosine_scores)
np.save(os.path.join(output_folder, 'doc_cosine_similarity.npy'), doc_cosine_sim)

print(f"   ✓ query.txt")
print(f"   ✓ query_vector.pkl")
print(f"   ✓ query_cosine_scores.npy")
print(f"   ✓ doc_cosine_similarity.npy")

print("\n" + "=" * 70)
print("COSINE SIMILARITY BERHASIL DIHITUNG")
print("=" * 70)