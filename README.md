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

4. Create your HTML template inside core/templates/generators/<new_generator>.html
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

5. Generate your pdf page using the following command:
```shell script
./manage.py generate -g <new_generator> --count 1
```
6. See your generated pdf in the <MEDIA_ROOT>/generated/<new_generator>/generated0.pdf


## Ideeas of new generators:
- [Maze generator](https://github.com/boppreh/maze)
- [Cut and sort the numbers 1-10](https://cdn.education.com/worksheet-image/917702/ordering-numbers-10.gif)
- [Match wearing with the weather seasons] (https://cdn.education.com/worksheet-image/128198/weather-wear-matching-weather-seasons.png)
- Match the icon with it's shadow
- 

## Thanks to
[freepik](https://www.freepik.com) - icons

[Website template](https://www.creative-tim.com/product/argon-design-system) - Frontend 

[PidginHost](https://www.pidginhost.com) - hosting
