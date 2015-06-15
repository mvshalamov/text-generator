# -*- coding: utf-8 -*-
import yaml

from textgenerator.engine import generate_text
import textgenerator.tpl_functions as funcs


class Generator(object):
    def __init__(self, settings_file, tpl_funcs=funcs):
        self.funcs = funcs
        settings = self.load_yaml(settings_file)

        self.templates = {}
        for name, path in settings.items():
            self.templates[name] = self.load_yaml(path)

    def load_yaml(self, path_to_tpl):
        with open(path_to_tpl, 'r') as tpl:
            data = tpl.read()

            return yaml.load(data)

    def _create_context(self, name_tpl, tpl_vars):
        context = {
            'funcs': self.funcs,
            'tpls': self.templates[name_tpl],
            'sub_tpls': self.templates.get('Sub', None),
            'tpl_vars': tpl_vars,
        }
        return context

    def generate_text(self, list_names, tpl_vars):
        res = []
        for name_tpl in list_names:
            context = self._create_context(name_tpl, tpl_vars)
            res.append(generate_text(context))

        return ' '.join(res)

    def igenerate_text(self, list_names, tpl_vars):
        for name_tpl in list_names:
            context = self._create_context(name_tpl, tpl_vars)
            yield generate_text(context)
