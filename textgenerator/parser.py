# -*- coding: utf-8 -*-
import re
import textgenerator.functions

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