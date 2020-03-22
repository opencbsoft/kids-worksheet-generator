import os
import random
import json

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.template.loader import render_to_string

import pdfkit


def generate_pattern_sets():
	source = os.path.join(settings.BASE_DIR, 'core', 'static', 'patterns', 'pattern_source.json')
	with open(source, 'r') as f:
		file_data = json.load(f)
	combinations = file_data.get('block4')
	positions = []
	final_combinations = []
	positions_index = 0
	while positions_index < 4:
		random_number = random.randint(0, len(combinations) - 1)
		if random_number not in positions:
			positions.append(random_number)
			positions_index += 1
	for position in positions:
		final_combinations.append(combinations[position])
	initial_values = []
	path_dir = os.path.join(settings.BASE_DIR, 'core', 'static', 'food')
	for item in os.listdir(path_dir):
		initial_values.append(item)
	data = list()
	options = list()
	for item in final_combinations:
		line = list()
		values_list = ["", "", "", ""]
		for element in range(0, 4):
			value_choice = ""
			while value_choice in values_list:
				value_choice = random.choice(initial_values)
			values_list[element] = value_choice
		for el in item:
			line.append(values_list[el])
		options.append(line[1])
		options.append(line[2])
		data.append(line)
	shuffled_list = random.sample(options, len(options))
	return {"items": data, "first_row": shuffled_list[4:], "second_row": shuffled_list[:4]}


class Command(BaseCommand):
	help = 'Closes the specified poll for voting'

	def handle(self, *args, **options):
		for i in range(1, 11):
			patterns = generate_pattern_sets()
			context = {'path': 'http://127.0.0.1:8000/static/', "items": patterns.get("items"), "first_row": patterns.get("first_row"), "second_row": patterns.get("second_row")}
			icons = {}
			for item in os.listdir(settings.RESOURCES):
				icons[item] = os.listdir(os.path.join(settings.RESOURCES, item))
			content = render_to_string('smart/fill_the_pattern2.html', context)
			folder = os.path.join(settings.OUTPUT, 'fill_the_pattern2')
			os.makedirs(folder, exist_ok=True)
			pdfkit.from_string(content, os.path.join(folder, 'generated{}.pdf'.format(i)), options=settings.PDF_OPTIONS)

		self.stdout.write(self.style.SUCCESS('Successfully generated'))
