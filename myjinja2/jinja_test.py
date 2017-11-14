# -*- coding: utf-8 -*-

from jinja2 import Template, Environment, PackageLoader


# template = Template('Hello {{name}}!')
# print template.render(name='John Doe')

env = Environment(loader=PackageLoader('myjinja2', 'templates'))
template = env.get_template('mytemplate.html')
print template.render(the='variables', go='here')
