# -*- coding: utf-8 -*-
import pymorphy2
from pymorphy2.shapes import restore_capitalization
import random
import re
from textgenerator.render import get_sub_tpl

morph = pymorphy2.MorphAnalyzer()


def _take_word_form(word, form):
    try:
        res = restore_capitalization(
            morph.parse(word)[0].inflect({form}).word,
            word
        )
        return res
    except Exception:
        for it in morph.parse(word):
            n = it.inflect({form})
            if n:
                return n.word
        print u'WARNING: unable to parse word "{}". Falling back to its original value'.format(word)
    return word


def inflect_case(value, case):
    value = unicode(value).split(' ')
    return' '.join([_take_word_form(v.title(), case) for v in value])


def lower(value):
    return value.lower()


def render_sub_tpl(value, tpl_name):
    pass

