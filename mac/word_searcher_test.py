# pip install spacy
# python -m spacy download en_core_web_sm
# conda install -c conda-forge spacy

'''def word_searcher(self,document):
    count = [x*0 for x in range(len(word_set))]
    document_word_list = document.split(' ')
    for i in range(len(word_set)):
        word = word_set[i]
        for doc_word in document_word_list:
            if doc_word == word:
                count[i] = count[i]+1
    
    return count'''


# new!
import re
from collections import Counter
import spacy
from spacy.matcher import PhraseMatcher
def word_searcher(document):
    # to init
    nlp = spacy.load('en_core_web_sm-2.2.5')
    phrase_matcher = PhraseMatcher(nlp.vocab)
    word_set = ['machine learning', 'robots', 'intelligent agents']
    patterns = [nlp(text) for text in word_set]
    phrase_matcher.add('hama', None, *patterns)
    # function body
    processed_document = document.lower()  
    processed_document = re.sub('[^a-zA-Z]', ' ', processed_document ) 
    processed_document = re.sub(r'\s+', ' ', processed_document)
    sentence = nlp(processed_document)
    matched_phrases = phrase_matcher(sentence)

    word_list = []

    for match_id, start, end in matched_phrases:
        string_id = nlp.vocab.strings[match_id]  
        span = sentence[start:end]                   
        word_list.append(span.text)
        print(match_id, string_id, start, end, span.text)

    #print("---Counter()---")
    result = Counter(word_list)
    print(result)

    count = []
    for key in word_set:
        count.append(result[key])

    res = sorted(result.items(),key=(lambda x:x[1]),reverse = True)

    resres = []
    for i in res:
        resres.append(str(i[0])+' '+str(i[1]))

    print(count)
    print(resres)

article_text = 'In intelligent agents computer science, artificial intelligence (AI), sometimes called machine intelligence, is intelligence demonstrated by machines, in contrast to the natural intelligence displayed by humans. Leading AI textbooks define the field as the study of "intelligent agents": any device that perceives its environment and takes actions that maximize its chance of successfully achieving its goals.[1] Colloquially, the term "artificial intelligence" is often used to describe machines (or computers) that mimic "cognitive" functions that humans associate with the human mind, such as "learning" and "problem solving".[2]'
word_searcher(article_text)

