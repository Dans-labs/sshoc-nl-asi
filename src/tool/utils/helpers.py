# Load a pretrained 300‑dim English model (≈1 GB)
#import fasttext
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import fasttext as ft



### Embedding related functions

def get_fasttext_vec(word: str):
    return ft.get_word_vector(word)   # returns a NumPy array (300,)

def print_similar_keywords(sim_matrix, keywords):
    """ 
    Print the words that are most similar to each other
    input: similarity matrix and list of keywords
    """
    num_keywords = len(keywords)
    for i in range(num_keywords):
        similarities = sim_matrix[i]
        # Get indices of keywords sorted by similarity (excluding self)
        sorted_indices = np.argsort(-similarities)
        most_similar_idx = sorted_indices[1]  # index of the most similar keyword
        print(f"Keyword '{keywords[i]}' is most similar to '{keywords[most_similar_idx]}' with similarity {similarities[most_similar_idx]:.4f}")


def print_vector_shapes(keywords):
    for keyword in keywords:
        vec = get_fasttext_vec(keyword)
        print(f"Keyword: {keyword} | Vector shape: {vec.shape}")


def calculate_similarity_matrix(keywords):
    vectors = np.stack([get_fasttext_vec(w) for w in keywords])
    sim_matrix = cosine_similarity(vectors)
    print(sim_matrix)
    print()




### LLM related functions
