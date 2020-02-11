from bert_serving.client import BertClient
from sklearn.metrics.pairwise import cosine_similarity

bc = BertClient()

def word_searcher(self, document):
    count = [x * 0 for x in range(len(self.word_set))]
    document_word_list = document.split(' ')
    for i in range(len(self.word_set)):
        word = self.word_set[i]
        vec_word = bc.encode(word)
        for doc_word in document_word_list:
            vec_doc_word = bc.encode(doc_word)
            if cosine_similarity(vec_word, vec_doc_word)>0.4:
                count[i] = count[i] + 1

        