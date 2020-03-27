import string
import random
from core.utils import Generator


class Main(Generator):
    name = 'Alphabet match upper case with lowercase'
    years = [4, 5]
    directions = 'Incercuiti bulina literei scrise de mana care corespunde cu litera scrisa de tipar'
    template = 'generators/alphabet_match_upper_lower.html'

    def generate_data(self):
        letters = string.ascii_uppercase
        letters_lowercase = string.ascii_lowercase
        results = []
        for i in range(self.count):
            row = dict()
            while not len(row.keys()) == 6:
                capital = random.choice(letters)
                others = random.sample(letters_lowercase, 4)
                if capital.lower() not in others:
                    others[0] = capital.lower()
                random.shuffle(others)
                if capital not in row.keys():
                    row[capital] = others
            results.append(row)
        self.data = results
        return results

    def get_context_data(self, iteration):
        context = super(Main, self).get_context_data(iteration)
        context['items'] = context['items'][iteration]
        return context
