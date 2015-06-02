import yaml
import random
import re
import functions


def load_proposal(path_to_tpl):
    with open(path_to_tpl, 'r') as tpl:
        data = tpl.read()

        return yaml.load(data)


def get_tpl_variables(tpl):
    result = re.finditer("<[^>\n]+>", tpl)
    vars = []
    for match in result:
        vars.append((match.group()[1:-1], match.span()))

    return vars


def render_vars(vars, value_vars):
    for tpl_var in vars[:]:
        data_var = tpl_var[0].split('~')
        var = data_var.pop(0)
        funcs = []
        for it in data_var:
            data = it.split(':')
            print '----------'
            print data
            print '----------'
            variable = data.pop(0)
            funcs.append([(variable, data)])
        render_var = var
        if data_var in value_vars:
            for func, func_vars in funcs:
                func = fabric_tplengine_functions(func)
                if func:
                    render_var = func()
        print '==========='
        print var, funcs
        print '==========='


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


def fabric_tplengine_functions(name_function):
    try:
        func = getattr(functions, name_function)
    except AttributeError:
        print "ERROR! not template function " + str(name_function)
        return None

    return func


if __name__ == '__main__':
    first_proposal = load_proposal('tpl/ex.yaml')
    tpl = first_proposal[0]['values'][1]['value']
    print spintax(tpl)
    vars = get_tpl_variables(tpl)
    print fabric_tplengine_functions('sdfsdfsdfsdfsdsdf')
    render_vars(vars, {'city': u'Париж', 'distance': '10', 'name': u'Смоуг', 'type': u'Первый'})