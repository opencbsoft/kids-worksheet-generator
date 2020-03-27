import random
import string
from core.utils import Generator


class Main(Generator):
	name = 'Completeaza literele lipsa usor'
	years = [5, 6]
	directions = 'Completeaza literele lipsa in zonele dedicate lor.'
	template = 'generators/missing_letters.html'

	def generate_data(self):
		results = []
		for i in range(self.count):
			result = []
			letters = list(string.ascii_lowercase)
			for index in range(6):
				sub_list = letters[index * 5: (index + 1) * 5]
				missing = []
				if len(sub_list) > 3:
					while len(missing) < 1:
						random_position = random.randint(1, 3)
						if len(result) > 5:
							upper = (index-2) * 5 + random_position
							if result[upper] != "":
								missing.append(random_position)
						else:
							missing.append(random_position)
					sub_list[missing[0]] = ""
				result = result + sub_list
			results.append(result)
		self.data = results
		return results

	def get_context_data(self, iteration):
		context = super(Main, self).get_context_data(iteration)
		context['shape'] = random.randint(1, 5)
		context['items'] = context['items'][iteration]
		return context
