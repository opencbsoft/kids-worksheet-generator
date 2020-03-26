import itertools
import random
from core.utils import Generator


class Main(Generator):
    name = 'Match image with shadow'
    years = [4, 5]
    icons_folder = ['food', 'animals']
    directions = 'Uneste imaginea corecta cu umbra ei'
    template = 'generators/match_image_with_shadow.html'

    def generate_data(self):
        results = []
        for i in range(self.count):
            icons = random.sample(self.icons, 6)
            used_icons = icons.copy()
            line = []
            for j in range(len(icons)):
                selected_icon = random.choice(used_icons)
                if selected_icon == icons[j]:
                    selected_icon = random.choice(used_icons)
                used_icons.remove(selected_icon)
                line.append({'left': icons[j], 'right': selected_icon})
            results.append(line)
        self.data = results
        return results

    def get_context_data(self, iteration):
        context = super(Main, self).get_context_data(iteration)
        context['items'] = context['items'][iteration]
        return context
