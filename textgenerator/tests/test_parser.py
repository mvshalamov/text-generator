# -*- coding: utf-8 -*-
from textgenerator.parser import (
    group_tpl_by_id, parse_conditions, replace_var_conditions, execute_conditions
)
import unittest


class TestParser(unittest.TestCase):
    def test_group_tpl_by_id(self):
        dict1 = {'probability': 10}
        dict2 = {}
        var = [dict1, dict2]
        self.assertEqual([(0, 10, dict1), (10, 11, dict2)], group_tpl_by_id(var)[0])
        self.assertEqual(11, group_tpl_by_id(var)[1])

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