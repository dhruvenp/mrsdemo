
import pandas as pd
import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Read data and preprocess it
df = pd.read_csv("D:\\music\\sv..csv")
df = df.sample(n=500).drop('link', axis=1).reset_index(drop=True)
df['text'] = df['text'].str.lower().replace(r'[^\w\s]', '').replace(r'\n', '', regex=True)

# Check if df is empty after preprocessing
if df.empty:
    print("DataFrame is empty after preprocessing.")
    exit()

# Tokenization and stemming
nltk.download('punkt')
ps = PorterStemmer()
def tokenization(txt):
    tokens = nltk.word_tokenize(txt)
    stemming = (ps.stem(w) for w in tokens)
    return " ".join(stemming)

df['text'] = df['text'].apply(lambda x: tokenization(x))

# TF-IDF Vectorization
tfid = TfidfVectorizer(stop_words="english")
matrix = tfid.fit_transform(df['text'])

# Compute cosine similarity
similarity = cosine_similarity(matrix)

def recommendation(song):
    pass

# Example usage
a = recommendation('If You Love Me')
print(a)

