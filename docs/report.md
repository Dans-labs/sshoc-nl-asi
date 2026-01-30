# Report on Automated Subject Indexing


## Project background 
This tool was created for SSHOC-NL deliverable 2025-D09, with the goal of automatically suggesting Getty AAT terms as keywords for datasets in the SSH Data Station. The tool outputs a number of controlled vocabulary terms based on the dataset title and description that match the dataset's topic. This task is referred to as Automated Subject Indexing (ASI). 




## Task description 
The task of Automated Subject Indexing (ASI)
> describe task, subjective nature etc


An important aspect of the task of subject indexing is that it is subjective. Finding the term that best describes a dataset or resource isn’t an exact science, and the answer might depend on who you ask or on what your goals are. Do you want a small set of broad terms that cover the topic? Or would a large number of more specific terms work? For humans, the task of subject indexing usually follows these steps (Golub, 2021):  
> 1: determining the subject of the resource; \
2: deciding which aspects of the content should be represented; \
3: translating those aspects to terms from a controlled vocabulary. 

Step 2 in particular introduces the subjective nature into the task. This should be kept in mind when thinking about how to perform it computationally, as there is not one correct label that should be aimed at. It also complicates the evaluation process of the generated output.  


### Approaches
#### Statistical techniques
Statistical (or classical machine-learning) approaches treat the task as a multi-label classification problem in which each document may be assigned any of the controlled vocabulary terms. The most common approach to ASI is the application of supervised machine learning algorithms (Golub, 2021). Such algorithms learn to extract patterns from large amounts of labeled data that can be generalized to a new set of unseen data. In the case of ASI, the training data would consist of datasets that have already been manually indexed. The algorithm would learn to make associations between the terms and dataset characteristics (e.g., frequently occurring words), which can be used to predict the most likely term of an new dataset. 

Supervised machine learning only works when large amounts of labeled training data are present, because the algorithm needs enough evidence to distinguish between each possible label. The minimal number of annotations per class that is required for reliable prediction by supervised machine learning depends on the task and algorithm. Golub et al. (2020) found that supervised classification for ASI only worked well with classes that have over 1000 training documents. This challenge is not easily overcome by libraries or repositories, as controlled vocabularies can be large, and the manually indexed datasets may not cover all of them. The Getty AAT, for instance, has over 500.000 terms, so a repository must house roughly 500 million datasets to yield sufficient training data (while also making the unlikely assumption that each term is equally distributed over the datasets). In short, supervised machine learning approaches to ASI are better suited for smaller controlled vocabularies for which sufficient training data can be more easily obtained. 

#### Lexical techniques 


#### Transfer learning
Transfer learning refers to Large Language Models' (LLM) ability to perform tasks without having received training data for that specific task. LLMs are statistical models that have evolved from classic machine learning, and are trained on vast amounts of language data. While in essence LLMs are trained to predict the next word in a sequence, they can successfully be applied to carry out most natural language processing tasks.  

In the context of ASI, LLMs have been used to predict 







## Method
The tool consists of two main components: 
- Summarization of the dataset content in keywords by an LLM. 
- Linking of the generated keywords to Getty AAT terms with embeddings and cosine similarity. 




## Current status 


## References 
- [Golub, K. (2021). Automated subject indexing: An overview. Cataloging & Classification Quarterly, 59(8), 702-719.](https://doi.org/10.1080/01639374.2021.2012311)
- Koraljka Golub, Johan Hagelbäck, and Anders Ardö, “Automatic Classification of
Swedish Metadata Using Dewey Decimal Classification: A Comparison of Approaches,”
Journal of Data and Information Science 5, no. 1 (2020): 18, https://doi.org/10.2478/jdis-2020-0003
- Zhang, S., Wu, M., & Zhang, X. (2023). Utilising a large language model to annotate subject metadata: A case study in an Australian national research data catalogue. 
- 