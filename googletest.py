import csv
from crawler_class import GoogleCrawler
from multiprocessing import Pool

def google_search_word_input(path):
    search_word_list = []

    with open(path,newline='') as swinput:
        reader = csv.reader(swinput)
        for row in reader:
            search_word_list.append(row[0])
    return search_word_list

def word_set_input(path):
    word_set_list = []

    with open(path,newline='') as swinput:
        reader = csv.reader(swinput)
        for row in reader:
            word_set_list.append(row[0])
    return word_set_list

def enum_test(word_list):
    temp = []
    for word in enumerate(word_list):
        temp.append(word)
    return temp

if __name__=='__main__':
    google_input_path = './google_search_keywords.csv'
    word_set_input_path = './word_set.csv'

    search_word_list = google_search_word_input(google_input_path)
    word_set_list = word_set_input(word_set_input_path)
    #print(word_set_list)

    crawler = GoogleCrawler(path = './chromedriver',
        word_set=word_set_list,
        date_min='1/1/2019',
        date_max='12/31/2019',
        page_limit=5)
    temp = enum_test(search_word_list)
    for current_keyword in temp:
        crawler.go_crawl(current_keyword)

    
    #print(temp)
    '''pool = Pool(processes=1)
    pool.map(crawler.go_crawl,temp,chunksize=1)'''

    #pool = Pool(processes=1)
    #temp_keyword = [("'india' PPP ADB",-1)]#,('beta',1),('caesar',2),('double',3)]
    #pool.map(go_crawl,temp_keyword)