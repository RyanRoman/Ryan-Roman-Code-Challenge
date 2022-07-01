from CrawlerSettings import CrawlerCommandLine
from Crawler import crawlerMain

try:
    #Runs the crawler with supplied arguments (run main.py -h for help on commands)
    cmdLine = CrawlerCommandLine()
    
    url = cmdLine.Args.url
    numberOfWordsToReturn = cmdLine.Args.nw
    exWords = cmdLine.Args.ex
    

    result = crawlerMain(url = url, numberOfWordsToReturn = numberOfWordsToReturn, exWords = exWords)

    print(result)


except Exception as e:
    print(e)