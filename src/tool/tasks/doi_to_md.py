
"""
This script takes the DOI of a dataset and collects its metadata

Input: dataset DOI
Output: metadata string with title and description

"""

import requests
import logging


def run(config): 

    logging.info("Fetching metadata from DOI...")

    doi = config['doi_to_md']['doi']
    base_url = config["doi_to_md"]["base_url"]

    # Format DOI for URL
    doi_encoded = doi.replace(":", "%3A")
    metadata_url = f"{base_url}{doi_encoded}"
    logging.debug(f"Metadata URL: {metadata_url}")

    # Get metadata from API
    try:  
        response = requests.get(metadata_url)
        response.raise_for_status()
        metadata = response.json()

    except Exception as e:
        logging.error(f"Error fetching metadata for DOI: {e}")
        return None

    # Extract basic metadata
    try:
        title = metadata["ore:describes"]["title"]
        if isinstance(metadata["ore:describes"]["citation:dsDescription"], list):
            description = " ".join([desc["citation:dsDescriptionValue"] for desc in metadata["ore:describes"]["citation:dsDescription"]])
        else:
            description = metadata["ore:describes"]["citation:dsDescription"]["citation:dsDescriptionValue"]
    except KeyError as e:
        logging.error(f"Missing expected metadata fields: {e}")
        return None

    # Extract keywords
    def extract_keywords(metadata):

        try: 
            keywords = metadata["ore:describes"]["citation:keyword"]
            # extract all keywords as a string, seperated by commas
            if isinstance(keywords, list):
                keywords = [kw["citation:keywordValue"] for kw in keywords]
            else:
                keywords = [keywords["citation:keywordValue"]]
            return ", ".join(keywords)

        except KeyError:
            logging.info("No keywords found in metadata.")
            return None

   # keywords = extract_keywords(metadata)
    keywords = None

    # Combine all parts 
    if keywords:    
        metadata_output = f"{title}; {description}; Keywords: {keywords}"
    else:
        metadata_output = f"{title}; {description}"

    logging.info("Metadata fetched successfully.")
    return metadata_output


