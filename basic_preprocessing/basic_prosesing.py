import os
import re
from nltk.tokenize import word_tokenize
import nltk

nltk.download('punkt')

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(BASE_DIR)

input_folder = os.path.join(PROJECT_DIR, "translate", "hasil_translate")
output_folder = os.path.join(BASE_DIR, "hasil_preprocessing")
os.makedirs(output_folder, exist_ok=True)

def clean_text(text):
    text = text.lower()
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    return text

for filename in os.listdir(input_folder):
    if filename.endswith('.txt'):
        input_path = os.path.join(input_folder, filename)
        output_path = os.path.join(output_folder, filename)

        with open(input_path, 'r', encoding='utf-8') as f:
            text = f.read()

        cleaned = clean_text(text)
        tokens = word_tokenize(cleaned)

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(' '.join(tokens))

        print(f"{filename} berhasil di-preprocessing.")
