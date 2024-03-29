import datetime
import os

from PyPDF2 import PdfFileMerger
from django.conf import settings
from django.core.management.base import BaseCommand

from core.models import Board


def get_available_generators():
    commands = []
    for item in os.listdir(os.path.join(settings.BASE_DIR, 'core', 'generators')):
        if item not in ['__init__.py', '__pycache__']:
            item = item.replace('.py', '')
            commands.append(item)
    return commands


def call_generator(c, generator, options):
    print('generating {}'.format(generator))
    try:
        mod = __import__('core.generators.{}'.format(generator), fromlist=['Main'])
        klass = getattr(mod, 'Main')
    except Exception as e:
        c.stderr.write(c.style.ERROR('Could not find the specific generator {} Error: {}'.format('core.generators.{}'.format(generator), e)))
        return 0
    generator = klass(options['count'], options.get('extra'))
    return generator.render()


class Command(BaseCommand):
    help = 'Generate a worksheet using a specific generator'

    def add_arguments(self, parser):
        parser.add_argument('--list', type=str, help='List all available generators that match a certain age, or all if you want to see all available.')
        parser.add_argument('-g', '--generator', type=str, help='The name of the generator to use')
        parser.add_argument('--count', type=int, help='How many to generate', default=10)
        parser.add_argument('--all', type=str, help='Generate from all templates')
        parser.add_argument('--extra', type=str, help='Extra parameter passed to the generator')

    def handle(self, *args, **options):
        if options['list']:
            for item in get_available_generators():
                print(item)
        elif options['generator']:
            call_generator(self, options['generator'], options)
            self.stdout.write(self.style.SUCCESS('Successfully generated'))
        elif options['all']:
            try:
                specific_date = datetime.datetime.strptime(options['all'], '%d.%m.%Y')
            except:
                specific_date = datetime.datetime.today()
            print('Printing for date: {}'.format(specific_date.strftime('%d.%m.%Y')))
            os.makedirs(os.path.join(settings.MEDIA_ROOT, 'worksheets'), exist_ok=True)
            generators = get_available_generators()
            generated_files = []
            for generator in generators:
                generated_files += call_generator(self, generator, options)
            merger = PdfFileMerger()
            for filename in generated_files:
                merger.append(filename)
            today = datetime.date.today()
            merger.write(os.path.join(settings.MEDIA_ROOT, 'worksheets', '{}.pdf'.format(specific_date.strftime('%d-%m-%Y'))))
            # if not Board.objects.filter(created=specific_date).exists():
            #     board = Board(created=specific_date)
            #     board.file.name = os.path.join('worksheets/{}.pdf'.format(specific_date.strftime('%d-%m-%Y')))
            #     board.save()
            for filename in generated_files:
                os.unlink(filename)
            self.stdout.write(self.style.SUCCESS('Successfully generated'))