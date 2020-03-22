import string
import random
from core.utils import Generator


class Main(Generator):
    name = 'Fill what comes next'
    years = [4, 5]
    directions = 'Decupeaza si lipeste imaginea care urmeaza.'
    template = 'generators/fill_pattern_easy.html'
    content_height = 1200
    icons_folder = ['food', 'animals']

    def generate_data(self):
        patterns = [[0, 0, 1], [0, 1, 0], [0, 1, 1], [0, 1, 2], [1, 0, 0]]
        results = []
        for i in range(self.count):
            final_patterns = []
            missing = []
            for pattern in random.sample(patterns, 4):
                complete_pattern = pattern+pattern[:2]
                missing.append(complete_pattern[-1])
                final_patterns.append(pattern+pattern[:1])
            available_icons = [random.sample(self.icons, 3) for i in range(4)]
            missing_icons = []
            for idx in range(0, len(missing)):
                missing_icons.append(available_icons[idx][missing[idx]])
            random.shuffle(missing_icons)
            results.append({'patterns': final_patterns, 'missing': missing_icons, 'icons': available_icons})
        self.data = results
        return results

    def get_context_data(self, iteration):
        context = super(Main, self).get_context_data(iteration)
        context['items'] = context['items'][iteration]
        return context
