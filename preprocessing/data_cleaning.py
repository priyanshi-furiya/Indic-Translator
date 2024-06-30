import pandas as pd
import re
import string

def load_data(file_path):
    return pd.read_csv(file_path)

def clean_text(text):
    text = str(text).lower()
    text = re.sub("'", '', text)
    exclude = set(string.punctuation)
    text = ''.join(ch for ch in text if ch not in exclude)
    text = re.sub("[२३०८१५७९४६]", "", text)
    text = text.strip()
    text = re.sub(" +", " ", text)
    return text

def remove_numbers(text):
    return re.sub(r'\d+', '', text)

def clean_data(df):
    df['english'] = df['english'].apply(clean_text)
    df['hindi'] = df['hindi'].apply(clean_text)
    df['english'] = df['english'].apply(remove_numbers)
    df['hindi'] = df['hindi'].apply(remove_numbers)
    df['hindi'] = df['hindi'].apply(lambda x: 'START_ ' + x + ' _END')
    return df

def filter_by_length(df, max_length=20):
    df['length_eng'] = df['english'].apply(lambda x: len(x.split()))
    df['length_hin'] = df['hindi'].apply(lambda x: len(x.split()))
    return df[(df['length_eng'] <= max_length) & (df['length_hin'] <= max_length)]

def clean_and_prepare_data(file_path):
    df = load_data(file_path)
    df = clean_data(df)
    df = filter_by_length(df)
    return df