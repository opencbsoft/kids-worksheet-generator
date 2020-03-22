import string
import random
from core.utils import Generator


class Main(Generator):
    name = 'Rainbow counting'
    years = [3, 4]
    directions = 'Numara punctele si incercuieste numarul corect. Dupa aceea coloreaza curcubeele.'
    template = 'generators/rainbow_counting.html'

    def generate_data(self):
        print('generated')
        min_vertical = 260
        max_vertical = 320
        min_left_horiz = 50
        max_left_horiz = 160
        min_right_horiz = 310
        max_right_horiz = 430
        possible = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        items = []
        for j in range(self.count):
            selected_numbers = random.sample(possible, 6)
            sheet = []
            for item in selected_numbers:
                data = dict()
                data['correct'] = item
                wrong_item = item + random.randint(1, 3)
                if wrong_item > 10:
                    wrong_item = item - random.randint(1, 3)
                data['wrong'] = wrong_item

                if random.randint(1, 2) == 1:
                    data['wrong'] = item
                    data['correct'] = wrong_item
                part2 = int(item / 2)
                if item % 2:
                    part2 += 1
                part1 = item - part2
                if part1 > 0:
                    data['points1'] = []
                    while len(data['points1']) < part1:
                        x = random.choice([i for i in range(min_left_horiz, max_left_horiz, 16)])
                        y = random.choice([i for i in range(min_vertical, max_vertical, 16)])
                        if (x, y) not in data['points1']:
                            data['points1'].append((x, y))
                if part2 > 0:
                    data['points2'] = []
                    while len(data['points2']) < part2:
                        x = random.choice([i for i in range(min_right_horiz, max_right_horiz, 16)])
                        y = random.choice([i for i in range(min_vertical, max_vertical, 16)])
                        if (x, y) not in data['points2']:
                            data['points2'].append((x, y))
                sheet.append(data)
            items.append(sheet)
        self.data = items
        return items

    def get_context_data(self, iteration):
        context = super(Main, self).get_context_data(iteration)
        context['items'] = context['items'][iteration]
        return context
