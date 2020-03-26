import string
import random
from core.utils import Generator


class Main(Generator):
    name = 'Decupeaza si potriveste'
    years = [3, 4, 5]
    directions = 'Decupeaza si lipseste literele si cifrele in zonele dedicate lor.'
    template = 'generators/cut_and_match.html'
    content_height = 1050

    def generate_data(self):
        if self.extra:
            max_number = int(self.extra)
        else:
            max_number = 10
        possible = [i for i in string.ascii_letters]
        possible += [str(i) for i in range(1, max_number + 1)]
        results = []
        for i in range(self.count):
            row = random.sample(range(1, max_number + 1), 5)  # Select a minimum of 5 numbers and 5 letters before
            row += random.sample(string.ascii_letters, 5)  # Also add 5 minimum letters
            while len(row) != 20:
                symbol = random.choice(possible)
                if symbol not in row:
                    row.append(symbol)
            random.shuffle(row)
            results.append(row)
        self.data = results
        return results

    def get_context_data(self, iteration):
        context = super(Main, self).get_context_data(iteration)
        context['items'] = random.choice(context['items'])
        return context
