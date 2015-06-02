import pymorphy2

morph = pymorphy2.MorphAnalyzer()


def _take_word_form(word, form):
    for it in morph.parse(word):
        n = it.inflect({form})
        if n:
            return n.word
        print u'WARNING: unable to take inflection "{}" of word "{}".'.format(form, word)
    print u'WARNING: unable to parse word "{}". Falling back to its original value'.format(word)
    return word


def inflect_case(value, case):
    value = unicode(value).split(' ')
    return' '.join([_take_word_form(v.title(), case) for v in value])