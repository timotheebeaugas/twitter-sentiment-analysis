# Twitter opinion mining 
This project connect to the twitter API and retrieve tweets for daily analysis.
A first program to connect to twitter to retrieve tweet in real time and save them in a CSV file.
A second program analyzes the sentiment of tweets with a package and a third class the more recursive words.
In this example the program searches all tweets using the word `france` and excludes the word `exclure`. It is possible to find and exclude multiple words.
At the end we get CSV files ready to be analyzed.
This project uses Python `3.9.0`.

### Project description

    .
    ├── input                      # Real-time tweet recording in a CSV file
    ├── output                     # Saving analysis results in a CSV file
    ├── config.py                  # Twitter API login data
    ├── requirements               # Required packages
    ├── script.py                  # Launch tweets analysis every day at a specific time
    ├── sentimentsAnalysis.py      # Tweet sentiment analysis
    |── twitterSteam.py            # Launch tweeter's stream and reconnection in case of errors
    ├── wordsRanking.py            # Ranking of the most recurring words
    └── README.md


### Install packages 
```
pip install -r requirements.txt 
```
### Run data analysis 
```
python script.py
```
### Lunch twitter stream
```
python twitterStream.py
```