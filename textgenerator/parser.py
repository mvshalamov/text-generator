# -*- coding: utf-8 -*-
import re
import textgenerator.functions
import random

PATTERN = "<[^>\n]+>"


def get_tpl_variables(tpl):
    """
    :param tpl: шаблон предложения
    :return: паттерны (пеоеменные и функции, которые к ним применяются)
    """
    result = re.finditer(PATTERN, tpl)
    vars = []
    for match in result:
        vars.append(match.group()[1:-1].replace(' ', ''))

    return vars


def _parse_funcs_and_params(funcs_data):
    """
    получаем строки шаблона с функциями и параметрами
    выдаем список функций и их параметров
    ex: city~inflect_case:gent~capfirst
    return: variable, funcs with params
    """
    data_var = funcs_data.split('~')
    print '=-=-=', data_var
    funcs = []
    variable = data_var.pop(0)
    for it in data_var:
        data = it.split(':')
        func_name = data.pop(0)
        funcs.append([(func_name, data)])

    return variable, funcs


def _render_variables_with_funcs(var_value, functions):
    """
    :param var_value: значение переменной шаблона
    :param functions: функции пременяемые к переменной и их параметры
    :return: значение переменной после применения к ним функций
    """
    value = var_value
    for func in functions:
        tpl_func = fabric_tplengine_functions(func[0][0])
        if tpl_func:
            value = tpl_func(value, *func[0][1])

    return value


def render_tpl_vars(vars, value_vars):
    """
    :param vars:[u'type~inflect_case:gent~lower', u'name', u'distance', u'city~inflect_case:gent~capfirst']
    :param value_vars: значения переменных, напр.: {'type': Первый}
    :return: значения переменных готовых к вставке в шаблон
    """
    print '-======', vars
    res = vars[:]
    for i, tpl_var in enumerate(vars[:]):
        var, funcs = _parse_funcs_and_params(tpl_var)

        if var in value_vars:
            render_var = _render_variables_with_funcs(value_vars[var], funcs)
            res[i] = render_var

    return res


def render_tpl(proposal, render_vars):
    """
    :param proposal: предложение в которое нужно подставить полученные значения
    :param render_vars: переменные которые нужно подставить
    :return: готовое предложение
    """
    pattern = re.compile(PATTERN)
    res = proposal
    for r in render_vars:
        res = pattern.sub(r, res, 1)

    return textgenerator.functions.spintax(res)


def fabric_tplengine_functions(name_function):
    """
    :param name_function:
    :return: function
    """
    try:
        func = getattr(textgenerator.functions, name_function)
    except AttributeError:
        print "ERROR! not template function " + str(name_function)
        return None

    return func


def choice_tpl_by_probability(list_tpl):
    """
    :param list_tpl: список шаблонов с вероятностями
    :return: выбранный по вероятности шаблон
    """
    probability_list = []
    position = 0
    for item in list_tpl:
        probability = item.get('probability', 1)
        probability_list.append((position, position + probability, item))
        position += probability

    if position:
        choice = random.randint(1, position)
        for start_prob, end_prob, item in probability_list:
            if start_prob < choice <= end_prob:
                print choice, position, item
                return item


def group_tpl_by_id(list_tpl):
    """
    :param list_tpl: [{'probability': int, ....},{'probability': int}]
    :return: [(start_pos, end_position, {'probability': 10,}) -
    при вероятностях 10, 15 - получим [(0, 10, item) (10, 25, item)]
    второй параметр, суммарное кол-во вероятностей
    """
    probability_list = []
    max_num_probability = 0
    for item in list_tpl:
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