"""
EXPORT TO EXCEL - HASIL LENGKAP UTS INFORMATION RETRIEVAL
Menggabungkan hasil Nomor 2 (TF-IDF) dan Nomor 3 (Cosine Similarity)
dengan analisis dan kesimpulan lengkap
"""

import os
import pickle
import numpy as np
import pandas as pd
from datetime import datetime

print("=" * 80)
print("EXPORT HASIL UTS INFORMATION RETRIEVAL KE EXCEL")
print("=" * 80)

# === KONFIGURASI PATH ===
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

TFIDF_PATH = os.path.join(BASE_DIR, "tf-idf", "hasil_tfidf", "tfidf_matrix.pkl")
VECTORIZER_PATH = os.path.join(BASE_DIR, "tf-idf", "hasil_tfidf", "vectorizer.pkl")
DOC_NAMES_PATH = os.path.join(BASE_DIR, "tf-idf", "hasil_tfidf", "doc_names.pkl")

QUERY_PATH = os.path.join(BASE_DIR, "cosine_simmiliarity", "hasil_cosine", "query.txt")
QUERY_VECTOR_PATH = os.path.join(BASE_DIR, "cosine_simmiliarity", "hasil_cosine", "query_vector.pkl")
QUERY_COSINE_PATH = os.path.join(BASE_DIR, "cosine_simmiliarity", "hasil_cosine", "query_cosine_scores.npy")
DOC_COSINE_PATH = os.path.join(BASE_DIR, "cosine_simmiliarity", "hasil_cosine", "doc_cosine_similarity.npy")

OUTPUT_DIR = os.path.join(BASE_DIR, "hasil_excel")
os.makedirs(OUTPUT_DIR, exist_ok=True)

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
OUTPUT_PATH = os.path.join(OUTPUT_DIR, f"UTS_IR_Hasil_Lengkap_{timestamp}.xlsx")

# === LOAD SEMUA DATA ===
print("\n[1] Memuat semua data...")

# Load TF-IDF data
with open(TFIDF_PATH, "rb") as f:
    tfidf_matrix = pickle.load(f)
with open(VECTORIZER_PATH, "rb") as f:
    vectorizer = pickle.load(f)
with open(DOC_NAMES_PATH, "rb") as f:
    doc_names = pickle.load(f)

# Load Query data
with open(QUERY_PATH, "r", encoding="utf-8") as f:
    query = f.read().strip()
with open(QUERY_VECTOR_PATH, "rb") as f:
    query_vector = pickle.load(f)

query_cosine_scores = np.load(QUERY_COSINE_PATH)
doc_cosine_sim = np.load(DOC_COSINE_PATH)

print(f"   ✓ TF-IDF Matrix: {tfidf_matrix.shape}")
print(f"   ✓ Query: '{query}'")
print(f"   ✓ Cosine Similarity: {query_cosine_scores.shape}")

# === EKSTRAK KOMPONEN ===
print("\n[2] Mengekstrak komponen TF-IDF dan Cosine...")

terms = vectorizer.get_feature_names_out()
doc_labels = [f"D{i+1}" for i in range(len(doc_names))]

# TF-IDF arrays
tfidf_array = tfidf_matrix.toarray()
query_tfidf = query_vector.toarray().flatten()

# DF dan IDF
df = np.array((tfidf_matrix > 0).sum(axis=0)).flatten()
N = len(doc_names)
d_per_df = N / df
idf = vectorizer.idf_

print(f"   ✓ Total terms: {len(terms)}")
print(f"   ✓ Total dokumen: {N}")

# === MEMBUAT TABEL LENGKAP (SEPERTI FORMAT SOAL) ===
print("\n[3] Membuat tabel lengkap seperti format UTS...")

# Tabel utama: Term, TF(D1), TF(D2), TF(D3), TF(Q), df, D/df, IDF, Q, D1, D2, D3
main_table = pd.DataFrame({'Term (Kata)': terms})

# Kolom TF untuk setiap dokumen
for i, label in enumerate(doc_labels):
    main_table[f'TF({label})'] = tfidf_array[i]

