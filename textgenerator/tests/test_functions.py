# -*- coding: utf-8 -*-
from textgenerator.functions import spintax
import unittest


class TestFunctions(unittest.TestCase):
    def test_simple_spintax(self):
        res = spintax(u'{разместился|расположен|находится}')
        self.assertTrue(res in [u'разместился', u'расположен', u'находится'])

    '''def test_include_spintax(self):
        res = spintax(
            u'{{ололо2|nlo1} разместился|{ололо2|nlo2} расположен|{ололо3|nlo3} находится}'
        )
        var_list = [
                u'ололо1 разместился',
                u'nlo1 разместился'
                u'ололо2 расположен',
                u'nlo2 расположен',
                u'ололо3 находится',
                u'nlo3 находится',
            ]

        self.assertTrue(res in var_list)'''
