import json
import urllib.request
import os
import sys
import datetime
import time

def get_request_url(url):
    req = urllib.request.Request(url)
    req.add_header("X-Naver-Client-Id", "")
    req.add_header("X-Naver-Client-Secret", "")

    try:
        response = urllib.request.urlopen(req)

        if response.getcode() == 200:
            print("[%s] Url Request Success" % datetime.datetime.now())
            return response.read().decode('utf-8')
    
    except Exception as e:
        print(e)
        print("[%s] Error for URL : %s" % (datetime.datetime.now(), url))
        return None

def getNaverSearchResult(sNode, search_text, page_start, display):
    base = "https://openapi.naver.com/v1/search"
    node = "/%s.json" % sNode
    parameters = "?query=%s&start=%s&display=%s" % (urllib.parse.quote(search_text), page_start, display)
    url = base + node + parameters

    retData = get_request_url(url)

    if (retData == None):
        return None
    else:
        return json.loads(retData)

def getPostData(sNode, post, jsonResult):
    org_link = ""

    title = post['title']
    link = post["link"]
    description = post['description']

    if (sNode == "news"):
        org_link = post['originallink']
        link = post['link']

        pDate = datetime.datetime.strptime(post['pubDate'], '%a, %d %b %Y %H:%M:%S +0900')
        pDate = pDate.strftime('%Y-%m-%d %H:%M:%S')

        jsonResult.append({'title':title, 'description':description, 'org_link':org_link, 'link':org_link, 'pDate':pDate})

    elif (sNode == "blog"):
        postdate = post['postdate']
        bloggername = post['bloggername']
        bloggerlink = post['bloggerlink']

        jsonResult.append({'title':title, 'description':description, 'link':link, 'postdate':postdate, 'bloggername':bloggername, 'bloggerlink':bloggerlink})

    else:
        cafename = post['cafename']
        cafeurl = post['cafeurl']

        jsonResult.append({'title':title, 'description':description, 'link':link, 'cafename':cafename, 'cafeurl':cafeurl})

    return

def main():
    nodeName = ["blog", "news", "cafearticle"]
    search_text = str(input("검색어를 입력하세요: \n"))
    display_count = 100

    for sNode in nodeName:
        jsonResult = []
        
        jsonSearch = getNaverSearchResult(sNode, search_text, 1, display_count)

        while ((jsonSearch != None) and (jsonSearch['display'] != 0)):
            for post in jsonSearch['items']:
                getPostData(sNode, post, jsonResult)

            nStart = jsonSearch['start'] + jsonSearch['display']
            jsonSearch = getNaverSearchResult(sNode, search_text, nStart, display_count)
        
        with open('%s_naver_%s.json' % (search_text, sNode), 'w', encoding='utf8') as outfile:
            print(jsonResult)
            retJson = json.dumps(jsonResult, indent=4, sort_keys=True, ensure_ascii=False)
            outfile.write(retJson)

    print('%s_naver_%s.json SAVED' % (search_text, sNode))

if (__name__ == "__main__"):
    main()

