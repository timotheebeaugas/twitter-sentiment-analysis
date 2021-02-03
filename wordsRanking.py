# -*- coding: utf8 -*-
from datetime import date, timedelta, datetime
from mots_vides import StopWordFactory, stop_words
import csv, os, re, emoji
import pandas as pd

yesterdayDate = str(datetime.utcnow().date().today()-timedelta(1)) # date storage to open file

def getAllTweets():
    data = pd.read_csv("input/"+yesterdayDate+".csv", header=None)
    return data.iloc[:, 1].to_string()

def removeEnglishStopWords():
    """
    deletion of common english words (default)
    """
    englishStopWords = stop_words('en')
    return englishStopWords.rebase(getAllTweets(), '')

def removeStopWords():
    """
    deletion of common words (additional language)
    """
    frenchStopWords = StopWordFactory().get_stop_words('french')
    return frenchStopWords.rebase(removeEnglishStopWords(), '')

def cleanText():
    """ 
    removal of numbers, accents, emoji and punctuation 
    """
    tweets = re.sub('@[^\s]+',' ',removeStopWords()) # remove mentions
    tweets = re.sub(r'http\S+', ' ',tweets) # remove http adress
    tweets = re.sub('[\W_]+\s', ' ', tweets) # remove all no word character
    tweets = emoji.get_emoji_regexp().sub(u'', tweets) # remove emoticons
    translateChars = "àâéèêëïîôùûç" # remove accent
    replaceChars= "aaeeeeiiouuc"
    deleteChars = """!"#$%&'()*+,-./:;<=>?@[\]^_`´{|}~’0123456789“”«»""" # remove punctuation
    text = tweets.maketrans(translateChars, replaceChars, deleteChars)
    textTranslated = tweets.translate(text)
    return textTranslated.lower().split()

def excludedWords():
    """ 
    optional word exclusion 
    """
    excludedWordsList = [
        "exclure", # mot you want to exclude 
    ]
    purgedList = []

    for a in cleanText():
        if a not in excludedWordsList:
            purgedList.append(a)
    return purgedList

def wordCount():
    """
    word occurrence count 
    """
    counts = dict()
    words = excludedWords()
    for word in words:
        if word in counts:
            counts[word] += 1
        else:
            counts[word] = 1
    return counts

def sortList():
    """
    sorting data and ranking in ascending order 
    """
    count = 0
    topTenWords = {}
    for a, b in sorted(wordCount().items(), key=lambda x: x[1], reverse=True):
        topTenWords[a] = b
        count += 1
        if count == 10: # ranking limit
            break
    return topTenWords

def saveData():        
    print(yesterdayDate)
    """ 
    save data in CSV with date
    delete the source file to release disk space
    """
    if os.path.exists("input/"+yesterdayDate+".csv"): 
        print(sortList()) # Print results before saving in CSV file
        finalList = [yesterdayDate]
        for a, b in zip(sortList().keys(), sortList().values()):
            finalList.append(a)
            finalList.append(b)
        with open('output/wordsRanking.csv', 'a', newline='', encoding='utf-8') as csv_file:
            csv_writer = csv.writer(csv_file, delimiter=',')
            csv_writer.writerow(finalList)
        os.remove("input/"+yesterdayDate+".csv")
    else:
        print("Output CSV file not found")
        pass

