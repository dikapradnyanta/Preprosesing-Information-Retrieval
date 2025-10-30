# 📚 Information Retrieval System - UTS Project
---

## 📖 Deskripsi Proyek

Sistem Information Retrieval lengkap yang mengimplementasikan preprocessing teks, perhitungan TF-IDF, dan Cosine Similarity untuk mengukur relevansi dokumen terhadap query **"Universitas Primakara"**.

### 🎯 Tujuan
1. Membangun sistem IR lengkap untuk memproses dokumen teks
2. Mengimplementasikan teknik preprocessing komprehensif
3. Menghitung matriks bobot menggunakan TF-IDF
4. Mengukur relevansi dokumen dengan Cosine Similarity
5. Menghasilkan ranking dokumen berdasarkan relevansi

---

## 🏗️ Struktur Proyek

```
project/
│
├── bahan/                          # Dokumen sumber (DOC 1-3.txt)
│
├── translate/                      # Modul 1: Translasi
│   ├── translate.py
│   ├── hasil_translate/
│   └── translate_cache.json
│
├── basic_preprocessing/            # Modul 2: Basic Preprocessing
│   ├── basic_prosesing.py
│   └── hasil_preprocessing/
│
├── stopword/                       # Modul 3: Stopword Removal
│   ├── Stopword.py
│   └── hasil_stopword/
│
├── stemming/                       # Modul 4: Stemming
│   ├── steming.py
│   └── hasil_stemming/
│
├── tf-idf/                         # Modul 5: TF-IDF
│   ├── tfidf_vector.py
│   └── hasil_tfidf/
│       ├── tfidf_matrix.pkl
│       ├── vectorizer.pkl
│       └── doc_names.pkl
│
├── cosine_simmiliarity/           # Modul 6: Cosine Similarity
│   ├── cosine_similarity.py
│   └── hasil_cosine/
│       ├── query.txt
│       ├── query_vector.pkl
│       ├── query_cosine_scores.npy
│       └── doc_cosine_similarity.npy
│
├── hasil_excel/                    # Output Laporan Excel
│   └── UTS_IR_Hasil_Lengkap_*.xlsx
│
├── export_to_excel.py             # Generator Laporan Excel
├── run_script.bat                 # Automation Script
└── README.md
```

---

## 🔧 Teknologi & Library

### Bahasa Pemrograman
- **Python 3.8+**

### Library Utama
| Library | Versi | Fungsi |
|---------|-------|--------|
| `nltk` | 3.8+ | Tokenisasi dan Stopwords |
| `scikit-learn` | 1.3+ | TF-IDF dan Cosine Similarity |
| `Sastrawi` | 1.2+ | Stemming Bahasa Indonesia |
| `pandas` | 2.0+ | Manipulasi Data |
| `openpyxl` | 3.1+ | Export ke Excel |
| `openai` | 1.0+ | Translasi (API) |
| `langdetect` | 1.0+ | Deteksi Bahasa |
| `python-dotenv` | 1.0+ | Environment Variables |

---

## ⚙️ Instalasi

