import itertools
import random
from core.utils import Generator
from mazelib import Maze
from mazelib.generate.Prims import Prims


def toHTML(grid, start, end, cell_size=10):
    row_max = len(grid)
    col_max = len(grid[0])

    html = '<style type="text/css">' + \
           '#maze {width: ' + str(cell_size * col_max) + 'px;height: ' + \
           str(cell_size * row_max) + 'px;border: 0px solid grey;}' + \
           'div.maze_row div{width: ' + str(cell_size) + 'px;height: ' + str(cell_size) + 'px;}' + \
           'div.maze_row div.bl{background-color: black;}' + \
           'div.maze_row div.wh{background-color: white;}' + \
           'div.maze_row div.exit{background-color: white;}' + \
           'div.maze_row div.entry{background-color: white;}' + \
           'div.maze_row div{float: left;}' + \
           'div.maze_row:after{content: ".";height: 0;visibility: hidden;display: block;clear: both;}' + \
           '</style>' + \
           '<div id="maze">'

    for row in range(row_max):
        html += '<div class="maze_row">'
        for col in range(col_max):
            if (row, col) == start:
                html += '<div class="entry"></div>'
            elif (row, col) == end:
                html += '<div class="exit"></div>'
            elif grid[row][col]:
                html += '<div class="bl"></div>'
            else:
                html += '<div class="wh"></div>'
        html += '</div>'
    html += '</div>'

    return html


class Main(Generator):
    name = 'Enter the maze and exit successfully'
    years = [3, 4, 5]
    directions = 'Alege o intrare in labirint si incearca sa iesi pe partea cealalta'
    template = 'generators/maze.html'

    def generate_data(self):
        m = Maze()
        m.generator = Prims(10, 10)
        m.generate()
        m.generate_entrances()
        self.data = toHTML(m.grid, m.start, m.end, 49)
        return self.data
