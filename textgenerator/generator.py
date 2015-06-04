# -*- coding: utf-8 -*-
import yaml
import random
from textgenerator.parser import get_tpl_variables, render_tpl_vars, render_tpl, fabric_tplengine_functions


def load_proposal(path_to_tpl):
    with open(path_to_tpl, 'r') as tpl:
        data = tpl.read()

        return yaml.load(data)

if __name__ == '__main__':
    first_proposal = load_proposal('tpl/ex.yaml')
    tpl = first_proposal[0]['values'][1]['value']
    vars = get_tpl_variables(tpl)
    print fabric_tplengine_functions('sdfsdfsdfsdfsdsdf')
    render = render_tpl_vars(vars, {'city': u'Париж', 'distance': '10', 'name': u'Смоуг', 'type': u'Первый'})
    print render
    print render_tpl(tpl, render)
