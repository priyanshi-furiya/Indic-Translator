from data_cleaning import clean_and_prepare_data
from preprocessing import preprocess_data, generate_batch
from model import create_model, train_model
from inference import translate
import numpy as np

def main():
    # Data cleaning and preparation
    df = clean_and_prepare_data('asmm_engg.csv')

    # Preprocessing
    (X_train, X_test, y_train, y_test, 
     input_token_index, target_token_index, 
     reverse_input_char_index, reverse_target_char_index,
     num_encoder_tokens, num_decoder_tokens,
     max_length_src, max_length_tar) = preprocess_data(df)

    # Model creation
    latent_dim = 300
    model, encoder_model, decoder_model = create_model(num_encoder_tokens, num_decoder_tokens, latent_dim)

    # Training
    batch_size = 64
    epochs = 25
    train_generator = generate_batch(X_train, y_train, batch_size, max_length_src, max_length_tar, num_decoder_tokens, input_token_index, target_token_index)
    val_generator = generate_batch(X_test, y_test, batch_size, max_length_src, max_length_tar, num_decoder_tokens, input_token_index, target_token_index)
    steps_per_epoch = len(X_train) // batch_size
    validation_steps = len(X_test) // batch_size

    model = train_model(model, train_generator, val_generator, steps_per_epoch, validation_steps, epochs)

    # Save the model
    model.save('eng-to-hindi.h5')

    # Test the model
    test_sentences = [
        "kitchen",
        "how are you",
        "what is your name"
    ]

    for sentence in test_sentences:
        translated = translate(sentence, encoder_model, decoder_model, input_token_index, target_token_index, reverse_target_char_index, max_length_src, max_length_tar)
        print(f"Input: {sentence}")
        print(f"Translated: {translated}\n")

if __name__ == "__main__":
    main()