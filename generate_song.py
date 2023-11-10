import numpy as np
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from train_model import build_and_train_model
from fetch_lyrics import read_api_keys_from_file, initialize_spotipy_client, fetch_and_store_lyrics

def clear_lyrics_file(filename='lyrics.txt'):
    """Clear the contents of the lyrics file."""
    with open(filename, 'w', encoding='utf-8') as _:
        pass

def sample_with_temperature(probs, temperature=2.0):  # Default temperature set to 2.0
    """Sample an index from a probability array based on temperature."""
    probs = np.asarray(probs).astype('float64')
    probs = np.log(probs) / temperature
    exp_probs = np.exp(probs)
    probs = exp_probs / np.sum(exp_probs)
    return np.random.choice(len(probs), p=probs)

def generate_lyrics(model, tokenizer, starting_phrase, word_count, temperature=2.0):  # Default temperature set to 2.0
    max_input_length = model.input_shape[1]
    generated_lyrics = starting_phrase
    
    current_input = starting_phrase

    for _ in range(word_count):
        tokenized_text = tokenizer.texts_to_sequences([current_input])[0]
        tokenized_text = pad_sequences([tokenized_text], maxlen=max_input_length, padding='pre')
        
        probs = model.predict(tokenized_text)[0]
        predicted_index = sample_with_temperature(probs, temperature)
        
        next_word = ""
        for word, index in tokenizer.word_index.items():
            if index == predicted_index:
                next_word = word
                break
        
        generated_lyrics += " " + next_word
        current_input += " " + next_word
        
        if len(current_input.split()) > max_input_length:
            current_input = " ".join(current_input.split()[-max_input_length:])
        
    # Splitting the lyrics into chunks of 7 words and joining them with a newline
    generated_lyrics = '\n'.join([' '.join(generated_lyrics.split()[i:i+7]) for i in range(0, len(generated_lyrics.split()), 7)])
    return generated_lyrics

def main():
    """Main function to train the model and generate lyrics."""
    
    # Clear the lyrics file
    clear_lyrics_file()

    # Fetch and store lyrics
    artists_input = input("Enter the names of the artists you want to check (separated by commas): ")
    artist_list = [artist.strip() for artist in artists_input.split(",")]
    
    api_keys = read_api_keys_from_file('keys.txt')
    sp_client = initialize_spotipy_client(api_keys)
    genius_key = api_keys['GENIUS_API_KEY']  # Define the genius_key variable
    
    for artist_name in artist_list:
        fetch_and_store_lyrics(sp_client, genius_key, artist_name)
    
    # Load and train the model
    lyrics_data = open('lyrics.txt').read().lower().splitlines()  # Keep newlines as it is
    model, tokenizer = build_and_train_model(lyrics_data)
    
    # Generate lyrics loop
    while True:
        starting_phrase = input(f"Enter a starting phrase or press Enter to use '{artist_name}': ")
        if not starting_phrase:
            starting_phrase = artist_name
        
        try:
            word_count = int(input("Enter the desired number of words for the generated song (default is 500): "))
        except ValueError:
            print("Invalid input. Using default value of 500.")
            word_count = 500

        # Explain temperature and prompt for its value
        print("\nTemperature is a parameter to control the randomness of predictions. "
              "A value closer to 0 will make the text more predictable, while a value "
              "closer to 1 will make it more random.")
        try:
            temperature = float(input("Enter the temperature for sampling (default is 2.0, range: 0.01 to 2.0): "))  # Default temperature set to 2.0
            if temperature < 0.01:
                temperature = 0.01
            elif temperature > 2.0:
                temperature = 2.0
        except ValueError:
            print("Invalid input. Using default temperature of 2.0.")  # Default temperature set to 2.0
            temperature = 2.0

        lyrics = generate_lyrics(model, tokenizer, starting_phrase, word_count, temperature)
        print(lyrics)
        
        another_song = input("\nDo you want to generate another song? (yes/no): ").strip().lower()
        if another_song != "yes":
            break

if __name__ == "__main__":
    main()