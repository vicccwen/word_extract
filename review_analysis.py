import nltk
import pandas as pd
from nltk.tokenize import word_tokenize
import string

# Ensure you have the necessary NLTK data
nltk.download('punkt', quiet=True)

# Read the Excel file
df = pd.read_excel('internal-medicine-provider-profile-41.xlsx')
print(df.head())

# # Define list of trust-related keywords
trust_keywords = ['trust', 'confident', 'reliable', 'faith', 'belief', 'believe']

# # #Define list of non medical-related keywords
# nonmed_keywords = ['friendly', 'quick', 'communicate', 'outstanding', 'exceptional','gentle','empathetic','compassionate', 'wait time','cruel', 'lazy','bad','rude']


# Preprocessing function
def preprocess(text):
    if isinstance(text, str):  # Check if the input is a string
        text = text.lower()
        text = text.translate(str.maketrans('', '', string.punctuation))
        tokens = word_tokenize(text)
        return tokens
    else:
        return []
    
# Apply preprocessing to create a tokens list
df['tokens'] = df['Review Text'].apply(preprocess)

# Extract trust-related function
def extract_trust_related(text_tokens, existing_content):
    extracted_words = ' '.join([word for word in text_tokens if word in trust_keywords])
    # Check if existing_content is NaN (float type in Pandas)
    if pd.isna(existing_content):
        return extracted_words
    else:
        return existing_content + ' ' + extracted_words if extracted_words else existing_content


# # Extract non-medical-related function
# def extract_nonmed(text_tokens, existing_content):
#     extracted_words = ' '.join([word for word in text_tokens if word in nonmed_keywords])
#     # Check if existing_content is NaN (float type in Pandas)
#     if pd.isna(existing_content):
#         return extracted_words
#     else:
#         return existing_content + ' ' + extracted_words if extracted_words else existing_content


# Apply the extract_trust_related function
df['Text related to trust'] = df.apply(lambda row: extract_trust_related(row['tokens'], row['Text related to trust']), axis=1)

# # Apply the nonmed function
# df['Any text not related to medical care'] = df.apply(lambda row: extract_nonmed(row['tokens'], row['Any text not related to medical care']), axis=1)

# Save the updated DataFrame to an Excel file
df.to_csv('updated_reviews.csv', index=False)