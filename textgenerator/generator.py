# -*- coding: utf-8 -*-
import yaml
import random


from textgenerator.render import (
    render, get_tpl_include, get_sub_tpl_by_name, render_sub_tpl,
    choice_tpl_by_probability, validate_conditions,
    group_tpl_by_id
)
import textgenerator.functions as funcs


def load_yaml(path_to_tpl):
    with open(path_to_tpl, 'r') as tpl:
        data = tpl.read()

        return yaml.load(data)


class Generator(object):
    def __init__(self, settings_file, tpl_funcs=funcs):
        self.funcs = funcs
        settings = load_yaml(settings_file)

        self.templates = {}
        for name, path in settings.items():
            self.templates[name] = load_yaml(path)

    def _create_context(self, name_tpl, tpl_vars):
        context = {
            'funcs': self.funcs,
            'tpls': self.templates[name_tpl],
            'sub_tpls': self.templates.get('Sub', None),
            'tpl_vars': tpl_vars,
        }
        return context

    def generate_text(self, list_names, tpl_vars):
        """
        :param list_proposal: [heading, main, heading]
        """
        res = ''
        for name_tpl in list_names:
            context = self._create_context(name_tpl, tpl_vars)
            res += render(context)

        return res


if __name__ == '__main__':
    gen = Generator('tpl/settings.yaml')
    print gen.generate_text(
        ['Heading', 'Main', 'Heading'],
        {'city': u'Париж', 'distance': '10', 'name': u'Смоуг', 'type': u'Первый', 'per': u'40'}
    )



    print '???????????????????????????????????'
    print '???????????????????????????????????'
    print '???????????????????????????????????'
    print '???????????????????????????????????'
    first_proposal = load_yaml('tpl/heading.yaml')
    sub_tpl = load_yaml('tpl/sub.yaml')
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
        'tpl_vars': {'city': u'Париж', 'distance': '10', 'name': u'Смоуг', 'type': u'Первый', 'per': u'40'},
    }
    print render(context)

    print '!!!!!!!!!!!!!!!!!!!!!!'

    '''print validate_conditions("distance1 > 10 and distance1 < 20", {'distance1': 12})

    print '--------------'

    print sub_tpl

    group = group_tpl_by_id(sub_tpl[0]['values'], {'distance': 20})
    print '-----', choice_tpl_by_probability(sub_tpl[0]['values'], {'distance': 20})
    name = get_tpl_include(first_proposal[0]['values'][1]['value'])
    l_sub_tpl = get_sub_tpl_by_name(context['sub_tpls'], name[0])
    print '==______==', l_sub_tpl
    sub_tpl = choice_tpl_by_probability(l_sub_tpl['values'], context['tpl_vars'])
    print '>>>>>>', get_tpl_include(tpl)
    print '>>>>>>', render_sub_tpl(context, sub_tpl['value'])'''
