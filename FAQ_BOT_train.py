# -*- coding: utf-8 -*-

'''name='workdaybot',
    version='1.0',
    packages=[''],
    url='',
    license='',
    author='Krutika Lodaya',
    author_email='krutika.lodaya@bcone.com',
    description='Workday Chatbot'
'''

import warnings;

import nltk
import pandas as pd

warnings.simplefilter("ignore")
from sklearn.feature_extraction.text import TfidfVectorizer, TfidfTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn import model_selection
#import matplotlib.pyplot as plt
from textblob import TextBlob
import pickle
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import re
from nltk.tag.stanford import StanfordNERTagger


'''import spacy
from spacy import displacy
from collections import Counter
import en_core_web_sm
nlp = en_core_web_sm.load()'''

#nltk.download('stopwords') #note : run this at time of environment preparation
#nltk.download()
class train_model:

    def __init__(self,filename, filenamestore):
        self.filename = filename
        self.filenamestore = filenamestore

    def split_into_tokens(self,message):
        message = str(message)
        message = TextBlob(message).correct() #convert bytes into proper unicode
        return TextBlob(message).words

    def remove_stop_words_and_lemmas(self,message):
        message = str(re.sub(r'[^\x00-\x7F]+',' ', message)).lower()
        #print(message)
        #translator = str.maketrans("", "", string.punctuation)
        #strip_puct = message.translate(string.maketrans("", ""), string.punctuation)
        #strip_digits = strip_puct.translate(string.maketrans("", ""), string.digits)
        #word_tokens = word_tokenize(message.translate(None, string.punctuation))
        word_tokens = word_tokenize(message)
        print(word_tokens)
        stop = set(stopwords.words('english'))
        stop_m = [i for i in word_tokens if str(i).lower() not in stop]
        print(stop_m)
        lemmatizer = WordNetLemmatizer()
        filtered_sentence = [lemmatizer.lemmatize(w) for w in stop_m]
        #print('inside stop word and lemma :',filtered_sentence)
        #print(filtered_sentence)
        return [lemmatizer.lemmatize(w) for w in stop_m]

    def split_into_lemmas(self, message):
        message = str(message).lower()
        words = TextBlob(message).words
        # for each word, take its "base form" = lemma
        return [word.lemma for word in words]


    def preprocess_data(self):
        global df
        #names=['sentences', 'class', 'other']
        df = pd.read_csv(self.filename, header=None, sep=',', names=['question', 'answer','class','user'],encoding = 'unicode_escape')
        #print(df)
        #global bow_transformer
        #list_of_lemma=split_into_lemmas
        bow_transformer = TfidfVectorizer(analyzer=self.remove_stop_words_and_lemmas,ngram_range=(1,5)).fit(df['question'])
        messages_bow = bow_transformer.transform(df['question'])
        #global tfidf_transformer
        tfidf_transformer = TfidfTransformer().fit(messages_bow)
        messages_tfidf = tfidf_transformer.transform(messages_bow)
        #print(messages_tfidf)
        #global le
        #le = preprocessing.LabelEncoder()
        #le.fit(list(df['class']))
        X = messages_tfidf
        y = list(df['answer'])
        print(X)
        print(y)
        #print("sentences, classes",df['sentences'],df['class'])
        return X, y

    def standtagger(self):
        text = "Where can I update my date of birth?"
        st = StanfordNERTagger('D:\\PycharmProjects\\workdaybot\\stanford-ner-2018-02-27\\classifiers\\english.all.3class.distsim.crf.ser.gz',
                               'D:\\PycharmProjects\\workdaybot\\stanford-ner-2018-02-27\\stanford-ner.jar',
                               encoding='utf-8')
        tokenized_text = word_tokenize(text)
        classified_text = st.tag(tokenized_text)
        print(classified_text)

    def store_model(self, model):
        data=model, df
        print("Model")
        pickle.dump(data, open(self.filenamestore, 'wb'))

    def Train(self):
        X,y=self.preprocess_data()
        X_train, X_test, y_train, y_test = model_selection.train_test_split(X, y,test_size=0.01, random_state=42)
        ####### naive bayes #############
        #clf=MultinomialNB()
        ####### Random forest ###########
        clf = RandomForestClassifier(n_estimators=200,min_samples_split=2,min_samples_leaf=1,max_depth=800, random_state=10,class_weight="balanced")
        intent_classifier=clf.fit(X_train, y_train)
        #print(intent_classifier)
        result = intent_classifier.score(X_train, y_train)
        print('Accuracy of the model is ', result)
        self.store_model(intent_classifier)
        return intent_classifier


obj = train_model("FAQ_Workday.csv","Latin.pickle")
obj.Train()
print(obj)
