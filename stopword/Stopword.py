import os
from nltk.corpus import stopwords
import nltk

nltk.download('stopwords')

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(BASE_DIR)

input_folder = os.path.join(PROJECT_DIR, "basic_preprocessing", "hasil_basic_preprocessing")
output_folder = os.path.join(BASE_DIR, "hasil_stopword")
os.makedirs(output_folder, exist_ok=True)

stop_words = set(stopwords.words('indonesian'))

for filename in os.listdir(input_folder):
    if filename.endswith('.txt'):
        input_path = os.path.join(input_folder, filename)
        output_path = os.path.join(output_folder, filename)

        with open(input_path, 'r', encoding='utf-8') as f:
            tokens = f.read().split()

        filtered = [w for w in tokens if w not in stop_words]

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(' '.join(filtered))

        print(f"{filename} berhasil di-stopword removal.")
