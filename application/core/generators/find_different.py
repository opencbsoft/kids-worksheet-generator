import itertools
import random
from core.utils import Generator


class Main(Generator):
    name = 'Find the different one'
    years = [2, 3, 4]
    directions = 'Gaseste si incercuieste imaginea diferita.'
    template = 'generators/find_different.html'
    icons_folder = ['food', 'animals']

    def generate_data(self):
        results = []
        for subset in itertools.combinations(self.icons, 2):
            line = [subset[1]]
            for x in range(0, 3):
                line.append(subset[0])
            random.shuffle(line)
            results.append(line)
        self.data = results
        return results

    def get_context_data(self, iteration):
        context = super(Main, self).get_context_data(iteration)
        context['items'] = random.sample(context['items'], 5)
        return context
