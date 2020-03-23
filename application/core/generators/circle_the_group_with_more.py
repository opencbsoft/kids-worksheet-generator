import string
import random
from core.utils import Generator


class Main(Generator):
    name = 'Circle the group with more'
    years = [3, 4, 5]
    directions = 'Incercuieste grupul care contine mai multe imagini'
    template = 'generators/circle_the_group_with_more.html'
    icons_folder = ['food', 'animals']

    def generate_data(self):
        if self.extra:
            max_value = int(self.extra)
        else:
            max_value = 8

        values = [i for i in range(1, max_value+1)]
        results = []
        while len(results) != self.count:
            result = []
            for i in range(4):
                value = random.sample(values, 2)
                value = (value[0], value[1])
                if value not in results and value[0] != value[1]:
                    result.append({'value1': range(value[0]), 'value2': range(value[1]), 'icon1': random.choice(self.icons), 'icon2': random.choice(self.icons)})
            results.append(result)
        self.data = results
        return results

    def get_context_data(self, iteration):
        context = super(Main, self).get_context_data(iteration)
        context['items'] = context['items'][iteration]
        return context
