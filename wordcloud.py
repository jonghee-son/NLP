import json
import re
import os

from konlpy.tag import Okt
from collections import Counter

import matplotlib.pyplot as plt
import matplotlib
from matplotlib import font_manager, rc

import pytagcloud
import webbrowser

def showGraph(wordInfo):
    font_location = "C:/Windows/Fonts/malgun.ttf"
    font_name = font_manager.FontProperties(fname=font_location).get_name()
    matplotlib.rc('font', family=font_name)

    plt.xlabel('주요 단어')
    plt.ylabel('빈도수')
    plt.grid(True)

    Sorted_Dict_Values = sorted(wordInfo.values(), reverse=True) # Sort data according to value
    Sorted_Dict_Keys = sorted(wordInfo, key=wordInfo.get, reverse=True) # Sort data according to key

    plt.bar(range(len(wordInfo)), Sorted_Dict_Values, align='center') # Create bar according to data values
    plt.xticks(range(len(wordInfo)), list(Sorted_Dict_Keys), rotation=70) # Set x-axis labels
    
    plt.show() # Show graph

def saveWordCloud(wordInfo, filename):
    taglist = pytagcloud.make_tags(dict(wordInfo).items(), maxsize=80)
    pytagcloud.create_tag_image(taglist, filename, size = (640, 480), fontname='korean', rectangular=False) # Create wordcloud image
    webbrowser.open(filename)

def main(searchTerm, searchSource):
    #searchTerm = str(input("검색어 입력: "))
    #searchSource = str(input("검색 출처 입력: "))
    source = ""
    __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

    if (searchSource == 1):
        source = "blog"
    elif (searchSource == 2):
        source = "news"
    elif (searchSource == 3):
        source = "cafearticle"

    openFileName = __location__ + '\\' + searchTerm +'_naver_' + source + '.json' # data(json) location
    cloudImagePath = openFileName + '.jpg'

    rfile = open(openFileName, 'r', encoding='utf-8').read() # Open data file

    jsonData = json.loads(rfile)
    message = ''

    for item in jsonData:
        if 'description' in item.keys():
            message = message + re.sub(r'[^\w]', ' ', item['description']) + ' ' # Get message part of data file

    nlp = Okt() # Uses Okt model of KoNLPy
    nouns = nlp.nouns(message) # get nouns from data
    count = Counter(nouns) # Count nouns

    wordInfo = dict() # Create empty dictionary
    for tags, counts in count.most_common(50): # Get 50 most commonly appeared nouns in data
        if (len(str(tags)) > 1):
            wordInfo[tags] = counts # Save nouns longer than 1
            print("%s : %d" % (tags, counts))

    showGraph(wordInfo)
    saveWordCloud(wordInfo, cloudImagePath)

if (__name__ == "__main__"):
    main(str(input("검색어 입력: ")), int(input("검색 출처 입력: ")))

