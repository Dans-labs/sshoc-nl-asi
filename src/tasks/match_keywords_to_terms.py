"""
This script matches the embeddings of generated keywords to the closest controlled vocabulary terms using cosine similarity.

Input: list of keyword embeddings and lookup dictionary with controlled vocabulary terms as embeddings
Output: matched terms for each keyword based on highest similarity as a txt file

"""

import logging 
import pickle
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import rdflib
from utils.helpers import return_top_n_terms




def run(config, keyword_embeddings):

    logging.info("Loading lookup dictionary...")
    lookup_dict_path = config["embeddings"]["lookup_dict_path"]
    lookup_dict = pickle.load(open(lookup_dict_path, "rb"))  # {term: embedding}

    terms = list(lookup_dict.keys())
    term_embeddings = np.stack(list(lookup_dict.values()))  # shape (num_terms, embedding_dim)

    #matched_terms = []
    #cosines = []

    #logging.info("Matching keywords to controlled vocabulary terms...")

    # find the terms that have a cosine similarity above a certain threshold
    #cosine_threshold = config["match_keywords_to_terms"]["cosine_threshold"]

    matched_terms_with_uris, cosines = return_top_n_terms(config, keyword_embeddings, term_embeddings, terms, n=5)


    # # find the closest term for each keyword embedding. return them and their cosine similarity scores
    # for kw_emb in keyword_embeddings:
    #     kw_emb = kw_emb.reshape(1, -1)  # reshape to (1, embedding_dim)
    #     similarities = cosine_similarity(kw_emb, term_embeddings)  # shape (1, num_terms)
    #     top_indices = np.argsort(-similarities[0])[:5]  # indices of top 5 similar terms
    #     top_terms = [terms[i] for i in top_indices if similarities[0][i] >= cosine_threshold]
    #     matched_terms.append((top_terms))
    #     top_cosines = [similarities[0][i] for i in top_indices if similarities[0][i] >= cosine_threshold]
    #     cosines.append(top_cosines)



    # # Load AATC.ttl and link the matched_terms back to URIs
    # aatc_graph = rdflib.Graph()
    # aatc_graph.parse("data/aatc.ttl", format="turtle")
    # term_to_uri = {}
    # for s, p, o in aatc_graph:
    #     if p.endswith("prefLabel"):
    #         if o.language == "en":
    #             term_to_uri[str(o)] = str(s)


    # # Link the matched_terms back to the URIs (in format (term, uri))
    # matched_terms_with_uris = []
    # for term_list in matched_terms:
    #     term_uri_list = []
    #     for term in term_list:
    #         uri = term_to_uri.get(term, "URI not found")
    #         term_uri_list.append((term, uri))
    #     matched_terms_with_uris.append(term_uri_list)


    return matched_terms_with_uris, cosines

