# -*- coding: utf8 -*-
from textblob import TextBlob
from textblob_fr import PatternTagger, PatternAnalyzer
import pandas as pd
from datetime import date, timedelta, datetime
import csv, os, re, emoji

yesterdayDate = str(datetime.utcnow().date().today()-timedelta(1)) # date storage to open file

def cleanText(tweets):
    """ 
    removal of mentions, url and emoji 
    """
    tweets = re.sub('@[^\s]+',' ',tweets) # remove mentions
    tweets = re.sub(r'http\S+', ' ',tweets) # remove http adress
    tweets = re.sub('[\W_]+\s', ' ', tweets) # remove all no word character
    tweets = emoji.get_emoji_regexp().sub(u'', tweets) # remove emoticons
    return tweets.lower()

def saveSentiments():        
    """
    opinion minning average for one day 
    save data in CSV file with date
    """
    data = pd.read_csv("input/"+yesterdayDate+".csv")
    f = open("output/sentimentAnalysis.csv", "a", newline='', encoding='utf-8')
    writer = csv.writer(f, delimiter=',')
    polarityAverage = []
    subjectivityAverage = []
    for i in range(len(data.index)):
        blob = TextBlob(cleanText(data.iloc[i, 1]), pos_tagger=PatternTagger(), analyzer=PatternAnalyzer())
        polarityAverage.append(blob.sentiment[0])
        subjectivityAverage.append(blob.sentiment[1])
    sum = 0
    for ele in polarityAverage: 
        sum += ele 
    polarityAverage = sum / len(polarityAverage) 
    for ele in subjectivityAverage: 
        sum += ele 
    subjectivityAverage = sum / len(subjectivityAverage) 
    writer.writerow([yesterdayDate, len(data.index), polarityAverage, subjectivityAverage])
    f.close()
