# -*- coding: utf-8 -*-
import copy
import re
import random

PATTERN_VAR = "<[^>\n]+>"
PATTERN_INCLUDE = "\[[^\]\n]+\]"


def get_sub_tpl_by_name(sub_tpl, name_tpl):
    for tpl in sub_tpl:
        if tpl['name'] == name_tpl:
            return copy.deepcopy(tpl)
    raise KeyError('not sub tpl name = %s' % name_tpl)


def get_text_patterns(tpl, patterns):
    result = re.finditer(patterns, tpl)
    vars = []
    for match in result:
        vars.append(match.group()[1:-1].replace(' ', ''))

    return vars


def insert_value_in_tpl(tpl, vars, pattern):
    pattern = re.compile(pattern)
    for r in vars:
        tpl = pattern.sub(r, tpl, 1)

    return tpl


def generate_text(context):
    main_tpls = choice_tpl_by_probability(context['tpls'], context['tpl_vars'])
    tpl = choice_tpl_by_probability(main_tpls['values'], context['tpl_vars'])['value']

    names_sub_tpl = get_text_patterns(tpl, PATTERN_INCLUDE)
    if names_sub_tpl and context['sub_tpls']:
        for name in names_sub_tpl:
            l_sub_tpl = get_sub_tpl_by_name(context['sub_tpls'], name)
            sub_tpl = choice_tpl_by_probability(l_sub_tpl['values'], context['tpl_vars'])
            render_sub_tpl = _render(sub_tpl['value'], context)
            tpl = spintax(insert_value_in_tpl(tpl, [render_sub_tpl], PATTERN_INCLUDE))

    return _render(tpl, context)


def _render(tpl, context):
    vars = get_text_patterns(tpl, PATTERN_VAR)
    render_vars = render_tpl_vars(vars, context)
    return spintax(insert_value_in_tpl(tpl, render_vars, PATTERN_VAR))


def _fabric_tplengine_functions(name_function, context):
    try:
        func = getattr(context['funcs'], name_function)
    except AttributeError:
        print "ERROR! not template function " + str(name_function)
        return None

    return func


def _parse_funcs_and_params(funcs_data):
    data_var = funcs_data.split('~')
    funcs = []
    variable = data_var.pop(0)
    for it in data_var:
        data = it.split(':')
        func_name = data.pop(0)
        funcs.append((func_name, data))

    return variable, funcs


def spintax(value):
    if isinstance(value, str):
        value = value.decode('utf8')
    delimiter = '|'
    while True:
        value, n = re.subn(
            '{([^{}]*)}',
            lambda m: random.choice(m.group(1).split(delimiter)),
            value
        )
        if n == 0:
            break
    return value


def render_tpl_vars(vars, context):
    res = vars[:]
    value_vars = context['tpl_vars']
    for i, tpl_var in enumerate(vars):
        var, funcs = _parse_funcs_and_params(tpl_var)

        if var in value_vars:
            render_var = _render_variables_with_funcs(value_vars[var], funcs, context)
            res[i] = render_var

    return res


def _render_variables_with_funcs(var_value, functions, context):
    if isinstance(var_value, str):
        var_value = var_value.decode('utf-8')
    value = var_value
    for func in functions:
        tpl_func = _fabric_tplengine_functions(func[0], context)
        if tpl_func:
            value = tpl_func(value, *func[1])

    return value


def choice_tpl_by_probability(list_tpl, vars_tpl):
    """
    :param list_tpl: список шаблонов с вероятностями
    :param vars_tpl: словарь переменных шаблона
    :return: выбранный по вероятности шаблон
    """
    group = _group_tpl_by_id(list_tpl, vars_tpl)
    return _choice_from_group_probability(group, random.randint(1, group[1]))


def _group_tpl_by_id(list_tpl, vars_tpl):
    """
    :param list_tpl: [{'probability': int, ....},{'probability': int}]
    :param vars_tpl: словарь переменных шаблона
    :return: [(start_pos, end_position, {'probability': 10,}) -
    при вероятностях 10, 15 - получим [(0, 10, item) (10, 25, item)]
    второй параметр, суммарное кол-во вероятностей
    """
    probability_list = []
    max_num_probability = 0
    for item in list_tpl:
        if not item.get('conditions', False) or validate_conditions(item.get('conditions'), vars_tpl):
            probability = item.get('probability', 1)
            probability_list.append((max_num_probability, max_num_probability + probability, item))
            max_num_probability += probability

    return probability_list, max_num_probability


def _choice_from_group_probability(group_probability, num_probability):
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