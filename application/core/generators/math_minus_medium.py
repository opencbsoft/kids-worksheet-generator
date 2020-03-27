import random
from core.utils import Generator


class Main(Generator):
    name = 'Fast medium subsctraction in one minute'
    years = [5, 6, 7]
    directions = 'Afla cat de multe operatiuni poti rezolva in maxim 1 minut.'
    template = 'generators/math.html'

    def generate_data(self):
        small_numbers = list(range(0, 10))
        big_numbers = list(range(11, 100))
        results = []
        for i in range(self.count):
            row = []
            while not len(row) == 48:
                left_number = random.choice(big_numbers)
                right_number = random.choice(small_numbers)
                total = left_number - right_number
                if (total, right_number) not in row:
                    row.append((total, right_number))
            results.append(row)
        self.data = results
        return results

    def get_context_data(self, iteration):
        context = super(Main, self).get_context_data(iteration)
        context['items'] = context['items'][iteration]
        context['operation'] = '-'
        return context
