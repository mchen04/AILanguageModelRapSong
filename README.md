# SongsmithAI

## Description
SongsmithAI is a state-of-the-art deep learning project designed to generate song lyrics. It leverages the powerful TensorFlow and Keras libraries to build and train models that emulate the craft of songwriting. The project integrates with Spotify's Spotipy library and the LyricsGenius API to amass a comprehensive dataset of song lyrics for analysis and training purposes.

## Installation
Before installation, ensure you have Python installed on your system. Then, install the necessary packages:

- numpy
- tensorflow
- matplotlib
- lyricsgenius
- spotipy
- langdetect

You can install all required packages using the following command:
pip install numpy tensorflow matplotlib lyricsgenius spotipy langdetect


## Usage
To run SongsmithAI, execute the following steps from the command line:


Follow the interactive prompts to input artist names. The script will perform the following actions:

1. Clear any existing lyric data.
2. Fetch and store lyrics from the specified artists.
3. Train a neural network with the collected lyrics.
4. Generate lyrics based on your input phrase.

## Configuration
To configure the application, update the following files as necessary:

- `keys.txt`: Add your Spotify and Genius API credentials here.
- `lyrics.txt`: The script will automatically populate this file with lyrics.

## Components
- `train_model.py`: Builds and trains the LSTM neural network.
- `fetch_lyrics.py`: Gathers and cleanses the lyrics data.
- `main.py`: Manages the training and lyric generation workflow.

## Contribution
We welcome contributions! If you'd like to contribute, please follow the project's coding standards and thoroughly document any changes. Your contributions can help improve SongsmithAI's functionality and accuracy.
