import pandas as pd

# Read the CSV file into a DataFrame
evaluation_dataset = pd.read_csv('evaluation_dataset.csv')

# Take DOIS 
dois = evaluation_dataset['doi'].tolist()

# Input into pipeline 
