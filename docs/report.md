# Report on Automated Subject Indexing (ASI) Pilot
Author: Alessandra Polimeno \
Date: February 06 2026 \
[Github repo](https://github.com/Dans-labs/sshoc-nl-asi/tree/main)

## Project background 
This tool was created for SSHOC-NL deliverable 2025-D09, with the goal of automatically suggesting Getty AAT terms as keywords for datasets in the SSH Data Station. The tool outputs a number of controlled vocabulary terms based on the dataset title and description that match the dataset's topic. This task is referred to as Automated Subject Indexing (ASI). 


## Abstract
- short task description 
- reason why semi-automation is important/useful 
- setup overview 
- what's new?
  - Very large vocabulary, cannot be included in the prompt 
  - relatively lightweight 



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
Golub (2021) provides an overview of approaches to ASI, as well as important developments, examples from operative systems, and best practices. Most of the information in the sections below is based on their work.  


#### Lexical techniques 
Lexical approaches treat the indexing problem as a term-lookup task. After preprocessing the record’s description, the system compares it directly with the terms of the controlled vocabulary.  

A typical preprocessing pipeline follows these steps (Golub, 2021):  
> 1: stop word removal (discards high-frequency function words with low semantic weight); \
> 2: tokenization (splits the text into atomic units / tokens, roughly corresponding to words); \
> 3: stemming or lemmatization (reduces morphological variants to a canonical form, e.g., “depositor” → “deposit”) 

The resulting documents could already be used to match against the controlled vocabulary using similarity measures. The simplest method would be exact string matching, which works well when the vocabulary terms appear verbatim in the target description. Using Edit distance or fuzzy matching can capture typographical errors or small variations. 

When exact/verbatim matches are rare, it can be useful to use TF-IDF weighted cosine similarity. This approach represents both the descriptions and term definitions as sparse vectors with weights that represent their information value. TF-IDF representations take into account how often a token appears in the document at hand, and how often it appears in the other documents of the collection. The weight can be seen as an indication of how well the corresponding token contributes to the overall topic of the document. Similarity measures like cosine similarity can compare the vectors and retrieve the terms that are most similar to the description.  


#### Statistical techniques
Statistical (or classical machine-learning) approaches treat the task as a multi-label classification problem in which each document may be assigned any of the controlled vocabulary terms. The most common approach to ASI is the application of supervised machine learning algorithms (Golub, 2021). Such algorithms learn to extract patterns from large amounts of labeled data that can be generalized to a new set of unseen data. In the case of ASI, the training data would consist of datasets that have already been manually indexed. The algorithm would learn to make associations between the terms and dataset characteristics (e.g., frequently occurring words), which can be used to predict the most likely term of an new dataset. 

Supervised machine learning only works when large amounts of labeled training data are present, because the algorithm needs enough evidence to distinguish between each possible label. The minimal number of annotations per class that is required for reliable prediction by supervised machine learning depends on the task and algorithm. Golub (2021) found that supervised classification for ASI only worked well with classes that have over 1000 training documents. This challenge is not easily overcome by libraries or repositories, as controlled vocabularies can be large, and the manually indexed datasets may not cover all of them. The Getty AAT, for instance, has over 500.000 terms, so a repository must house roughly 500 million datasets to yield sufficient training data (while also making the unlikely assumption that each term is equally distributed over the datasets). In short, supervised machine learning approaches to ASI are better suited for smaller controlled vocabularies for which sufficient training data can be more easily obtained. 




#### Large Language Models (LMMs)
LLMs are statistical models that have evolved from classic machine learning, and are trained on vast amounts of language data. While in essence LLMs are trained to predict the next word in a sequence, they can successfully be applied to carry out most natural language processing tasks. It is possible to interact with an LLM using natural language, so designing your prompt in which you describe the task is essential.  

The main advantage of using LLMs with zero or few shot learning is the lack of need for extensive training data. The main downsides are that the output is nondeterministic; it may give varying answers when given the same prompt multiple times. Moreover, LLMs tend to hallucinate and make up terms that are not in the vocabularies, even when explicitly instructed to only stick to the vocabulary terms. Relatedly, in a small explorative experiment, we found that the LLMs we used consistently failed at linking the generated terms to their URIs. Even if a valid Getty AAT term was generated, the corresponding URI would not be valid and link either to a different term, or no term at all. Zhang et al., (2023) found that transfer learning works well for smaller vocabularies that can be included verbatim in the input prompt. 

Note that in practice, a combination of approaches is often implemented. 


### Embeddings 
We use embedding representations to retrieve the controlled vocabulary terms that match with the generated keywords. This section provides some background on how embeddings work.  

Embeddings are machine-readable vector representations of texts that encode semantic information. Embeddings are based on the distributional hypothesis, which states that words that occur in similar contexts tend to have similar meanings. The difference in meaning between words can in this way be captured by measuring the difference in their environment. Similarly, the different senses of polysemous words (words with the same form but different meanings), can be distinguished by contextualized embeddings. 

Based on the assumption that the meaning of words can be derived
from their neighboring words, word embeddings represent words as vectors that map them to a point in a multidimensional semantic space, where numbers in the vector represent coordinates in the vector space. The values of the vectors are commonly learned by neural networks trained on large amounts of text that obtain the representation based on the frequency distributions of words and its neighbors. This results in clusters where words in close proximity of each other occur in similar contexts, and are thus semantically similar. Reversely, a large distance between two words indicates a high dissimilarity. 

A common way to illustrate the semantic power of embeddings is using arithmetic operations on vectors to finish analogies. Analogies are statements that take the form of “a is to b as x is to y”. In the analogy “France is to Paris as Italy is to x ”, x can be calculated by subtracting the vectors of France and Italy, and adding the vector of Paris. This will result in the vector of Rome. Embedding models are not trained on this property, they are inherent to the way word vectors are designed. 

## System setup

### Overview
Our tool takes a dataset DOI as input and extracts some metadata (currently the title and description). It proceeds to create term suggestions with the following two main components: 

> 1. Summarization of the dataset content in keywords by an LLM. 
> 2. Linking of the generated keywords to Getty AAT terms with embeddings and cosine similarity. 

When looking at the steps that are typically involved in subject indexing as outlined in the [Task Description section](#task-description) above, the LLM in our system performs the first two steps (determining and formulating the subject matter of the document), and the second component carries out the last step (translating the subject matter into the indexing language). 

The indexing language in our case is a slim version of the [Getty Art and Architecture Thesaurus](https://www.getty.edu/research/tools/vocabularies/aat/) (AAT). This vocabulary is already in use in the DANS Data Stations. See below on more information about the Getty version that we use.  


>TO DO: VISUALIZATION OF SYSTEM 

### LLM 
We found earlier that instructing an LLM to directly match dataset metadata with Getty AAT terms and the corresponding URI was not effective. Many generated terms and all URIs were hallucinated. However, the keywords that were generated to summarize the dataset looked fitting. 

The model we used for the first iteration of experiments was [gpt-oss-120b](https://huggingface.co/openai/gpt-oss-120b) which was accessed with the Huggingface API. If this tool gets integrated into the DANS Data Stations, it should work with a local LLM hosted on DANS servers, or an LLM that is developed by a trusted institute such as [SURF](https://www.surf.nl/en).  

We formulated the input prompt as follows: 

> **Instruction**: Select up to 10 terms from the Getty AAT (https://vocab.getty.edu/aat/) that summarize the contents of the dataset description below. Only choose terms that are present in the AAT. \
**Format**: Please format your output as follows: 'name_term_1, name_term_2, name_term_3, name_term_4, name_term_5' \
**Dataset description**: {metadata}

Our aim was to minimize the number of input tokens necessary to inform the LLM on the task and generate the keywords, which is why we chose to not include examples in the prompt. Note that the explicit instruction to only use vocabulary terms was not always followed. 

We currently have not specified the desired language of the terms in the prompt, but when testing and evaluating we found that the generated keywords were always in English, probably due to the prompt being in English but despite the metadata being predominantly Dutch. For robustness we could include a language specification in the prompt. 


### Embeddings 
While LLMs appeared suitable for summarizing the subject of a dataset, the method consistently failed at producing the corresponding vocabulary term and its URI. We solved this problem by representing both the controlled vocabulary terms and the generated keywords as embeddings, and retrieving the vocabulary term with the highest similarity to each generated keyword. The similarity between two embedding representations can easily be determined with the cosine similarity measure. 

Cosine similarity measures how closely two embedding vectors point in the same direction: it computes the cosine of the angle between them, giving a value from –1 (opposite) to 1 (identical). In practice, words with similar meanings end up with vectors that form a small angle, so their cosine similarity is close to 1, indicating they’re semantically related. 

By retrieving the embedding representation of the AAT term that is most similar to the embedding representation of a generated keyword, we created a list of suggestions. We only selected term-keyword pairs with a cosine higher than 0.7. A setting is implemented that allows you to choose for either only the single most similar term for each keyword, or the top n most similar keywords. 

The embeddings model that the tool currently uses is [Sentence-BERT](https://www.sbert.net/) (SBERT), specifically `all-MiniLM-L6-v2` via [Huggingface](https://huggingface.co/sentence-transformers/multi-qa-MiniLM-L6-cos-v1). 


### The AAT Concepts
We use a slim version of the Getty Art and Architecture Thesausus that was created to address size issues and easier use in the DANS Data Stations. This version is called the [Art and Architecture Thesaurus Concepts](https://zenodo.org/records/15487726) (AATC) and is a trimmed-down version of the original thesaurus, focused only on concepts (rather than hierarchy names), containing a simplified schema for language labels, only in English and Dutch, and relinquish the hierarchy in favor of a flat list of concepts. It is a SKOS concept scheme that can be browsed [here](https://vocabs.datastations.nl/AATC/en/). 

The AAT Concepts contains considerably fewer terms as it only takes the concepts, and Dutch and English labels, resulting in 55741 concepts. The ASI tool represents these concepts as contextualized embeddings with the same model as the generated keywords (namely Sentence-BERT). 


## Evaluation
 The question of how good current automated approaches to subject indexing are is not straightforward to answer. Most of the research on the topic is conducted in laboratory conditions that tend to lack the complexities of reality (Golub, 2021). Moreover, evaluation of an ASI system is difficult because of the subjective nature of the task. A common evaluation method is comparing generated labels against a human-assigned gold standard (Golub, 2021). This evaluation method is imperfect because there often is not one correct answer, especially with larger vocabularies. Humans may have chosen a more specific or broader term than the ASI system, but that does not necessarily mean that the predicted term is incorrect or unsuitable. One of the lines Golub (2021) recommends is involving both subject indexing experts and users in the evaluation process. We did not have the funds for a thorough evaluation and instead opted for the input of four data experts. 

We selected a stratified sample of 60 datasets from the [DANS Data Station Social Sciences and Humanities](https://ssh.datastations.nl/), making sure they had varying title and description lengths. For this sample we generated a file containing the dataset metadata, the keyword generated by the LLM, and the matched AATC term. We asked the data experts to annotate each keyword-term pair with a value indicating if the matching went well of not, and whether the resulting term would be acceptable as subject index or not. They were also asked to indicate whether they found the set of suggested terms to sufficiently describe the dataset, or if they were missing important terms.  


### Guideline summary
Our annotation guidelines included the following information for each of the variables: 
- Linking between keyword and AATC term: 
  - Indicate whether the linking between the generated keyword and AATC term was done correctly. Does the AATC term refer to roughly the same concept as the generated keyword?  
- Relevance: 
  - Does the AATC term do a good job at describing the content of the dataset? Would you, as a data curator, choose this term to describe the dataset? 
- Overall: 
  - Does the set of AATC terms sufficiently describe the dataset as a whole? Is there a term you are missing? Are the terms too generic to capture the subject?  
 

Tables 1-3 display the results of the evaluation. Keep in mind that large differences between assessments by different people are normal for the task given its subjective nature (Golub, 2021). The total number of annotated pairs may vary slightly between annotators as they sometimes indicated a third ambiguous option that is not included in the table due to inconsistencies.  



|  | correct | incorrect | 
| --- | --- | --- | 
**coder 1** | 214 (75%) | 73 (25%) | 
**coder 2** | 270 (94%)  |  16 (6%) | 
**coder 3** | 245 (86%)|  38 (14%)        |

*Table 1: Evaluation results for the linking between generated keywords and AATC terms.*


|  | acceptable | unacceptable | 
| --- | --- | --- | 
**coder 1** | 254 (89%) | 33 (11%) | 
**coder 2** |  269 (95%)| 14(5%) | 
**coder 3**| 222 (80%) | 56 (20%) | 

*Table 2: Evaluation results for the relevance of the suggested AATC terms.*


|  | OK | missing | too generic | 
| --- | --- | --- | --- |
**coder 1** | 30 | 22 | 7 | 
**coder 2** | 27  | 28  | 5  | 
**coder 3** |  22 | -  | -  | 

*Table 3: Evaluation results for the overall quality of the suggested AATC terms on dataset level.*


### Discussion
(Preliminary for now as more annotations may come in)
- Overall, it can be said that the relevance of the terms generated by the tool is quite high (see Table 2). 
- For many datasets the annotators identified missing terms. 
- Given that the tool should be used to make suggestions to depositors, it is most important that the suggestions are relevant. If the tool were to suggest many irrelevant terms it would be unusable.   



## Integration requirements
What's needed?



## References 
- Golub, K., Soergel, D., Buchanan, G., Tudhope, D., Lykke, M., & Hiom, D. (2016). A framework for evaluating automatic indexing or classification in the context of retrieval. Journal of the association for information science and technology, 67(1), 3-16,  https://doi.org/10.1002/asi.23600
- Golub, K. (2021). Automated subject indexing: An overview. Cataloging & Classification Quarterly, 59(8), 702-719. https://doi.org/10.1080/01639374.2021.2012311
- Koraljka Golub, Johan Hagelbäck, and Anders Ardö, “Automatic Classification of
Swedish Metadata Using Dewey Decimal Classification: A Comparison of Approaches,”
Journal of Data and Information Science 5, no. 1 (2020): 18, https://doi.org/10.2478/jdis-2020-0003
- Mai, J. E. (2001). Semiotics and indexing: an analysis of the subject indexing process. Journal of documentation, 57(5), 591-622, https://doi.org/10.1108/EUM0000000007095
- Zhang, S., Wu, M., & Zhang, X. (2023). Utilising a large language model to annotate subject metadata: A case study in an Australian national research data catalogue. 
