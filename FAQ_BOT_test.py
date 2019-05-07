# -*- coding: utf-8 -*-
"""
Created on Wed Jan  9 11:54:57 2019

@author: BARIAR-CONT
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from builtins import open
from builtins import str
# etc., as needed

from future import standard_library
standard_library.install_aliases()
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer, TfidfTransformer
from sklearn import preprocessing
import pandas as pd
import numpy as np
from textblob import TextBlob
import pickle
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import string
import re
import os
import argparse

class test_model:

    def __init__(self, modelname):
        self.model = modelname
        print(modelname)
        self.intent_classifier, self.df = self.load_model_with_preprocess()
        self.bow_transformer = TfidfVectorizer(analyzer=self.remove_stop_words_and_lemmas,ngram_range=(1,5)).fit(self.df['question'])
        self.messages_bow = self.bow_transformer.transform(self.df['question'])


    def load_model_with_preprocess(self):
        loaded_model = pickle.load(open(self.model, 'rb'),encoding='latin1')
        return loaded_model

    def split_into_tokens(self, message):
        message = str(message)  # convert bytes into proper unicode
        message = TextBlob(message).correct()
        return TextBlob(message).words

    def split_into_lemmas(self, message):
        message = str(message).lower()
        words = TextBlob(message).words
        #print(words)
        # for each word, take its "base form" = lemma
        return [word.lemma for word in words]

    def remove_stop_words_and_lemmas(self,message):
        message = str(re.sub(r'[^\x00-\x7F]+',' ', message)).lower()
        #stop_words = set(stopwords.words('english'))
        #translator = str.maketrans("", "", string.punctuation)
        ##strip_digits=strip_puct.translate(string.maketrans("", ""), string.digits)

        word_tokens = word_tokenize(message)
        stop = set(stopwords.words('english'))
        stop_m = [i for i in word_tokens if str(i).lower() not in stop]
        lemmatizer = WordNetLemmatizer()
        filtered_sentence = [lemmatizer.lemmatize(w) for w in stop_m] # if not w in stop_words]
        return filtered_sentence

    def predict_class(self, ipdata):
        ipdata_bow = self.bow_transformer.transform([ipdata])
        print(ipdata_bow)
        tfidf_transformer = TfidfTransformer().fit(self.messages_bow)
        ipdata_tfidf = tfidf_transformer.transform(ipdata_bow)
        prediction = self.intent_classifier.predict(ipdata_tfidf)
        print(prediction)
        '''try:
            print(self.le.inverse_transform(type(prediction[0])))
        except Exception as exp:
            print(exp,exp.with_traceback())'''
        probability=self.intent_classifier.predict_proba(ipdata_tfidf)
        prob_per_class_dictionary = dict(zip(self.intent_classifier.classes_, probability[0]))
        print("\n\n\n")
        print(prediction)
        return prediction, prob_per_class_dictionary



