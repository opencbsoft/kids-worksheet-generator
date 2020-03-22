import itertools
import random
from core.utils import Generator


class Main(Generator):
    name = 'Simple math addition'
    years = [4, 5]
    icons_folder = ['food', 'animals']
    directions = 'Aduna imaginile si scrie rezultatul in casuta.'
    template = 'generators/simple_math_addition.html'

    def generate_data(self):
        if self.extra:
            max_number = int(self.extra)
            if max_number > 10:
                max_number = 10
        else:
            max_number = 5
        numbers = []
        for i in range(1, max_number+1):
            numbers.append(i)
        result = []
        for subset in itertools.combinations(numbers, 2):
            if subset[0] + subset[1] <= max_number:
                result.append({'no1': subset[0], 'no2': subset[1], 'icon': random.choice(self.icons), 'range1': range(subset[0]), 'range2': range(subset[1])})
                result.append({'no2': subset[0], 'no1': subset[1], 'icon': random.choice(self.icons), 'range2': range(subset[0]), 'range1': range(subset[1])})
        self.data = result
        return result

    def get_context_data(self, iteration):
        context = super(Main, self).get_context_data(iteration)
        context['items'] = random.sample(context['items'], 4)
        return context

