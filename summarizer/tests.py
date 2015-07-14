#!/usr/bin/python
# coding=utf-8

import operator
import pytest

from .helpers import split_sentences, get_keywords,\
                        split_words, title_score, length_score
from .summarizer import get_score

SINGLE_SENTENCE = "This sentence will have 6 word's."

NEPAL_TITLE =\
"A short text on Nepal"

NEPAL_TEXT =\
'''
Nepal Nepal Nepal. Nepal is a wonderful country. This 
country is filled with a lot of amazing stuffs but people 
here are kinda shitty. But it is hard to compare people here
to people in another country.
'''

BBC_TITLE =\
'''
Greece debt crisis: What's the deal?
'''

BBC_ARTICLE =\
'''
Greece has won conditional agreement to receive up to €86bn (£61bn; $95bn) over three years, although this is not yet in the bag.

But it has had to make substantial concessions in return - and the consequences for the Greek economy look set to be far-reaching.

What are the main areas of economic reform stipulated by the deal?

In a nutshell: taxation, pensions, the labour markets, banks and privatisation. 

The agreement refers to "the streamlining of the VAT system and the broadening of the tax base to increase revenue". It seems that more items will be subject to the country's top VAT rate of 23%, including restaurants, while popular holiday destinations in the Greek islands will no longer benefit from a lower VAT rate. Corporation tax will also go up, to 28%.

There will be "upfront measures to improve long-term sustainability of the pension system as part of a comprehensive reform programme". That means the retirement age will rise to 67 by the year 2022, while aid to the poorest pensioners will be phased out by the end of 2019.
Labour markets will be liberalised, as will shop opening hours, with "rigorous reviews and modernisation of collective bargaining, industrial action and, in line with the relevant EU directive and best practice, collective dismissals". The Greek government is sternly warned that the country's past approach is "not compatible with the goals of promoting sustainable and inclusive growth".
Greece must "adopt the necessary steps to strengthen the financial sector". This means taking tougher action on non-performing loans and strengthening banking governance, including "eliminating any possibility for political interference, especially in appointment processes". In fact, the deal calls for a specific programme for "de-politicising the Greek administration".
This is one of the most far-reaching aspects of the deal. The text of the summit statement says: "Valuable Greek assets will be transferred to an independent fund that will monetise the assets through privatisations and other means."

It says the fund will be established in Greece and managed by the Greek authorities, but "under the supervision of the relevant European institutions" - that is, the European Central Bank and the European Commission, which, along with the International Monetary Fund, have been supervising Greek finances throughout the crisis.

In effect, this is being seen as a trust fund outside the control of the Greek government, which can cherry-pick Greek assets and dispose of them in order to repay the country's debts.

The summit document quotes a figure of €50bn for the value of the fund. Of that, half will go towards recapitalising the country's cash-strapped banks, whose health - or lack of it - has been so much under scrutiny in recent months.

A quarter of the proceeds of the fund will be used for reducing Greece's debt-to-GDP ratio, while the remaining €12.5bn will be used for investments in Greece.

'''


def check_numerical(x):
    if isinstance(x, (int, long, float, complex)):
        return True
    return False


def greater(val1, val2):
    if not check_numerical(val1) or not check_numerical(val2):
        raise TypeError("Both input parameters have to be numeric")
    if val1 > val2:
        return True 
    return False 


def test_check_numerical():
    assert check_numerical(2) == True 
    assert check_numerical("simpsons") == False 


def test_greater():
    assert greater(2, 5) == False 
    assert greater(5, 2) == True
    with pytest.raises(TypeError):
        greater("simpsons", "family guy")


def test_split_sentences():
    original = ''.join(['If this function works, I will have four sentences. ',
        "This is will be the first sentence. ", "This will be the second. ",
        "And, this one is the third of course."])
    output = split_sentences(original)
    assert len(output) == 4


def test_split_words():
    output = split_words(SINGLE_SENTENCE)
    assert len(output) == 6


def test_get_keywords():
    '''
    This function gets keywords based on frequency.
    '''
    output = get_keywords(NEPAL_TEXT)
    output =  sorted(output, key=output.get, reverse=True)
    top_3_output = output[:3]
    assert top_3_output == ['nepal', 'people', 'country']


def test_title_score():
    '''
    This test should give higher score for more relevant sentence
    and title 
    '''
    score_more = title_score("England queen visits Nepal".split(" "), "England queen visits India too".split(" "))
    score_less = title_score("England queen visits Nepal".split(" "), "England lost the world cup finale to another team".split(" "))
    assert greater(score_more, score_less) == True


def test_length_score():
    assert length_score(["england","queen","visit","water","prohect"]) == 0.25   



def test_get_score():
    '''
    This function tests score for sentence from the text 
    '''
    title = NEPAL_TITLE
    text = NEPAL_TEXT
    sentences = split_sentences(text)
    keys_ = get_keywords(text)
    title_words = split_words(title)
    highest_expected_sentence = u'Nepal Nepal Nepal.'
    second_expected_sentence = u'Nepal is a wonderful country.'
    sentence_weights = get_score(sentences, title_words, keys_)
    print(sentence_weights[highest_expected_sentence])

    assert greater(sentence_weights[highest_expected_sentence], sentence_weights[second_expected_sentence]) == True


def test_summarize():
    from .summarizer import summarize
    title = BBC_TITLE
    article = BBC_ARTICLE
    assert len(summarize(title, article, 11)) == 11
    np_title = NEPAL_TITLE
    np_text = NEPAL_TEXT
    assert summarize(np_title, np_text, 3)[0] == 'Nepal Nepal Nepal.'
