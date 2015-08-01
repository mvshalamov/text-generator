# -*- coding: utf-8 -*-
from textgenerator.generator import Generator

if __name__ == '__main__':
    gen = Generator('tpl/settings.yaml')
    print gen.generate_text(
        ['Heading', 'Main', 'Heading'],
        {'city': u'Париж', 'distance': '11', 'name': u'Грант', 'type': u'Первый'}
    )

