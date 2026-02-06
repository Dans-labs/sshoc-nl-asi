# Report on Automated Subject Indexing (ASI)
Author: Alessandra Polimeno \
Date: February 06 2026

## Project background 
This tool was created for SSHOC-NL deliverable 2025-D09, with the goal of automatically suggesting Getty AAT terms as keywords for datasets in the SSH Data Station. The tool outputs a number of controlled vocabulary terms based on the dataset title and description that match the dataset's topic. This task is referred to as Automated Subject Indexing (ASI). 


## Abstract
- short task description 
- reason why semi-automation is important/useful 
- setup overview 
- what's new? 


## Task description 
The task of subject indexing aims to facilitate findability of digital resources by providing keywords that describe the subject of the resource. The keywords are terms from a controlled vocabulary or thesaurus. With the help of the keywords, a user can retrieve relevant documents for the topic they are researching. What makes this task complex is the fact that relevance is subjective, and differs between people or can change over time for the same person. The perspective from which a user wants to retrieve a document cannot be fully predicted, and subject indeces are incomplete by default (Golub, 2016). 

The process of subject indexing itself is subjective in nature, too. The terms an indexer comes up with do not form a neutral and objective representation of what a resource is about, but rather the representation of an interpretation of the resource made by the indexer. The result is influenced by both the social and cultural context of the indexer (Mai, 2001). The subjective nature of the task should be kept in mind when thinking about how to perform it computationally, as there is no finite set of correct labels for a given document that should be aimed at. Moreover, it complicates the evaluation process because no gold standard can be assumed, and evaluation should combine quantitative and qualitative methods (Golub, 2016). 


For subject indexing by humans, the task is commonly characterized as three steps (Mai, 2001): 
> 1: determine the subject matter of the document; \
> 2: reformulate the subject matter in a natural language statement; \
> 3: translate the subject matter into the indexing language. 

Each step involves a reinterpretation of the result of the previous step. 

Manually adding subject terms to documents is time-consuming, especially for larger libraries or repositories. Automated Subject Indexing (ASI) addresses the problem of scale by (semi-)automatically enriching documents with subject terms. Tools for ASI are scarcely ever used to completely automatically add keywords to resources, mainly due to the subjectivity involved. Moreover, it has been difficult to find hard evidence of the success of fully automatic tools, as research and evaluation is often conducted in laboratory settings that do not consider the complexities of real-life systems (Golub, 2016). More commonly,  ASI tools provide suggestions that are then selected or rejected by human curators.  



## Background

### Approaches
#### Statistical techniques
Statistical (or classical machine-learning) approaches treat the task as a multi-label classification problem in which each document may be assigned any of the controlled vocabulary terms. The most common approach to ASI is the application of supervised machine learning algorithms (Golub, 2021). Such algorithms learn to extract patterns from large amounts of labeled data that can be generalized to a new set of unseen data. In the case of ASI, the training data would consist of datasets that have already been manually indexed. The algorithm would learn to make associations between the terms and dataset characteristics (e.g., frequently occurring words), which can be used to predict the most likely term of an new dataset. 

Supervised machine learning only works when large amounts of labeled training data are present, because the algorithm needs enough evidence to distinguish between each possible label. The minimal number of annotations per class that is required for reliable prediction by supervised machine learning depends on the task and algorithm. Golub et al. (2020) found that supervised classification for ASI only worked well with classes that have over 1000 training documents. This challenge is not easily overcome by libraries or repositories, as controlled vocabularies can be large, and the manually indexed datasets may not cover all of them. The Getty AAT, for instance, has over 500.000 terms, so a repository must house roughly 500 million datasets to yield sufficient training data (while also making the unlikely assumption that each term is equally distributed over the datasets). In short, supervised machine learning approaches to ASI are better suited for smaller controlled vocabularies for which sufficient training data can be more easily obtained. 

#### Lexical techniques 
Lexical approaches treat the indexing problem as a term-lookup task. After preprocessing the record’s description, the system compares it directly with the terms of the controlled vocabulary.  

