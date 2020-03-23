# Kids worksheet generator
During the COVID-19 pandemic kids are stuck indoor, so this is a little help for the parents to keep the kids active.

## Steps required to create new generators
1. create a new file in application/core/generators/<new_generator>.py
2. Import the base Generator class 
```python
from core.utils import Generator
```

3. Override the generate_data function
```python
class Main(Generator):
    name = 'Circle the group with more'
    years = [3, 4, 5]
    directions = 'Incercuieste grupul care contine mai multe imagini'
    template = 'generators/circle_the_group_with_more.html'
    icons_folder = ['food', 'animals']

    def generate_data(self):
        results = []
        self.data = results
        return results
    
    def get_context_data(self, iteration):
        #  If you generate for all the papers required the data, then you can select the items only based on the iteration
        context = super(Main, self).get_context_data(iteration)
        context['items'] = context['items'][iteration]
        return context
```

4. Create your HTML template inside core/templates/generators/
```jinja2
{% extends 'base.html' %}
{% block content %}
    {% for item in items %}
        <div style="padding-top:10px;height: 320px;position: relative">
            <div style="float:left;position: relative; width: 508px; height: 320px; border: 2px solid #000000;">
            {% for i in item.value1 %}
                <div style="width: 100px; height: 100px;float: left;margin-top: 5px;margin-left: 20px;">
                    <img src="{{ path }}{{ item.icon1 }}" />
                </div>
            {% endfor %}
            </div>
            <div style="float:left;position: relative; width: 508px; height: 320px; border: 2px solid #000000;margin-left: 10px;">
            {% for i in item.value2 %}
                <div style="width: 100px; height: 100px;float: left;margin-top: 5px;margin-left: 20px;">
                    <img src="{{ path }}{{ item.icon2 }}" />
                </div>
            {% endfor %}
            </div>
            <div class="clearfix"></div>
        </div>
    {% endfor %}

{% endblock %}
```