# -*- coding: utf-8 -*-
import yaml
import random
from textgenerator.parser import (
    choice_tpl_by_probability, validate_conditions,
    group_tpl_by_id
)

from textgenerator.render import render, get_tpl_include, get_sub_tpl_by_name
import textgenerator.functions as funcs


def load_proposal(path_to_tpl):
    with open(path_to_tpl, 'r') as tpl:
        data = tpl.read()

        return yaml.load(data)

if __name__ == '__main__':
    first_proposal = load_proposal('tpl/ex.yaml')
    sub_tpl = load_proposal('tpl/sub.yaml')
    print first_proposal
    #print choice_tpl_by_probability(first_proposal)
    print '---------------------'
    print first_proposal[0]['values']
    #print choice_tpl_by_probability(first_proposal[0]['values'])
    #print group_tpl_by_id(first_proposal[0]['values'])
    print '---------------------'
    tpl = first_proposal[0]['values'][1]['value']
    '''vars = get_tpl_variables(tpl)
    print fabric_tplengine_functions('sdfsdfsdfsdfsdsdf')
    render = render_tpl_vars(vars, {'city': u'Париж', 'distance': '10', 'name': u'Смоуг', 'type': u'Первый'})
    print render
    print render_tpl(tpl, render)'''
    context = {
        'funcs': funcs,
        'tpls': first_proposal,
        'sub_tpls': sub_tpl,
        'tpl_vars': {'city': u'Париж', 'distance': '10', 'name': u'Смоуг', 'type': u'Первый'},
    }
    print render(tpl, {'city': u'Париж', 'distance': '10', 'name': u'Смоуг', 'type': u'Первый'}, context)

    print '!!!!!!!!!!!!!!!!!!!!!!'

    print validate_conditions("distance1 > 10 and distance1 < 20", {'distance1': 12})

    print '--------------'

    print sub_tpl

    group = group_tpl_by_id(sub_tpl[0]['values'], {'distance': 20})
    print '-----', choice_tpl_by_probability(sub_tpl[0]['values'], {'distance': 20})
    name = get_tpl_include(first_proposal[0]['values'][1]['value'])
    print get_sub_tpl_by_name(context['sub_tpls'], name[0])
