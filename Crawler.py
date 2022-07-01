#Import Required Libs/Functions
import requests
from CrawlerSettings import CrawlerInvalidParameters, getDefaultNumberOfWords, getDefaultUrl, CrawlerCommandLine
from bs4 import BeautifulSoup
from typing import Dict, List, Set
from collections import Counter

import re


def CleanedWordList(soup: BeautifulSoup, exWordList: List[str]):
    """
        This will process and filter words based on the text from a BeautifulSoup Object.
    """

    if soup != None:
        # get the list of words
        wordList = [word.strip().lower() for word in soup.getText().split()]

        # set a new list to capture the filtered words
        cleanedWords = []
        for word in wordList:
            # replace the symbols
            replaceSymbols = "!@#$%^&*()_-+={[}]|\;:\"<>?/.,"
            for i in range(len(replaceSymbols)):
                word = word.replace(replaceSymbols[i], '')

            # split the words if they are separated by a space
            words = word.split()

            # add the words to the processed list
            for cleanedAndSplitWords in words:
                if len(cleanedAndSplitWords) > 0 and cleanedAndSplitWords not in exWordList:
                    cleanedWords.append(word)

        return cleanedWords
    else:
        raise CrawlerInvalidParameters(
            "Invalid BeautifulSoup Object passed as a parameter.")





def crawlerMain(url: str, numberOfWordsToReturn:int, exWords: Set = None, localPath: str = None) -> Dict:

    '''
        Main Crawling Function, Scrapes the provided URL and returns a list of sorted/counted words based on occurance
    '''

    # Verify the validity of the URL
    if url != None and len(url) > 0:
        if not(url.startswith('https://')):
                raise CrawlerInvalidParameters('URL is Invalid')
    elif localPath == None:
        raise CrawlerInvalidParameters('URL is Invalid')

    # Varify the number of words the user wants to return
    if numberOfWordsToReturn == None:
        numberOfWordsToReturn = getDefaultNumberOfWords()

    if numberOfWordsToReturn < 0:
        raise CrawlerInvalidParameters('Invalid: Number of words to return must be a positive integer')

    # Verify the validity of the list of excluded words
    if exWords != None:
        for word in exWords:
            if not isinstance(word, str):
                raise CrawlerInvalidParameters('List of excluded words is invalid')


    try:

        # Get the URL source code
        urlSource = None
        if localPath != None:
            source = open(localPath, encoding="utf8")
        else:
            source = requests.get(url).text

        # Regex To grab the "History" Section of the Wikipedia Page specifically
        sourceHistory = re.search('(?<=History )[\S\s]*(?=Corporate affairs)', source)

        # Create the Beautiful Soup Object
        if localPath != None:
            soup = BeautifulSoup(sourceHistory.group(0).read(), 'html.parser')
        else:
            soup = BeautifulSoup(sourceHistory.group(0), 'html.parser')

        # Clean unseen text for teh user
        [e.extract() for e in soup(['style', 'script', 'head', 'title', 'meta', '[document]'])]

        # Collect all of teh cleaned words
        cleanWords = CleanedWordList(soup, exWords)

        # Count the frequency of the cleaned words
        counts = Counter(cleanWords)

        # Return the sorted list of the most common words (default is top 10)
        return counts.most_common(numberOfWordsToReturn)

    except Exception as e:
        raise e