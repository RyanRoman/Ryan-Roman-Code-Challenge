# Crawler Settings (Constants, Word Exceptions, Command Line Code, Additional Details, etc)
import argparse

def getDefaultNumberOfWords():
    return 10

def getDefaultUrl():
    return 'https://en.wikipedia.org/wiki/Microsoft'

class CrawlerInvalidParameters(Exception):
    def __init__(self):
        pass

# Create command line aruments that users can utilize

class CrawlerCommandLine:
    def __init__(self):
        self.Parser = argparse.ArgumentParser( description = 'This web crawler will visit the provided URL and return the top number of words based on frequency.')

        self.Parser.add_argument('-url', '--url', type=str, default=getDefaultUrl(), help="The URL to be crawled (defualt = https://en.wikipedia.org/wiki/Microsoft#History)")
        self.Parser.add_argument('-nw', metavar='--numberofwords', type=int, default=10, help='the number of counted words to be returned (Defualt = 10)')
        self.Parser.add_argument('-ex', metavar='--excludedwords', nargs='+', default=[], help="Words to be excluded from the counted list")
        self.Args = self.Parser.parse_args()