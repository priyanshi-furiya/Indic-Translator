import numpy as np
from sklearn.model_selection import train_test_split

def create_tokenizer(words):
    word_to_index = {word: i+1 for i, word in enumerate(sorted(list(words)))}
    index_to_word = {i+1: word for i, word in enumerate(sorted(list(words)))}
    return word_to_index, index_to_word

def preprocess_data(df):
    all_eng_words = set()
    all_hindi_words = set()

    for eng in df['english']:
        all_eng_words.update(eng.split())
    for hin in df['hindi']:
        all_hindi_words.update(hin.split())

    input_token_index, reverse_input_char_index = create_tokenizer(all_eng_words)
    target_token_index, reverse_target_char_index = create_tokenizer(all_hindi_words)

    num_encoder_tokens = len(all_eng_words)
    num_decoder_tokens = len(all_hindi_words) + 1

    max_length_src = df['length_eng'].max()
    max_length_tar = df['length_hin'].max()

    X, y = df['english'], df['hindi']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    return (X_train, X_test, y_train, y_test, 
            input_token_index, target_token_index, 
            reverse_input_char_index, reverse_target_char_index,
            num_encoder_tokens, num_decoder_tokens,
            max_length_src, max_length_tar)

def generate_batch(X, y, batch_size, max_length_src, max_length_tar, num_decoder_tokens, input_token_index, target_token_index):
    while True:
        for j in range(0, len(X), batch_size):
            encoder_input_data = np.zeros((batch_size, max_length_src), dtype='float32')
            decoder_input_data = np.zeros((batch_size, max_length_tar), dtype='float32')
            decoder_target_data = np.zeros((batch_size, max_length_tar, num_decoder_tokens), dtype='float32')
            for i, (input_text, target_text) in enumerate(zip(X[j:j+batch_size], y[j:j+batch_size])):
                for t, word in enumerate(input_text.split()):
                    encoder_input_data[i, t] = input_token_index[word]
                for t, word in enumerate(target_text.split()):
                    if t < len(target_text.split()) - 1:
                        decoder_input_data[i, t] = target_token_index[word]
                    if t > 0:
                        decoder_target_data[i, t - 1, target_token_index[word]] = 1.
            yield([encoder_input_data, decoder_input_data], decoder_target_data)