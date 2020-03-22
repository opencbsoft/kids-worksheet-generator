import itertools
import random
from core.utils import Generator


class Main(Generator):
    name = 'Connect with the other half'
    years = [3, 4]
    directions = 'Traseaza o linie de la fiecare imagine pana la jumatatea ei.'
    template = 'generators/connect_the_other_half.html'
    icons_folder = ['food', 'animals']

    def get_context_data(self, iteration):
        context = super(Main, self).get_context_data(iteration)
        selected_icons = random.sample(self.icons, 5)
        left_part = [i for i in selected_icons]
        right_part = [i for i in selected_icons]
        random.shuffle(right_part)
        context['items'] = []
        for i in range(5):
            context['items'].append((left_part[i], right_part[i]))
        return context
