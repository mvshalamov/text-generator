# -*- coding: utf-8 -*-
import unittest

import textgenerator.tpl_functions as funcs

from textgenerator.engine import (
    get_text_patterns, PATTERN_INCLUDE, PATTERN_VAR,
    spintax, insert_value_in_tpl, _parse_funcs_and_params, render_tpl_vars,
    parse_conditions, replace_var_conditions, execute_conditions
)


class TestEngine(unittest.TestCase):
    def setUp(self):
        self.context = {
            'funcs': funcs,
            'tpls': [],
            'sub_tpls': [],
            'tpl_vars': {'name': u'имя', 'type': u'тип'},
        }

    def test_simple_spintax(self):
        res = spintax(u'{разместился|расположен|находится}')
        self.assertTrue(res in [u'разместился', u'расположен', u'находится'])

    def test_get_text_patterns(self):
        str1 = u"<type~inflect_case:gent~lower> sfsdfsdf <name>"
        res1 = get_text_patterns(str1, PATTERN_VAR)
        self.assertEqual([u'type~inflect_case:gent~lower', u'name'], res1)

        str2 = u"<type~inflect_case:gent~lower> sfsdfsdf [name]"
        res2 = get_text_patterns(str2, PATTERN_INCLUDE)
        self.assertEqual([u'name'], res2)

    def test_insert_value_in_tpl(self):
        str1 = u"<type~inflect_case:gent~lower> test"
        res1 = insert_value_in_tpl(str1, ['OLOLO'], PATTERN_VAR)
        self.assertEqual('OLOLO test', res1)

        str2 = u"[name] test"
        res2 = insert_value_in_tpl(str2, ['OLOLO'], PATTERN_INCLUDE)
        self.assertEqual('OLOLO test', res2)

    def test_parse_fincs_and_params(self):
        str1 = u'city~inflect_case:gent~capfirst'
        res = _parse_funcs_and_params(str1)
        self.assertEqual((u'city', [(u'inflect_case', [u'gent']), (u'capfirst', [])]), res)

    def test_render_tpl_vars(self):
        data = [u'type~inflect_case:nomn~lower', u'name']
        res = render_tpl_vars(data, self.context)
        self.assertEqual([u'тип', u'имя'], res)

    def test_parse_conditions(self):
        conditions = u'distance1 > 10 and distance1 < 20'
        self.assertEqual(
            ['distance1', '>', '10', 'and', 'distance1', '<', '20'],
            parse_conditions(conditions)
        )

    def test_replace_var_conditions(self):
        parse_cond = ['distance1', '>', '10', 'and', 'distance1', '<', '20']
        self.assertEqual(
            [10, '>', '10', 'and', 10, '<', '20'],
            replace_var_conditions(parse_cond, {'distance1': 10})
        )

    def test_execute_conditions(self):
        conditions = [10, '>', '10', 'and', 10, '<', '20']
        self.assertEqual(
            False,
            execute_conditions(conditions)
        )
