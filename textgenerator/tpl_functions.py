# -*- coding: utf-8 -*-
import pymorphy2

MORPHY = pymorphy2.MorphAnalyzer()


def _take_word_form(word, form):

    for item in MORPHY.parse(word):
        word_form = item.inflect({form})
        if word_form:
            return word_form.word

    return word


def inflect_case(value, case):
    value = unicode(value).split(' ')
    return' '.join([_take_word_form(v.title(), case) for v in value])


def lower(value):
    return value.lower()


def capfirst(value):
    return value.title()
