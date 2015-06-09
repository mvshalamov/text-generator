# -*- coding: utf-8 -*-
import re
import random
import copy


def choice_tpl_by_probability(list_tpl, vars_tpl):
    """
    :param list_tpl: список шаблонов с вероятностями
    :param vars_tpl: словарь переменных шаблона
    :return: выбранный по вероятности шаблон
    """
    group = group_tpl_by_id(list_tpl, vars_tpl)
    return choice_from_group_probability(group, random.randint(1, group[1]))


def group_tpl_by_id(list_tpl, vars_tpl):
    """
    :param list_tpl: [{'probability': int, ....},{'probability': int}]
    :param vars_tpl: словарь переменных шаблона
    :return: [(start_pos, end_position, {'probability': 10,}) -
    при вероятностях 10, 15 - получим [(0, 10, item) (10, 25, item)]
    второй параметр, суммарное кол-во вероятностей
    """
    print '-=-=-=', list_tpl
    probability_list = []
    max_num_probability = 0
    for item in list_tpl:
        if not item.get('conditions', False) or validate_conditions(item.get('conditions'), vars_tpl):
            probability = item.get('probability', 1)
            probability_list.append((max_num_probability, max_num_probability + probability, item))
            max_num_probability += probability

    return probability_list, max_num_probability


def choice_from_group_probability(group_probability, num_probability):
    """
    :param group_probability: результат group_tpl_by_id
    :param num_probability: выпавшая вероятность от 1 до результат group_tpl_by_id[1]
    ex: choice = random.randint(1, group_tpl_by_id[1])
    :return: выбранный элемент
    """
    probability_list, max_num_probability = group_probability
    if max_num_probability:
        for start_prob, end_prob, item in probability_list:
            if start_prob < num_probability <= end_prob:
                print num_probability, num_probability, item
                return item


def parse_conditions(tpl_conditions):
    """
    :param tpl_conditions: distance > 10 and distance < 20
    :return: ['distance', '>', '10', 'and', 'distance', '<', '20']
    """
    PATTERN_FOR_TOKENS = '>|>=|<|<=|==|or|and|[\w\d]+'
    tokens_compile = re.compile(PATTERN_FOR_TOKENS)
    tokens = tokens_compile.findall(tpl_conditions)
    return tokens


def replace_var_conditions(token_conditions, vars_data):
    """
    :param token_conditions: ['distance', '>', '10', 'and', 'distance', '<', '20']
    :param vars_data: {'distance': 10}
    :return: [10, '>', '10', 'and', 10, '<', '20']
    """
    tokens = token_conditions[:]
    print tokens, vars_data
    for i, token in enumerate(tokens):
        if token in vars_data:
            tokens[i] = vars_data[token]

    return tokens


def execute_conditions(conditions):
    """
    :param conditions: [10, '>', '10', 'and', 10, '<', '20']
    :return: True or False conditions
    """
    cond = ' '.join([str(it) for it in conditions])
    try:
        return eval(cond)
    except SyntaxError:
        return False


def validate_conditions(tpl_conditions, data_conditions):
    tokens_conditions = parse_conditions(tpl_conditions)
    conditions_for_execute = replace_var_conditions(tokens_conditions, data_conditions)
    return execute_conditions(conditions_for_execute)
