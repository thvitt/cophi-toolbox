from jinja2 import Template

with open('index.html.jinja') as f:
    tmpl = Template(f.read())
print(tmpl.render(title = 'Demonstrator', item_list = ["Erster Punkt", "Zweiter Punkt", "Dritter Punkt"]))
