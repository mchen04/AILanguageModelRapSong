# SongsmithAI

## Description
SongsmithAI is a project designed to generate song lyrics using deep learning models. It leverages TensorFlow and Keras for model building and training, Spotipy for fetching song data from Spotify, and LyricsGenius to scrape lyrics from Genius.

## Installation
Before running the code, ensure that you have Python installed on your system along with the following packages:
- numpy
- tensorflow
- matplotlib
- lyricsgenius
- spotipy
- langdetect

Use the following command to install the required packages:
```bash
pip install numpy tensorflow matplotlib lyricsgenius spotipy langdetect
Usage

To run the SongsmithAI, execute the main script in the terminal:

bash
Copy code
python main.py
You will be prompted to enter the names of artists for which you want to generate lyrics. After entering the artist names, the script will:

Clear the previous lyrics data.
Fetch and store new lyrics from the specified artists.
Train a deep learning model with the collected lyrics.
Allow you to generate new song lyrics based on a starting phrase you provide.
Configuration
Modify the following files as needed:

keys.txt: Add your Spotify and Genius API keys here.
lyrics.txt: This file will be automatically populated with lyrics fetched by the script.
Components
train_model.py: Contains the logic for building and training the LSTM model.
fetch_lyrics.py: Handles fetching and cleaning lyrics from Genius and Spotify.
main.py: The main driver script that orchestrates the training and lyric generation process.
Contribution
Contributions to SongsmithAI are welcome. Please ensure that you follow the code style and provide documentation for your changes.

