# Audio Keyword Collector

This is a tool to extract spoken word utterances from audio, and preprocess the clips to prepare them for machine learning algorithms.  The tool can collect utterances from YouTube videos, or utterances can be extracted from local wav files instead.

![](extract_graphic.png)

# Features

* Extracts and exports desired keyword utterances from long-form audio
* Uploads collected utterances, raw audio, and resampled wav files to GCP Cloud Storage 
* Stores records of search results, downloaded audio, and number of collected utterances per file in GCP database
* Automatically resamples downloaded audio and converts to 1-channel 
* Allows for custom search queries to find relevant audio on YouTube