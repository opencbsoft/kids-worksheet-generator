import random
from core.utils import Generator


class Main(Generator):
	name = 'Completeaza numerele lipsa mediu'
	years = [5, 6]
	directions = 'Completeaza numerele lipsa in zonele dedicate lor.'
	template = 'generators/missing_numbers.html'

	def generate_data(self):
		results = []
		for i in range(self.count):
			result = []
			for index in range(10):
				sub_list = list(range(index*10+1, (index+1)*10+1))
				target_missing = random.randint(1, 3)
				missing = []
				while len(missing) < target_missing:
					random_position = random.randint(index*10+1, (index+1)*10)
					if random_position not in missing:
						missing.append(random_position)
				for element in missing:
					for range_index in range(len(sub_list)):
						if sub_list[range_index] == element:
							sub_list[range_index] = ""
							continue
				result = result + sub_list
			results.append(result)
		self.data = results
		return results

	def get_context_data(self, iteration):
		context = super(Main, self).get_context_data(iteration)
		context['items'] = context['items'][iteration]
		return context
