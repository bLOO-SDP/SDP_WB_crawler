from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time
from multiprocessing import Pool
import csv
import re
from collections import Counter
import spacy
from spacy.matcher import PhraseMatcher
#from bert_serving.client import BertClient
#from sklearn.metrics.pairwise import cosine_similarity
#from nltk.corpus import stopwords
#import nltk

class GoogleCrawler:
    # date_min and date_min gets formatted string such as m/d/yyyy
    def __init__(self,path,word_set,date_min,date_max,page_limit):
        self.path = path
        self.word_set = word_set
        self.date_min = date_min
        self.date_max = date_max
        self.page_limit = page_limit

        # to init
        self.nlp = spacy.load('en_core_web_sm-2.2.5')
        self.phrase_matcher = PhraseMatcher(self.nlp.vocab)
        #word_set = ['machine learning', 'robots', 'intelligent agents']
        self.patterns = [self.nlp(text) for text in word_set]
        self.phrase_matcher.add('hama', None, *(self.patterns))

    def date_limit(self,driver):
        # select date option
        tool = driver.find_element_by_id('hdtb-tls')
        tool.click()

        time.sleep(0.5)

        date = driver.find_element_by_xpath("//div[@aria-label='모든 날짜']")
        #print(date)
        date.click()

        time.sleep(0.5)

        date_option = driver.find_element_by_id("cdrlnk")
        #date_option = driver.find_element_by_link_text("기간 설정...")
        date_option.click()

        time.sleep(0.5)

        # input date min and max
        date_min_input = driver.find_elements_by_xpath("//*[@class='OouJcb ktf mini']")
        date_min_input[0].send_keys(self.date_min)
        date_max_input = driver.find_elements_by_xpath("//*[@class='rzG2be ktf mini']")
        date_max_input[0].send_keys(self.date_max)
        date_enter = driver.find_elements_by_xpath("//*[@class='Ru1Ao ksb mini']")
        date_enter[0].click()

        time.sleep(1)
    
    # new!
    def word_searcher(self,document):
        # function body
        processed_document = document.lower()  
        processed_document = re.sub('[^a-zA-Z]', ' ', processed_document ) 
        processed_document = re.sub(r'\s+', ' ', processed_document)
        sentence = self.nlp(processed_document)
        matched_phrases = self.phrase_matcher(sentence)

        word_list = []

        for match_id, start, end in matched_phrases:
            span = sentence[start:end]                   
            word_list.append(span.text)
            #print(match_id, string_id, start, end, span.text)

        #print("---Counter()---")
        result = Counter(word_list)
        #print(result)

        count = []
        for key in self.word_set:
            count.append(result[key])

        res = sorted(result.items(),key=(lambda x:x[1]),reverse = True)

        resres = []
        for i in res:
            resres.append(str(i[0])+' '+str(i[1]))

        return count,resres
        #print(count)
        #print(resres)

    '''#one to one word comparison, the possibility of replacement exists.
    def word_searcher(self,document):
        count = [x*0 for x in range(len(self.word_set))]
        document_word_list = document.split(' ')
        for i in range(len(self.word_set)):
            word = self.word_set[i]
            for doc_word in document_word_list:
                if doc_word == word:
                    count[i] = count[i]+1
        
        return count'''

    '''def word_searcher(self, document):
    
        stop_words = set(stopwords.words())
        count = [x * 0 for x in range(len(self.word_set))]
        document_word_list = document.split(' ')
        bc = BertClient(port_out=5560,port=5559)
        for i in range(len(self.word_set)):
            word = self.word_set[i]
            vec_word = bc.encode([word])
            for doc_word in document_word_list:
                if len(doc_word)<3:
                    continue
                vec_doc_word = bc.encode([doc_word])
                if not doc_word in stop_words:    
                    if cosine_similarity(vec_word, vec_doc_word)>0.93:
                        print(word,doc_word,cosine_similarity(vec_word, vec_doc_word))
                        count[i] = count[i] + 1
        return count'''

    def csv_out(self,keyword,title,link,count):
        directory = ''#'google-drive/2020_WB Project/crawl_result_nounverb/'
        output = [keyword,title,link]
        for i in count:
            output.append(i)
        #count_str = ''.join(str(e)+',' for e in count)
        with open(directory+keyword+'.csv','a',newline='', encoding='utf-8-sig') as csvfile:
            out_writer = csv.writer(csvfile)
            out_writer.writerow(output)

    def go_crawl(self,search_keyword):
        #nltk.download('stopwords') 
        # loading chrome driver
        driver = webdriver.Chrome(self.path)
        driver.set_window_size(800,500)
        driver.implicitly_wait(0.5)
        driver.set_window_position((search_keyword[0]%2)*800, (search_keyword[0]//2%2)*500)
        driver.implicitly_wait(3)

        # enter the google
        driver.get('https://www.google.com')

        # search the keywords 
        search_box = driver.find_element_by_name("q")
        search_box.send_keys(search_keyword[1])
        search_box.submit()
        driver.implicitly_wait(3)

        self.date_limit(driver) #######

        link_list = []
        count_list = []

        # 1,2페이지 검색
        for search_count in range(1,self.page_limit+1):

            # press next page button
            if search_count != 1:
                continue_link = driver.find_element_by_link_text(str(search_count))
                continue_link.click()

            google_page = driver.window_handles[0]

            # get titles of the documents and click it
            titles = driver.find_elements_by_xpath("//div[@class='r']/a")
            article_count = 0 

            # for all articles in the search result
            for article_count in range(len(titles)):
                word_count = [0,0,0]
                try:
                    titles = driver.find_elements_by_xpath("//div[@class='r']/a")
                    title_string = titles[article_count].text.splitlines()[-1]
                except:
                    title_string = "unknown title"
                    print('title out of range error occurred')
                print(title_string)

                try:
                # handling exception, the crawler must go on
                    titles = driver.find_elements_by_xpath("//div[@class='r']/a")

                    ActionChains(driver).key_down(Keys.CONTROL).click(titles[article_count]).key_up(Keys.CONTROL).perform()
                    driver.switch_to.window(driver.window_handles[-1])

                    element = driver.find_element_by_tag_name('body').text
                    link_url = driver.current_url
                    #print(element) ####### for demo
                    driver.implicitly_wait(5) ####### for demo
                    print("no error until word_searcher")
                    word_count,word_list = self.word_searcher(element)
                    print(word_list)
                    #print(word_count)
                    print('search:',search_count)
                    print('article:',article_count)
                except:
                    print('error occurred')
                    driver.switch_to.window(driver.window_handles[0])
                    continue
                
                for i in range(len(word_count)):
                    if word_count[i] != 0:
                        word_count[i] = 1

                print(word_count)
                if sum(word_count)>1:
                    link_list.append(link_url)
                    count_list.append(word_count)
                    ############################################
                    #link saving function required
                    self.csv_out(search_keyword[1],title_string,link_url,word_list)
                    ############################################
                    driver.switch_to.window(google_page)
                else:
                    driver.close()
                    driver.switch_to.window(google_page)
        print("crawling ended")
        #time.sleep(10)
        #driver.quit()
