"""
Input: a list of keywords

Output: embeddding representations of the keywords

"""


# Import libraries
import logging




def run(config, keywords):

    logging.info("Converting keywords to embeddings...")

    method = config["embeddings"]["method"]
    

    keywords = [kw.lower() for kw in keywords]

    if method == "fasttext":
        import fasttext
        from utils.helpers import get_fasttext_vec

        model_path = config["embeddings"]["model_path"]
        
        logging.info(f"Using FastText model at: {model_path}")
        # Load FastText model
        #fasttext.util.download_model('en', if_exists='ignore')
        ft = fasttext.load_model(model_path)


        # Get embeddings
        keyword_embeddings = [ft.get_word_vector(kw) for kw in keywords]

        return keyword_embeddings
    
    if method == "SBERT":
        from sentence_transformers import SentenceTransformer
        import numpy as np

        logging.info(f"Using SBERT model: {config['embeddings']['sbert_model']}")
        sbert_model = SentenceTransformer(config['embeddings']['sbert_model'])

        def get_sbert_embedding(text: str) -> np.ndarray:
            if not text or not isinstance(text, str):
                raise ValueError("Input text must be a non-empty string.")
            embedding = sbert_model.encode(text, convert_to_numpy=True, normalize_embeddings=True)
            return embedding  # returns a NumPy array


        # Get embeddings
        keyword_embeddings = [get_sbert_embedding(kw) for kw in keywords]
        
        return keyword_embeddings
        

    else:
        logging.error(f"Something went wrong with method: {method}")
        return None


