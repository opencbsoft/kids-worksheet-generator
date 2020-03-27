import os
import random
import json
import itertools
import random
from PIL import Image
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.template.loader import render_to_string
from mazelib import Maze
from mazelib.generate.Prims import Prims

import matplotlib.pyplot as plt


def toHTML(grid, start, end, cell_size=10):
    row_max = len(grid)
    col_max = len(grid[0])

    html = '<style type="text/css" media="screen">' + \
           '#maze {width: ' + str(cell_size * col_max) + 'px;height: ' + \
           str(cell_size * row_max) + 'px;border: 3px solid grey;}' + \
           'div.maze_row div{width: ' + str(cell_size) + 'px;height: ' + str(cell_size) + 'px;}' + \
           'div.maze_row div.bl{background-color: black;}' + \
           'div.maze_row div.wh{background-color: white;}' + \
           'div.maze_row div.rd{background-color: red;}' + \
           'div.maze_row div.gr{background-color: green;}' + \
           'div.maze_row div{float: left;}' + \
           'div.maze_row:after{content: ".";height: 0;visibility: hidden;display: block;clear: both;}' + \
           '</style></head><body>' + \
           '<div id="maze">'

    for row in range(row_max):
        html += '<div class="maze_row">'
        for col in range(col_max):
            if (row, col) == start:
                html += '<div class="gr"></div>'
            elif (row, col) == end:
                html += '<div class="rd"></div>'
            elif grid[row][col]:
                html += '<div class="bl"></div>'
            else:
                html += '<div class="wh"></div>'
        html += '</div>'
    html += '</div>'

    return html


class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):
        m = Maze()
        m.generator = Prims(10, 10)
        m.generate()
        m.generate_entrances()
        print()
        self.stdout.write(self.style.SUCCESS('Successfully generated'))
