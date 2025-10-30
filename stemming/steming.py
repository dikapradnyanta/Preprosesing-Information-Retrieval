import os
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(BASE_DIR)

input_folder = os.path.join(PROJECT_DIR, "stopword", "hasil_stopword")
output_folder = os.path.join(BASE_DIR, "hasil_stemming")
os.makedirs(output_folder, exist_ok=True)

factory = StemmerFactory()
stemmer = factory.create_stemmer()

for filename in os.listdir(input_folder):
    if filename.endswith('.txt'):
        input_path = os.path.join(input_folder, filename)
        output_path = os.path.join(output_folder, filename)

        with open(input_path, 'r', encoding='utf-8') as f:
            tokens = f.read().split()

        stemmed = [stemmer.stem(word) for word in tokens]

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(' '.join(stemmed))

        print(f"{filename} berhasil di-stemming.")
