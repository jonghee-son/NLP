import wordcloud as wc
import navercrawler as nvc

def crawlerMain():
    num = 0
    exitYN = ""
    searchText = ""

    while (True):
        print()
        print("========================================================")
        print("종료를 하시기 위해서는 Y를 입력하여 주시기 바랍니다.")
        print()
        print("1. 네이버 수집")
        print("2. 그래프 출력 / 워드 클라우드")
        print()
        print("========================================================")
        print()

        num = int(input("항목 번호 입력: "))
        #searchText = ""
        searchSource = 0

        if (num == 1):
            cid = str(input("NAVER Open API Client ID 입력: "))
            cs = str(input("NAVER Open API Client Secret 입력: "))
            searchText = str(input("검색어 입력: "))
            nvc.main(searchText, cid, cs)
        elif (num == 2):
            if (searchText != ""):
                print()
                print("======================================================")
                print("검색 출처 선택")
                print("1. blog")
                print("2. news")
                print("3. cafearticle")
                print("======================================================")
                print()
                searchSource = int(input("항목 번호 입력: "))
                wc.main(searchText, searchSource)
            else:
                searchText = str(input("검색어 입력: "))
                print()
                print("======================================================")
                print("검색 출처 선택")
                print("1. blog")
                print("2. news")
                print("3. cafearticle")
                print("======================================================")
                print()
                searchSource = int(input("항목 번호 입력: "))
                wc.main(searchText, searchSource)
                

        else:
            print("항목 번호를 잘못 입력하였습니다. 다시 입력하여 주시기 바랍니다.")
            print()

        exitYN = input("종료를 하시려면 Y 또는 y를 입력하여 주시기 바랍니다")
        #searchText = ""

        if (exitYN == "Y" or exitYN == "y"):
            break

if __name__ == "__main__":
    crawlerMain()

