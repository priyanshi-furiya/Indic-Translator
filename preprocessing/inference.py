import numpy as np

def decode_sequence(input_seq, encoder_model, decoder_model, target_token_index, reverse_target_char_index, max_decoder_seq_length):
    states_value = encoder_model.predict(input_seq)
    target_seq = np.zeros((1, 1))
    target_seq[0, 0] = target_token_index['START_']

    stop_condition = False
    decoded_sentence = ''
    while not stop_condition:
        output_tokens, h, c = decoder_model.predict([target_seq] + states_value)

        sampled_token_index = np.argmax(output_tokens[0, -1, :])
        sampled_char = reverse_target_char_index[sampled_token_index]
        decoded_sentence += ' ' + sampled_char

        if (sampled_char == '_END' or len(decoded_sentence) > max_decoder_seq_length):
            stop_condition = True

        target_seq = np.zeros((1, 1))
        target_seq[0, 0] = sampled_token_index
        states_value = [h, c]

    return decoded_sentence

def translate(input_text, encoder_model, decoder_model, input_token_index, target_token_index, reverse_target_char_index, max_encoder_seq_length, max_decoder_seq_length):
    input_seq = np.zeros((1, max_encoder_seq_length), dtype='float32')
    for i, word in enumerate(input_text.split()):
        if word in input_token_index:
            input_seq[0, i] = input_token_index[word]
        else:
            input_seq[0, i] = input_token_index['UNK']  # Use 'UNK' for unknown words
    decoded_sentence = decode_sequence(input_seq, encoder_model, decoder_model, target_token_index, reverse_target_char_index, max_decoder_seq_length)
    return decoded_sentence[:-4]  # Remove '_END'