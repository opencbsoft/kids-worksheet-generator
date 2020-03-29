import random
from core.utils import Generator


class Main(Generator):
	name = 'Completeaza literele lipsa mediu'
	years = [5, 6]
	directions = 'Completeaza literele lipsa in zonele dedicate lor.'
	template = 'generators/missing_letters.html'
	LETTERS = 'ABCDEFGHIJKLMNOPQRSȘTȚUVWXYZ'

	def generate_data(self):
		results = []
		for i in range(self.count):
			result = []
			letters = self.LETTERS
			for index in range(6):
				sub_list = letters[index * 5: (index + 1) * 5]
				missing = []
				if len(sub_list) > 3:
					while len(missing) < 2:
						random_position = random.randint(1, 3)
						if random_position not in missing:
							missing.append(random_position)
					for element in missing:
						for range_index in range(len(sub_list)):
							if range_index == element:
								sub_list[range_index] = ""
								continue
				result = result + sub_list
			results.append(result)
		self.data = results
		return results

	def get_context_data(self, iteration):
		context = super(Main, self).get_context_data(iteration)
		context['shape'] = random.randint(1, 5)
		context['items'] = context['items'][iteration]
		return context
