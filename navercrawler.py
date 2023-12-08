import json
import urllib.request
import os
import sys
import datetime
import time

def get_request_url(url, cid, cs): # Get request url & Get response
    req = urllib.request.Request(url)
    req.add_header("X-Naver-Client-Id", cid) # Naver API Client ID
    req.add_header("X-Naver-Client-Secret", cs) # Naver API Client Secret

    try:
        response = urllib.request.urlopen(req) # Get response

        if response.getcode() == 200: # If response is success
            print("[%s] Url Request Success" % datetime.datetime.now()) # Print success message
            return response.read().decode('utf-8') # Returns response data
    
    except Exception as e: # If response is fail
        print(e) # Print error message
        print("[%s] Error for URL : %s" % (datetime.datetime.now(), url))
        return None

def getNaverSearchResult(sNode, search_text, page_start, display, cid, cs): # Get Naver search result as json
    base = "https://openapi.naver.com/v1/search" # Naver API base url
    node = "/%s.json" % sNode # Naver API request node
    parameters = "?query=%s&start=%s&display=%s" % (urllib.parse.quote(search_text), page_start, display) # Naver API request parameters
    url = base + node + parameters # Naver API full url

    retData = get_request_url(url, cid, cs) # Get response data

    if (retData == None):
        return None # If response is fail return None
    else:
        return json.loads(retData) # Returns json data

def getPostData(sNode, post, jsonResult): # Get post processed data
    org_link = ""

    # parse data from json
    title = post['title']
    link = post["link"]
    description = post['description']

    # Shape data into certain format by source
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

def main(search_text, cid, cs):
    nodeName = ["blog", "news", "cafearticle"]
    #search_text = str(input("검색어를 입력하세요: \n")) # Get search text from user
    display_count = 100

    for sNode in nodeName:
        jsonResult = []
        
        jsonSearch = getNaverSearchResult(sNode, search_text, 1, display_count, cid, cs) # Get Naver search result as json

        while ((jsonSearch != None) and (jsonSearch['display'] != 0)): # If response data is present
            for post in jsonSearch['items']:
                getPostData(sNode, post, jsonResult) # Get post processed data

            nStart = jsonSearch['start'] + jsonSearch['display'] # Get next start number
            jsonSearch = getNaverSearchResult(sNode, search_text, nStart, display_count) # Search again
        
        with open('%s_naver_%s.json' % (search_text, sNode), 'w', encoding='utf8') as outfile: # Save json data as file
            print(jsonResult)
            retJson = json.dumps(jsonResult, indent=4, sort_keys=True, ensure_ascii=False)
            outfile.write(retJson) # Write json data to file

    print('%s_naver_%s.json SAVED' % (search_text, sNode)) # Print success message

if (__name__ == "__main__"):
    main(str(input("검색어 입력: ")), str(input("NAVER Open API Client ID 입력: ")), str(input("NAVER Open API Client Secret 입력: ")))