### 1. Clone Repository
```bash
git clone <repository-url>
cd information-retrieval-uts
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

**requirements.txt:**
```txt
nltk==3.8.1
scikit-learn==1.3.0
Sastrawi==1.2.0
pandas==2.0.3
openpyxl==3.1.2
openai==1.3.0
langdetect==1.0.9
python-dotenv==1.0.0
numpy==1.24.3
```

### 3. Download NLTK Data
```python
import nltk
nltk.download('punkt')
nltk.download('stopwords')
```

### 4. Setup Environment (Opsional untuk Translasi)
Buat file `.env` di folder `translate/`:
```env
OPENAI_API_KEY=your_openai_api_key_here
```

---

## 🚀 Cara Penggunaan

### Metode 1: Automated (Direkomendasikan)
Jalankan seluruh pipeline dengan satu perintah:

```bash
run_script.bat
```

Script akan menjalankan secara berurutan:
1. ✅ Translasi dokumen
2. ✅ Basic preprocessing
3. ✅ Stopword removal
4. ✅ Stemming
5. ✅ TF-IDF calculation
6. ✅ Cosine similarity
7. ✅ Export ke Excel

### Metode 2: Manual (Step-by-step)

#### Step 1: Translasi
```bash
python translate/translate.py
```

#### Step 2: Basic Preprocessing
```bash
python basic_preprocessing/basic_prosesing.py
```

#### Step 3: Stopword Removal
```bash
python stopword/Stopword.py
```

#### Step 4: Stemming
```bash
python stemming/steming.py
```

#### Step 5: TF-IDF
```bash
python tf-idf/tfidf_vector.py
```

#### Step 6: Cosine Similarity
```bash
python cosine_simmiliarity/cosine_similarity.py
```

#### Step 7: Export ke Excel
```bash
python export_to_excel.py
```

---

## 📊 Output

### File Excel Output
File: `hasil_excel/UTS_IR_Hasil_Lengkap_YYYYMMDD_HHMMSS.xlsx`

**8 Sheets:**
1. **Tabel Lengkap** - Perhitungan TF-IDF dan Cosine lengkap
2. **Ranking Dokumen** - Ranking berdasarkan relevansi
3. **TF-IDF Matrix** - Matrix bobot TF-IDF
4. **DF-IDF** - Document Frequency dan IDF
5. **Cosine Antar Dokumen** - Similarity matrix
6. **Analisis Query** - Breakdown query "Universitas Primakara"
7. **Statistik** - Metrik sistem
8. **Kesimpulan** - Kesimpulan lengkap

### Format Ranking Dokumen
| Ranking | Dokumen | Cosine Similarity | Status |
|---------|---------|-------------------|--------|
| 1 | D2 | 0.7854 | Relevan |
| 2 | D1 | 0.3421 | Relevan |
| 3 | D3 | 0.0000 | Tidak Relevan |

---

## 🔄 Alur Kerja Sistem

```
┌─────────────────┐
│ Dokumen Mentah  │
│   (bahan/)      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   Translasi     │ translate.py
│  (Indonesia)    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│     Cleaning    │ basic_prosesing.py
│   Tokenisasi    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│    Stopword     │ Stopword.py
│    Removal      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│    Stemming     │ steming.py
│  (Bentuk Dasar) │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│    TF-IDF       │ tfidf_vector.py
│   Vectorizer    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│     Cosine      │ cosine_similarity.py
│   Similarity    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Laporan Excel  │ export_to_excel.py
│   (8 Sheets)    │
└─────────────────┘
```

---

## 📝 Query yang Digunakan

**Query:** `"Universitas Primakara"`

**Preprocessing Query:**
1. **Tokenisasi**: ["universitas", "primakara"]
2. **Lowercase**: ["universitas", "primakara"]
3. **Stemming**: ["universitas", "primakara"]
4. **TF-IDF Transform**: Vector [61 dimensi]

---

## 🧮 Metode yang Diimplementasikan

### 1. Text Preprocessing
- **Case Folding**: Mengubah ke lowercase
- **Cleaning**: Menghapus karakter khusus
- **Tokenisasi**: NLTK word_tokenize
- **Stopword Removal**: NLTK Indonesian stopwords
- **Stemming**: Sastrawi Stemmer

### 2. TF-IDF (Term Frequency-Inverse Document Frequency)
```
TF-IDF(t,d) = TF(t,d) × IDF(t)
IDF(t) = log(N / df(t))
```

### 3. Cosine Similarity
```
similarity = cos(θ) = (A · B) / (||A|| × ||B||)
```

**Range:** 0 (tidak relevan) hingga 1 (sangat relevan)

---

## 📈 Hasil Perhitungan

### Statistik Sistem
- **Total Dokumen**: 3
- **Total Unique Terms**: 61
- **Dokumen Paling Relevan**: D2 (DOC 2)
- **Similarity Score Tertinggi**: ~0.78
- **Query Terms**: 2 terms

### Interpretasi
- Dokumen dengan skor **> 0.7**: Sangat relevan
- Dokumen dengan skor **0.3-0.7**: Cukup relevan
- Dokumen dengan skor **< 0.3**: Kurang relevan
- Dokumen dengan skor **0.0**: Tidak relevan

---

## 🐛 Troubleshooting

### Error: NLTK Data Not Found
```bash
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')"
```

### Error: OpenAI API Key
Pastikan file `.env` ada di folder `translate/` dengan format:
```env
OPENAI_API_KEY=sk-...
```

### Error: Module Not Found
```bash
pip install -r requirements.txt
```

### Error: Permission Denied (Windows)
Jalankan Command Prompt sebagai Administrator

---

## 📄 Lisensi

Proyek ini dibuat untuk keperluan akademis UTS Information Retrieval.

---


## 🙏 Acknowledgments

- **NLTK** - Natural Language Toolkit
- **Scikit-learn** - Machine Learning Library
- **Sastrawi** - Indonesian Stemmer
- **OpenAI** - Translation API

---

**Last Updated:** Oktober 2024

---

*"Transforming unstructured text into meaningful insights through Information Retrieval"* ✨
