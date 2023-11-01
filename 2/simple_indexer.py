#!/usr/bin/env python3

import os
import string
import math
from nltk.stem import PorterStemmer

class SimpleIndexer:
    def __init__(self) -> None:
        self.__documents = []
        self.__names = dict()
        self.__index = {}
        self.__id = 0
        self.__stop_words = ['a', 'about', 'above', 'across', 'after', 'again', 'against', 'all', 'almost', 'alone', 'along', 'already', 'also', 'although', 'always', 'among', 'an', 'and', 'another', 'any', 'anybody', 'anyone', 'anything', 'anywhere', 'are', 'area', 'areas', 'around', 'as', 'ask', 'asked', 'asking', 'asks', 'at', 'away', 'b', 'back', 'backed', 'backing', 'backs', 'be', 'became', 'because', 'become', 'becomes', 'been', 'before', 'began', 'behind', 'being', 'beings', 'best', 'better', 'between', 'big', 'both', 'but', 'by', 'c', 'came', 'can', 'cannot', 'case', 'cases', 'certain', 'certainly', 'clear', 'clearly', 'come', 'could', 'd', 'did', 'differ', 'different', 'differently', 'do', 'does', 'done', 'down', 'down', 'downed', 'downing', 'downs', 'during', 'e', 'each', 'early', 'either', 'end', 'ended', 'ending', 'ends', 'enough', 'even', 'evenly', 'ever', 'every', 'everybody', 'everyone', 'everything', 'everywhere', 'f', 'face', 'faces', 'fact', 'facts', 'far', 'felt', 'few', 'find', 'finds', 'first', 'for', 'four', 'from', 'full', 'fully', 'further', 'furthered', 'furthering', 'furthers', 'g', 'gave', 'general', 'generally', 'get', 'gets', 'give', 'given', 'gives', 'go', 'going', 'good', 'goods', 'got', 'great', 'greater', 'greatest', 'group', 'grouped', 'grouping', 'groups', 'h', 'had', 'has', 'have', 'having', 'he', 'her', 'here', 'herself', 'high', 'high', 'high', 'higher', 'highest', 'him', 'himself', 'his', 'how', 'however', 'i', 'if', 'important', 'in', 'interest', 'interested', 'interesting', 'interests', 'into', 'is', 'it', 'its', 'itself', 'j', 'just', 'k', 'keep', 'keeps', 'kind', 'knew', 'know', 'known', 'knows', 'l', 'large', 'largely', 'last', 'later', 'latest', 'least', 'less', 'let', 'lets', 'like', 'likely', 'long', 'longer', 'longest', 'm', 'made', 'make', 'making', 'man', 'many', 'may', 'me', 'member', 'members', 'men', 'might', 'more', 'most', 'mostly', 'mr', 'mrs', 'much', 'must', 'my', 'myself', 'n', 'necessary', 'need', 'needed', 'needing', 'needs', 'never', 'new', 'new', 'newer', 'newest', 'next', 'no', 'nobody', 'non', 'noone', 'not', 'nothing', 'now', 'nowhere', 'number', 'numbers', 'o', 'of', 'off', 'often', 'old', 'older', 'oldest', 'on', 'once', 'one', 'only', 'open', 'opened', 'opening', 'opens', 'or', 'order', 'ordered', 'ordering', 'orders', 'other', 'others', 'our', 'out', 'over', 'p', 'part', 'parted', 'parting', 'parts', 'per', 'perhaps', 'place', 'places', 'point', 'pointed', 'pointing', 'points', 'possible', 'present', 'presented', 'presenting', 'presents', 'problem', 'problems', 'put', 'puts', 'q', 'quite', 'r', 'rather', 'really', 'right', 'right', 'room', 'rooms', 's', 'said', 'same', 'saw', 'say', 'says', 'second', 'seconds', 'see', 'seem', 'seemed', 'seeming', 'seems', 'sees', 'several', 'shall', 'she', 'should', 'show', 'showed', 'showing', 'shows', 'side', 'sides', 'since', 'small', 'smaller', 'smallest', 'so', 'some', 'somebody', 'someone', 'something', 'somewhere', 'state', 'states', 'still', 'still', 'such', 'sure', 't', 'take', 'taken', 'than', 'that', 'the', 'their', 'them', 'then', 'there', 'therefore', 'these', 'they', 'thing', 'things', 'think', 'thinks', 'this', 'those', 'though', 'thought', 'thoughts', 'three', 'through', 'thus', 'to', 'today', 'together', 'too', 'took', 'toward', 'turn', 'turned', 'turning', 'turns', 'two', 'u', 'under', 'until', 'up', 'upon', 'us', 'use', 'used', 'uses', 'v', 'very', 'w', 'want', 'wanted', 'wanting', 'wants', 'was', 'way', 'ways', 'we', 'well', 'wells', 'went', 'were', 'what', 'when', 'where', 'whether', 'which', 'while', 'who', 'whole', 'whose', 'why', 'will', 'with', 'within', 'without', 'work', 'worked', 'working', 'works', 'would', 'x', 'y', 'year', 'years', 'yet', 'you', 'young', 'younger', 'youngest', 'your', 'yours', 'z']
        self.__stemmer = PorterStemmer()
        self.__stop_words = [self.__stemmer.stem(word) for word in self.__stop_words]

    def index_document(self, document:str, name:str=""):
        id = self.next_id()
        self.__documents.append((id,document))
        tokens = self.preprocess(document)
        vocabulary = sorted(set(tokens))
        for word in vocabulary:
            if word not in self.__index:
                self.__index[word] = dict()
            self.__index[word][id] = tokens.count(word)
        self.__names[name] = id

    def tf(self, term:str, doc_id:int):
        if term in self.__index:
            if doc_id in self.__index[term]:
                return math.log(1 + self.__index[term][doc_id])
        return 0
    
    def idf(self, term:str):
        if term in self.__index:
            return math.log(len(self.__documents) / len(self.__index[term]))
        return 0
    
    def tf_idf(self, term:str, doc_id:int):
        return self.tf(term, doc_id) * self.idf(term)

    def preprocess(self, document:str):
        document = document.lower()
        for p in string.punctuation:
            document = document.replace(p, "")
        document = document.split()
        document = [self.__stemmer.stem(word) for word in document]
        document = [word for word in document if word not in self.__stop_words]
        return document

    def id(self):
        return self.__id
    
    def next_id(self):
        id = self.__id
        self.__id += 1
        return id
    
    def documents(self):
        return self.__documents
    
    def index(self):
        return self.__index
    
    def get_document(self, id):
        for doc_id, doc in self.__documents:
            if doc_id == id:
                return doc
        return None
    
    def search(self, query: str):
        query = self.preprocess(query)
        query = sorted(set(query))
        scores = dict()
        for doc_id, _ in self.__documents:
            scores[doc_id] = 0
            for term in query:
                scores[doc_id] += self.tf_idf(term, doc_id)
        return scores
    
    def name(self, id):
        for name, doc_id in self.__names.items():
            if doc_id == id:
                return name
        return None

def main():
    if not os.path.exists("DataAssignment4"):
        print("DataAssignment4 folder not found")
        return
    
    indexer = SimpleIndexer()
    
    for file in os.listdir("DataAssignment4"):
        if file.endswith(".txt"):
            print("Indexing", file)
            with open(os.path.join("DataAssignment4", file), "r") as f:
                indexer.index_document(f.read(), name="DataAssignment4/" + file)

    queries = ["claim", "claim*", "claim of duty"]
    for query in queries:
        scores = indexer.search(query)
        scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        print("Query:", query)
        for doc_id, score in scores:
            print(f"\t{indexer.name(doc_id)} with score {score}")

if __name__ == "__main__":
    main()