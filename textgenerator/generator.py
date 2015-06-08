# -*- coding: utf-8 -*-
import yaml
import random
from textgenerator.parser import (
    get_tpl_variables, render_tpl_vars, render_tpl, fabric_tplengine_functions,
    choice_tpl_by_probability, parse_conditions, replace_var_conditions, execute_conditions,
    group_tpl_by_id
)


def load_proposal(path_to_tpl):
    with open(path_to_tpl, 'r') as tpl:
        data = tpl.read()

        return yaml.load(data)

if __name__ == '__main__':
    first_proposal = load_proposal('tpl/ex.yaml')
    print first_proposal
    print choice_tpl_by_probability(first_proposal)
    print '---------------------'
    print first_proposal[0]['values']
    print choice_tpl_by_probability(first_proposal[0]['values'])
    print group_tpl_by_id(first_proposal[0]['values'])
    print '---------------------'
    tpl = first_proposal[0]['values'][1]['value']
    vars = get_tpl_variables(tpl)
    print fabric_tplengine_functions('sdfsdfsdfsdfsdsdf')
    render = render_tpl_vars(vars, {'city': u'Париж', 'distance': '10', 'name': u'Смоуг', 'type': u'Первый'})
    print render
    print render_tpl(tpl, render)
    print '!!!!!!!!!!!!!!!!!!!!!!'
    tokens = parse_conditions("distance1 > 10 and distance1 < 20")
    tokens_cond = replace_var_conditions(tokens, {'distance1': 10})
    print tokens_cond
    print execute_conditions(tokens_cond)
