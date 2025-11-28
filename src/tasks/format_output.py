
import pandas as pd

def run(config, keywords, matched_terms, cosines, metadata_length, metadata_output): 
    
    """
    Format the output of the pipeline into a csv with the columns [DOI, Keyword, Matched Term, URI, Cosine Similarity]
    
    
    Input: 
    - doi: the DOI of the publication
    - keywords: list of generated keywords
    - matched_terms: list of matched controlled vocabulary terms with URIs

    Output:
    - formatted_output: a dictionary containing the DOI, keywords, and matched terms with URIs
    """

    doi = config["doi_to_md"]["doi"]
    method = config["embeddings"]["method"]
    cosine_threshold = config["match_keywords_to_terms"]["cosine_threshold"]
    matching_method = config["match_keywords_to_terms"]["matching_method"]


    aggregated_data = []


    # print("keywords:", keywords, len(keywords))
    # print("matched_terms:", matched_terms, len(matched_terms))
    # print("cosines:", cosines, len(cosines))

    if matching_method == "closest":
        for keyword, matches, cosine in zip(keywords, matched_terms, cosines):
            if cosine >= cosine_threshold:
                # each `matches` is a list with exactly one (term, uri) tuple
                term, uri = matches[0]

                aggregated_data.append({
                    "DOI": doi,
                    "Metadata": metadata_output,
                    "Keyword": keyword,
                    "Matched Term": term,
                    "URI": uri,
                    "Cosine Similarity": float(cosine),   
                })


    if matching_method == "top_n":        
        for i, keyword in enumerate(keywords):
            for (term, uri), cosine in zip(matched_terms[i], cosines[i]):
                if cosine >= cosine_threshold:
                    aggregated_data.append({
                        "DOI": doi,
                        "Metadata": metadata_output,
                        "Keyword": keyword,
                        "Matched Term": term,
                        "URI": uri,
                        "Cosine Similarity": float(cosine), 
                    })




    # Create a DataFrame from the collected data
    df = pd.DataFrame(aggregated_data)

    # Save the DataFrame to a CSV file
    base_path = config["format_output"]["base_path"]
    output_path = base_path.replace("{doi}", doi.replace("/", "_"))
    output_path = output_path.replace("{method}", method)
    output_path = output_path.replace("{cosine}", str(cosine_threshold))

    df.to_csv(output_path, index=False)

    return {"status": "success", "output_file": output_path}
