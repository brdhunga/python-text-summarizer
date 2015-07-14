#!/usr/bin/python
# coding=utf-8
from __future__ import division

from re import split as regex_split
from re import sub as regex_sub
from re import UNICODE as REGEX_UNICODE
from collections import Counter 

from .helpers import STOPWORDS, split_words, title_score,\
                        length_score, sentence_position, sbs, dbs,\
                        NO_OF_KEYWORDS, split_sentences, get_keywords


def get_score(sentences, title_words, keywords):
    '''
    This function gives weight to sentences based on
    various factors
    '''
    sentence_size = len(sentences)
    ranks = Counter()
    for i, s in enumerate(sentences):
        sentence = split_words(s)
        titleFeature = title_score(title_words, sentence)
        sentenceLength = length_score(sentence)
        sentencePosition = sentence_position(i+1, sentence_size)
        sbsFeature = sbs(sentence, keywords)
        dbsFeature = dbs(sentence, keywords)
        frequency = (sbsFeature + dbsFeature) / 2.0 * NO_OF_KEYWORDS

        #weighted average of scores from four categories
        totalScore = (titleFeature*1.5 + frequency*2.0 +
                      sentenceLength*1.0 + sentencePosition*1.0) / 4.0
        ranks[s] = totalScore
    return ranks


def summarize(title, text, no_of_sentences=5):
    summaries = []
    text = text.decode('utf-8')
    sentences = split_sentences(text)
    keys = get_keywords(text)
    titleWords = split_words(title)

    if len(sentences) <= 5:
        return sentences

    #score setences, and use the top 5 sentences
    ranks = get_score(sentences, titleWords, keys).most_common(no_of_sentences)
    print("the length is", len(ranks))
    for rank in ranks:
        summaries.append(rank[0])

    return summaries