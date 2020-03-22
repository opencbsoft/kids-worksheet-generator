import itertools
import random
from core.utils import Generator


class Main(Generator):
    name = 'Fill the missing number'
    years = [3, 4, 5]
    directions = 'Completeaza cu cifra care lipseste.'
    template = 'generators/fill_the_number.html'

    def generate_data(self):
        if self.extra:
            until = int(self.extra)
        else:
            until = 10
        result = []
        number_array = []
        for i in range(1, until + 1):
            number_array.append(i)
        number_options = []
        for j in range(0, 7):
            for i in range(0, 4):
                selected = number_array[j:j + 4]
                selected[i] = 0
                number_options.append(selected)

        for L in range(0, len(number_options) + 1):
            for subset in itertools.combinations(number_options, 4):
                result.append(subset)
        self.data = result
        return result

    def get_context_data(self, iteration):
        context = super(Main, self).get_context_data(iteration)
        context['shapes'] = random.sample([1, 2, 3, 4, 5], 4)
        context['items'] = random.choice(context['items'])
        return context
