# Load a pretrained 300‑dim English model (≈1 GB)
#import fasttext
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import fasttext as ft
import rdflib



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


def return_top_n_terms(config, keyword_embeddings, term_embeddings, terms, n=5):
    matched_terms = []
    cosines = []

    # find the terms that have a cosine similarity above a certain threshold
    cosine_threshold = config["match_keywords_to_terms"]["cosine_threshold"]


    # find the closest term for each keyword embedding. return them and their cosine similarity scores
    for kw_emb in keyword_embeddings:
        kw_emb = kw_emb.reshape(1, -1)  # reshape to (1, embedding_dim)
        similarities = cosine_similarity(kw_emb, term_embeddings)  # shape (1, num_terms)
        top_indices = np.argsort(-similarities[0])[:n]  # indices of top 5 similar terms
        top_terms = [terms[i] for i in top_indices if similarities[0][i] >= cosine_threshold]
        matched_terms.append((top_terms))
        top_cosines = [similarities[0][i] for i in top_indices if similarities[0][i] >= cosine_threshold]
        cosines.append(top_cosines)



    # Load AATC.ttl and link the matched_terms back to URIs
    aatc_graph = rdflib.Graph()
    aatc_graph.parse("data/aatc.ttl", format="turtle")
    term_to_uri = {}
    for s, p, o in aatc_graph:
        if p.endswith("prefLabel"):
            if o.language == "en":
                term_to_uri[str(o)] = str(s)


    # Link the matched_terms back to the URIs (in format (term, uri))
    matched_terms_with_uris = []
    for term_list in matched_terms:
        term_uri_list = []
        for term in term_list:
            uri = term_to_uri.get(term, "URI not found")
            term_uri_list.append((term, uri))
        matched_terms_with_uris.append(term_uri_list)


    return matched_terms_with_uris, cosines

def return_closest_term(config, keyword_embedding, term_embeddings, terms):
    cosine_threshold = config["match_keywords_to_terms"]["cosine_threshold"]
    keyword_embedding = keyword_embedding.reshape(1, -1)  # reshape to (1, embedding_dim)
    similarities = cosine_similarity(keyword_embedding, term_embeddings)  # shape (1, num_terms)
    most_similar_idx = np.argmax(similarities)
    if similarities[0][most_similar_idx] >= cosine_threshold:
        matched_term = terms[most_similar_idx]
        cosine_score = similarities[0][most_similar_idx]
    
    


### LLM related functions
