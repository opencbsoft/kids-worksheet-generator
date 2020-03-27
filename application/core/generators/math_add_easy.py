import random
from core.utils import Generator


class Main(Generator):
    name = 'Fast addition in one minute'
    years = [5, 6]
    directions = 'Afla cat de multe operatiuni poti rezolva in maxim 1 minut.'
    template = 'generators/math.html'

    def generate_data(self):
        numbers = list(range(0, 10))
        results = []
        for i in range(self.count):
            row = []
            while not len(row) == 48:
                left_number = random.choice(numbers)
                righ_possible = numbers.copy()
                righ_possible.remove(left_number)
                right_number = random.choice(righ_possible)
                if (left_number, right_number) not in row:
                    row.append((left_number, right_number))
            results.append(row)
        self.data = results
        return results

    def get_context_data(self, iteration):
        context = super(Main, self).get_context_data(iteration)
        context['items'] = context['items'][iteration]
        context['operation'] = '+'
        return context
