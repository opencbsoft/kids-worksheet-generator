import os
import random
import string
import itertools

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.template.loader import render_to_string

import pdfkit


def generate(icons: list, count: int):
    context = {'path': 'http://127.0.0.1:8000/static/'}
    folder = os.path.join(settings.OUTPUT, 'match_with_number')
    os.makedirs(folder, exist_ok=True)
    for no in range(count):
        samples = random.sample(list(range(1, 23)), 6)
        context['items'] = []
        for i in samples:
            context['items'].append(range(i))
        context['icons'] = random.sample(icons, 6)
        random.shuffle(samples)
        context['numbers'] = samples
        content = render_to_string('smart/match_with_number.html', context)
        pdfkit.from_string(content, os.path.join(folder, 'generated{}.pdf'.format(no)), options=settings.PDF_OPTIONS)
    return True


class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def add_arguments(self, parser):
        parser.add_argument('--count', type=int, help='How many to generate', default=10)

    def handle(self, *args, **options):
        path_dir = os.path.join(settings.BASE_DIR, 'core', 'static', 'food')
        icons = [item for item in os.listdir(path_dir)]
        generate(icons, options['count'])

        self.stdout.write(self.style.SUCCESS('Successfully generated'))
