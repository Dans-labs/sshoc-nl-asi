
import pandas as pd

def run(config, keywords, matched_terms, cosines, metadata_length): 
    
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

    # Print formatted output
    # for i, term_list in enumerate(matched_terms):
    #     print(f"Keyword: {keywords[i]}")
    #     for term, uri in term_list:
    #         print(f"  Matched Term: {term} | URI: {uri}")
    #     print("\n")

    # Create a DataFrame to hold the formatted output
    data = []
    for i, keyword in enumerate(keywords):
        for (term, uri), cosine in zip(matched_terms[i], cosines[i]):
            data.append({
                "DOI": doi,
                "Keyword": keyword,
                "Matched Term": term,
                "URI": uri,
                "Cosine Similarity": cosine, 
                "Num chars in metadata" : metadata_length
            })

    # Create a DataFrame from the collected data
    df = pd.DataFrame(data)

    # Save the DataFrame to a CSV file
    base_path = config["format_output"]["base_path"]
    output_path = base_path.replace("{doi}", doi.replace("/", "_"))
    output_path = output_path.replace("{method}", method)
    output_path = output_path.replace("{cosine}", str(cosine_threshold))

    df.to_csv(output_path, index=False)

    return {"status": "success", "output_file": output_path}
