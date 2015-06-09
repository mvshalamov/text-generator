# -*- coding: utf-8 -*-
import copy
import re
import random


def get_sub_tpl_by_name(sub_tpl, name_tpl):
    for tpl in sub_tpl:
        if tpl['name'] == name_tpl:
            return copy.deepcopy(tpl)
    raise KeyError('not sub tpl name = %s' % name_tpl)


def render(tpl, vars_tpl, context):
    """
    :param tpl: шаблон предложения
    :param vars_tpl: список переменных и их значений для шаблона
    :return: отрендеренное предложение
    """

    vars = get_tpl_variables(tpl)
    render_vars = render_tpl_vars(vars, vars_tpl, context)
    return render_tpl(tpl, render_vars)


PATTERN_VAR = "<[^>\n]+>"
PATTERN_INCLUDE = "\[[^\]\n]+\]"


def get_tpl_include(tpl):
    """
    :param tpl: шаблон предложения
    :return: паттерны (пеоеменные и функции, которые к ним применяются)
    """
    result = re.finditer(PATTERN_INCLUDE, tpl)
    vars = []
    for match in result:
        vars.append(match.group()[1:-1].replace(' ', ''))

    return vars


def fabric_tplengine_functions(name_function, context):
    """
    :param name_function:
    :return: function
    """
    if name_function == 'render_sub_tpl':
        return render_sub_tpl(context)
    try:
        func = getattr(context['funcs'], name_function)
    except AttributeError:
        print "ERROR! not template function " + str(name_function)
        return None

    return func


def render_sub_tpl(context):
    """
    добавляем подшаблоны в основнйо шаблон
    :param context:
    :return:
    """
    print 'context', context
    a = 1

    def add_to_tpl(value):
        sub_tpl = get_sub_tpl(context['sub_tpls'], value)
        ren = render(sub_tpl, context['tpl_vars'], context)
        return value + str(a)

    return add_to_tpl


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


def render_tpl_vars(vars, value_vars, context):
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
            render_var = _render_variables_with_funcs(value_vars[var], funcs, context)
            res[i] = render_var

    return res


def get_tpl_variables(tpl):
    """
    :param tpl: шаблон предложения
    :return: паттерны (пеоеменные и функции, которые к ним применяются)
    """
    result = re.finditer(PATTERN_VAR, tpl)
    vars = []
    for match in result:
        vars.append(match.group()[1:-1].replace(' ', ''))

    return vars


def render_tpl(proposal, render_vars):
    """
    :param proposal: предложение в которое нужно подставить полученные значения
    :param render_vars: переменные которые нужно подставить
    :return: готовое предложение
    """
    pattern = re.compile(PATTERN_VAR)
    res = proposal
    for r in render_vars:
        res = pattern.sub(r, res, 1)

    return spintax(res)


def _render_variables_with_funcs(var_value, functions, context):
    """
    :param var_value: значение переменной шаблона
    :param functions: функции пременяемые к переменной и их параметры
    :return: значение переменной после применения к ним функций
    """
    value = var_value
    for func in functions:
        tpl_func = fabric_tplengine_functions(func[0][0], context)
        if tpl_func:
            value = tpl_func(value, *func[0][1])

    return value


def get_sub_tpl(tpl, name_tpl):
    for it in tpl:
        if it['name'] == name_tpl:
            return copy.deepcopy(it)