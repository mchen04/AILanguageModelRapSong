# SongsmithAI

## Description
SongsmithAI is a cutting-edge project aimed at creating song lyrics with the help of deep learning. Utilizing the powerful TensorFlow and Keras libraries, it constructs and trains models to mimic the art of songwriting. Integration with Spotify's Spotipy library and the LyricsGenius API allows SongsmithAI to gather a vast dataset of songs for analysis and learning.

## Installation
Ensure you have Python and the following packages installed:

- numpy
- tensorflow
- matplotlib
- lyricsgenius
- spotipy
- langdetect

Install the required packages with the command:
```bash
pip install numpy tensorflow matplotlib lyricsgenius spotipy langdetect

Usage
Run SongsmithAI via the command line by typing:

bash
Copy code
python main.py
Follow the prompts to input artist names. The script will:

Clear existing lyric data.
Fetch and store lyrics from the specified artists.
Train a neural network with the newly acquired lyrics.
Enable lyric generation based on your input phrase.
Configuration
Update these files as needed:

keys.txt: Insert your Spotify and Genius API credentials.
lyrics.txt: This file will be auto-filled with lyrics by the script.
Components
train_model.py: Constructs and trains the LSTM neural network.
fetch_lyrics.py: Acquires and sanitizes lyrics data.
main.py: Orchestrates the training and generation processes.
Contribution
Contributions are encouraged! Please adhere to the project's coding standards and document any changes you make.