# Kolom TF(Q)
main_table['TF(Q)'] = query_tfidf

# Kolom df, D/df, IDF
main_table['df'] = df
main_table['D/df'] = d_per_df
main_table['IDF (log D/df)'] = idf

# Kolom Q (sama dengan TF(Q) karena sudah TF-IDF)
main_table['Q'] = query_tfidf

# Kolom Cosine Similarity untuk setiap dokumen
for i, label in enumerate(doc_labels):
    main_table[label] = query_cosine_scores[i]

print("   ✓ Tabel utama lengkap")

# === RANKING DOKUMEN ===
print("\n[4] Membuat ranking dokumen...")

ranking_df = pd.DataFrame({
    'Ranking': range(1, len(doc_labels) + 1),
    'Dokumen': doc_labels,
    'Nama File': doc_names,
    'Cosine Similarity': query_cosine_scores,
    'Persentase': query_cosine_scores * 100,
    'Status': ['Relevan' if score > 0 else 'Tidak Relevan' for score in query_cosine_scores]
})

ranking_df = ranking_df.sort_values('Cosine Similarity', ascending=False).reset_index(drop=True)
ranking_df['Ranking'] = range(1, len(ranking_df) + 1)

most_relevant = ranking_df.iloc[0]

print(f"   ✓ Dokumen paling relevan: {most_relevant['Dokumen']} ({most_relevant['Cosine Similarity']:.4f})")

# === TF-IDF MATRIX (TRANSPOSA) ===
tfidf_matrix_df = pd.DataFrame(
    tfidf_array.T,
    index=terms,
    columns=doc_labels
)

# === DF DAN IDF ===
df_idf_df = pd.DataFrame({
    'Term': terms,
    'df (Document Frequency)': df,
    'D/df': d_per_df,
    'IDF (log D/df)': idf
})

# === COSINE SIMILARITY ANTAR DOKUMEN ===
cosine_matrix_df = pd.DataFrame(
    doc_cosine_sim,
    columns=doc_labels,
    index=doc_labels
)

# === ANALISIS QUERY ===
print("\n[5] Menganalisis query...")

query_terms_indices = np.where(query_tfidf > 0)[0]
query_terms_analysis = pd.DataFrame({
    'Term': [terms[i] for i in query_terms_indices],
    'TF-IDF Weight': [query_tfidf[i] for i in query_terms_indices],
    'IDF': [idf[i] for i in query_terms_indices],
    'Muncul di Dokumen': [
        ', '.join([doc_labels[j] for j in range(N) if tfidf_array[j][i] > 0])
        for i in query_terms_indices
    ]
})

print(f"   ✓ Query memiliki {len(query_terms_indices)} term")

# === STATISTIK ===
print("\n[6] Menghitung statistik...")

stats_df = pd.DataFrame({
    'Metrik': [
        'Total Dokumen',
        'Total Unique Terms',
        'Query',
        'Total Terms dalam Query',
        'Dokumen Paling Relevan',
        'Similarity Score Tertinggi',
        'Persentase Kesamaan',
        'Dokumen Relevan (score > 0)',
        'Dokumen Tidak Relevan (score = 0)',
        'Rata-rata Similarity',
        'Terms dengan df=1',
        'Terms dengan df=2',
        'Terms dengan df=3',
        'IDF Maksimum',
        'IDF Minimum'
    ],
    'Nilai': [
        N,
        len(terms),
        query,
        len(query_terms_indices),
        f"{most_relevant['Dokumen']} ({most_relevant['Nama File']})",
        f"{most_relevant['Cosine Similarity']:.4f}",
        f"{most_relevant['Persentase']:.2f}%",
        np.sum(query_cosine_scores > 0),
        np.sum(query_cosine_scores == 0),
        f"{np.mean(query_cosine_scores):.4f}",
        np.sum(df == 1),
        np.sum(df == 2),
        np.sum(df == 3),
        f"{idf.max():.4f}",
        f"{idf.min():.4f}"
    ]
})

print("   ✓ Statistik selesai")

# === KESIMPULAN ===
print("\n[7] Membuat kesimpulan...")