A typical preprocessing pipeline follows these steps (Golub, 2021):  
> 1: stop word removal (discards high-frequency function words with low semantic weight); \
> 2: tokenization (splits the text into atomic units / tokens, roughly corresponding to words); \
> 3: stemming or lemmatization (reduces morphological variants to a canonical form, e.g., “depositor” → “deposit”) 

The resulting documents could already be used to match against the controlled vocabulary using similarity measures. The simplest method would be exact string matching, which works well when the vocabulary terms appear verbatim in the target description. Using Edit distance or fuzzy matching can capture typographical errors or small variations. 

When exact/verbatim matches are rare, it can be useful to use TF-IDF weighted cosine similarity. This approach represents both the descriptions and term definitions as sparse vectors with weights that represent their information value. TF-IDF representations take into account how often a token appears in the document at hand, and how often it appears in the other documents of the collection. The weight can be seen as an indication of how well the corresponding token contributes to the overall topic of the document. Similarity measures like cosine similarity can compare the vectors and retrieve the terms that are most similar to the description.  


#### Large Language Models (LMMs)
LLMs are statistical models that have evolved from classic machine learning, and are trained on vast amounts of language data. While in essence LLMs are trained to predict the next word in a sequence, they can successfully be applied to carry out most natural language processing tasks. It is possible to interact with an LLM using natural language, so designing your prompt in which you describe the task is essential.  

The main advantage of using LLMs with zero or few shot learning is the lack of need for extensive training data. The main downsides are that the output is nondeterministic; it may give varying answers when given the same prompt multiple times. Moreover, LLMs tend to hallucinate and make up terms that are not in the vocabularies, even when explicitly instructed to only stick to the vocabulary terms. Relatedly, in a small explorative experiment, we found that the LLMs we used consistently failed at linking the generated terms to their URIs. Even if a valid Getty AAT term was generated, the corresponding URI would not be valid and link either to a different term, or no term at all. Zhang et al., 2023 found that transfer learning works well for smaller vocabularies that can be included verbatim in the input prompt. 


### Mixed methods 
- In practice, a mix of approaches is often implemented. 


## System setup

The tool consists of two main components: 
- Summarization of the dataset content in keywords by an LLM. 
- Linking of the generated keywords to Getty AAT terms with embeddings and cosine similarity. 

### LLM 
We found before that instructing an LLM to directly match dataset metadata with Getty AAT terms and the corresponding URI was not effective. Many generated terms and all URIs were hallucinated. However, 


### Embeddings 
Embeddings are machine-readable vector representations of text that encode semantic information. Representing both the controlled vocabulary terms and the generated keywords as embeddings allows for the use of cosine similarity to match the keywords with their closest neighbor in the controlled vocabulary.

### Cosine similarity 
> add formula, short explanation of how it works 

### The Getty AAT 

## Evaluation

## Current status 

## Integration 
What's needed?


## References 
- Golub, K., Soergel, D., Buchanan, G., Tudhope, D., Lykke, M., & Hiom, D. (2016). A framework for evaluating automatic indexing or classification in the context of retrieval. Journal of the association for information science and technology, 67(1), 3-16,  https://doi.org/10.1002/asi.23600
- Golub, K. (2021). Automated subject indexing: An overview. Cataloging & Classification Quarterly, 59(8), 702-719. https://doi.org/10.1080/01639374.2021.2012311
- Koraljka Golub, Johan Hagelbäck, and Anders Ardö, “Automatic Classification of
Swedish Metadata Using Dewey Decimal Classification: A Comparison of Approaches,”
Journal of Data and Information Science 5, no. 1 (2020): 18, https://doi.org/10.2478/jdis-2020-0003
- Mai, J. E. (2001). Semiotics and indexing: an analysis of the subject indexing process. Journal of documentation, 57(5), 591-622, https://doi.org/10.1108/EUM0000000007095
- Zhang, S., Wu, M., & Zhang, X. (2023). Utilising a large language model to annotate subject metadata: A case study in an Australian national research data catalogue. 