kesimpulan_text = f"""
KESIMPULAN ANALISIS INFORMATION RETRIEVAL
==========================================

1. QUERY YANG DIGUNAKAN
   "{query}"

2. METODE YANG DIGUNAKAN
   - Preprocessing: Tokenisasi, Stopword Removal, Stemming
   - TF-IDF (Term Frequency - Inverse Document Frequency)
   - Cosine Similarity

3. HASIL PERHITUNGAN TF-IDF
   - Total dokumen: {N}
   - Total unique terms: {len(terms)}
   - Terms dalam query: {len(query_terms_indices)} term
   
4. HASIL COSINE SIMILARITY
   Ranking dokumen berdasarkan relevansi dengan query:
"""

for idx, row in ranking_df.iterrows():
    kesimpulan_text += f"\n   {row['Ranking']}. {row['Dokumen']} ({row['Nama File']})\n"
    kesimpulan_text += f"      - Similarity Score: {row['Cosine Similarity']:.4f}\n"
    kesimpulan_text += f"      - Persentase: {row['Persentase']:.2f}%\n"
    kesimpulan_text += f"      - Status: {row['Status']}\n"

kesimpulan_text += f"""
5. DOKUMEN PALING RELEVAN
   {most_relevant['Dokumen']} - {most_relevant['Nama File']}
   Similarity Score: {most_relevant['Cosine Similarity']:.4f} ({most_relevant['Persentase']:.2f}%)

6. INTERPRETASI HASIL
   - Cosine Similarity berkisar dari 0 (tidak relevan) hingga 1 (sangat relevan)
   - Dokumen {most_relevant['Dokumen']} memiliki kesamaan tertinggi dengan query
   - Query "{query}" ditemukan {len(query_terms_indices)} term dalam vocabulary
   
7. KESIMPULAN
   Berdasarkan perhitungan TF-IDF dan Cosine Similarity, dokumen yang paling
   relevan dengan query "{query}" adalah {most_relevant['Dokumen']} 
   dengan similarity score {most_relevant['Cosine Similarity']:.4f} ({most_relevant['Persentase']:.2f}%).
"""

kesimpulan_df = pd.DataFrame({
    'Kesimpulan': [kesimpulan_text]
})

print("   ✓ Kesimpulan selesai")

# === SIMPAN KE EXCEL ===
print("\n[8] Menyimpan ke Excel dengan multiple sheets...")

with pd.ExcelWriter(OUTPUT_PATH, engine='openpyxl') as writer:
    # Sheet 1: Tabel Lengkap (Format Soal)
    main_table.to_excel(writer, sheet_name="1. Tabel Lengkap", index=False)
    
    # Sheet 2: Ranking Dokumen
    ranking_df.to_excel(writer, sheet_name="2. Ranking Dokumen", index=False)
    
    # Sheet 3: TF-IDF Matrix
    tfidf_matrix_df.to_excel(writer, sheet_name="3. TF-IDF Matrix")
    
    # Sheet 4: DF dan IDF
    df_idf_df.to_excel(writer, sheet_name="4. DF-IDF", index=False)
    
    # Sheet 5: Cosine Similarity Antar Dokumen
    cosine_matrix_df.to_excel(writer, sheet_name="5. Cosine Antar Dokumen")
    
    # Sheet 6: Analisis Query
    query_terms_analysis.to_excel(writer, sheet_name="6. Analisis Query", index=False)
    
    # Sheet 7: Statistik
    stats_df.to_excel(writer, sheet_name="7. Statistik", index=False)
    
    # Sheet 8: Kesimpulan
    kesimpulan_df.to_excel(writer, sheet_name="8. Kesimpulan", index=False)

print(f"\n   ✓ File Excel berhasil dibuat!")
print(f"   ✓ Lokasi: {OUTPUT_PATH}")

# === TAMPILKAN KESIMPULAN DI CONSOLE ===
print("\n" + "=" * 80)
print("KESIMPULAN")
print("=" * 80)
print(kesimpulan_text)
print("=" * 80)
print(f"\nEXPORT SELESAI - Silakan buka file Excel untuk hasil lengkap")
print("=" * 80)