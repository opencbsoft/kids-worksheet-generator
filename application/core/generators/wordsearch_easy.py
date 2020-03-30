import string
import random
from core.utils import Generator


class WordSearch:
    HORIZONTAL = 0
    VERTICAL = 1
    DIAGONAL = 2
    REVHORIZONTAL = 3
    REVVERTICAL = 4
    REVDIAGONAL = 5
    REVFLIPDIAGONA = 6
    FLIPDIAGONAL = 7
    DONTCARE = -100
    wordPosition = {}

    def __init__(self, searchWords, maxX=20, maxY=20, direction=0):
        self.direction = direction
        self.maxX = maxX
        self.maxY = maxY
        self.grid = []  # grid is a list of list of strings (characters)
        if ',' in searchWords:
            self.searchWords = searchWords.split(",")
        else:
            self.searchWords = searchWords
        print(self.searchWords)
        for row in range(0, self.maxY):
            self.grid.append([])
            for column in range(0, self.maxX):
                self.grid[row].append('*')
        for word in searchWords:
            while not self.engrave(word, self.DONTCARE, self.DONTCARE, self.direction):
                pass
        #self.obfuscate()

    def engrave(self, word, x, y, direction):
        if len(word) == 0:
            return True
        # word has length > 0
        # check if we need to choose random pos
        if x == self.DONTCARE or y == self.DONTCARE:
            while True:
                y = random.randint(0, self.maxY - 1)
                x = random.randint(0, self.maxX - 1)
                if self.grid[y][x] == '*':
                    break
        # check if x & y are valid
        if x == self.maxX or x < 0:
            return False
        if y == self.maxY or y < 0:
            return False
        if not (self.grid[y][x] == "*" or self.grid[y][x] == word[0]):
            return False
        undovalue = self.grid[y][x]
        undox = x
        undoy = y
        self.grid[y][x] = word[0]
        # now need to write rest of the word
        if direction == self.HORIZONTAL:
            x += 1
        elif direction == self.VERTICAL:
            y += 1
        elif direction == self.DIAGONAL:
            y += 1
            x += 1
        elif direction == self.REVHORIZONTAL:
            x -= 1
        elif direction == self.REVVERTICAL:
            y -= 1
        elif direction == self.REVDIAGONAL:
            y -= 1
            x -= 1
        elif direction == self.FLIPDIAGONAL:
            x += 1
            y -= 1
        elif direction == self.REVFLIPDIAGONA:
            x -= 1
            y += 1
        else:
            print("This direction not implemented yet")
        if self.engrave(word[1:], x, y, direction):
            # we could do the rest, we are happy and done
            return True
        else:
            # grrh: something didn’t work, we need to undo now
            y = undoy
            x = undox
            self.grid[y][x] = undovalue
            return False

    def obfuscate(self):
        for row in self.grid:
            for i in range(len(row)):
                if row[i] == '*':
                    row[i] = random.choice(string.ascii_uppercase)

    def letter(self, x, y):
        return self.grid[x][y]

    def findWords(self, words):
        for word in words:
            firstLetter = word[0]
            positions = None
            y = 0; found = False
            while y < self.maxY and not found:
                x = 0
                while x < self.maxX and not found:
                    if firstLetter == self.grid[y][x]:
                        positions = self.wordIsHere(word, x, y)
                        if positions:
                            found = True
                            break
                    x += 1
                if not found:
                    y += 1
            if found:
                self.wordPosition[word] = positions

    def wordIsHere(self,word, firstX, firstY):
         maxX = self.maxX
         maxY = self.maxY
         # horizontal
         found = True; x = firstX; y = firstY; positions = []
         for letter in word:
             if x == maxX or letter != self.grid[y][x]:
                 found = False
                 break
             positions.append((y, x))
             x += 1
         if found:
             return positions
         # vertical
         found = True; x = firstX; y = firstY; positions = []
         for letter in word:
             if y == maxY or letter != self.grid[y][x]:
                 found = False
                 break
             positions.append((y, x))
             y += 1
         if found:
             return positions
         # reverse horizontal
         found = True; x = firstX; y = firstY; positions = []
         for letter in word:
             if x == -1 or letter != self.grid[y][x]:
                 found = False
                 break
             positions.append((y, x))
             x -= 1
         if found:
             return positions
         # reverse vertical
         found = True; x = firstX; y = firstY; positions = []
         for letter in word:
             if y == -1 or letter != self.grid[y][x]:
                 found = False
                 break
             positions.append((y, x))
             y -= 1
         if found:
             return positions
         # diagonal
         found = True; x = firstX; y = firstY; positions = []
         for letter in word:
             if y == maxY or x == maxX or letter != self.grid[y][x]:
                 found = False
                 break
             positions.append((y, x))
             x += 1
             y += 1
         if found:
             return positions
         # reverse diagonal
         found = True; x = firstX; y = firstY; positions = []
         for letter in word:
             if y == -1 or x == -1 or letter != self.grid[y][x]:
                 found = False
                 break
             positions.append((y, x))
             x -= 1
             y -= 1
         if found:
             return positions
         # flip diagonal
         found = True; x = firstX; y = firstY; positions = []
         for letter in word:
             if y == -1 or x == maxX or letter != self.grid[y][x]:
                 found = False
                 break
             positions.append((y, x))
             x += 1
             y -= 1
         if found:
             return positions
         # reverse flip diagonal
         found = True; x = firstX; y = firstY; positions = []
         for letter in word:
             if y == maxY or x == -1 or letter != self.grid[y][x]:
                 found = False
                 break
             positions.append((y, x))
             x -= 1
             y += 1
         if found:
             return positions
         return None


class WordGrid:
    HORIZONTAL = 0
    VERTICAL = 1
    DIAGONAL = 2
    DIRECTIONS = [HORIZONTAL, VERTICAL, DIAGONAL]
    LETTERS = 'ABCDEFGHIJKLMNOPQRSȘTȚUVWXYZ'

    def __init__(self, search_words:list, width, height, direction=0):
        self.words = search_words
        self.width = width
        self.heigth = height
        self.direction = direction
        self.grid = []
        for i in range(0, self.heigth):
            row = []
            for j in range(0, self.width):
                row.append('*')
            self.grid.append(row)
        for word in self.words:
            self.add_word(word, self.direction)
        self.fill_remaining()

    def get_grid(self):
        return self.grid

    def add_word(self, word, direction):
        if direction == self.HORIZONTAL:
            # 1. search for rows having this width available
            available_rows = []
            possible = ''
            for i in range(0, len(word)):
                possible += '*'
            for i in range(0, self.heigth):
                line = ''.join(self.grid[i])
                if possible in line:
                    available_rows.append(i)
            # 2. select a random row
            if len(available_rows) == 0:
                raise Exception('Not enough space o fit this word on a row')
            row = random.choice(available_rows)
            # 3. select a random col
            line = ''.join(self.grid[row])
            index = 0
            available_cols = []
            while index < len(line):
                index = line.find(possible, index)
                if index == -1:
                    break
                available_cols.append(index)
                index += 1
            if len(available_cols) == 0:
                raise Exception('Not enough space o fit this word horizontally')
            col = random.choice(available_cols)
            # fill the word in that col
            for i in range(0, len(word)):
                self.grid[row][col] = word[i]
                col += 1

    def fill_remaining(self):
        for row in range(0, self.heigth):
            for col in range(0, self.width):
                if self.grid[row][col] == '*':
                    self.grid[row][col] = random.choice(list(self.LETTERS))

    def print(self):
        line = ' '
        for i in range(1, self.width+1):
            line += '-'
        line += ' '
        print(line)
        for row in self.grid:
            line = '|'
            for col in row:
                line += col
            line += '|'
            print(line)
        line = ' '
        for i in range(1, self.width + 1):
            line += '-'
        line += ' '
        print(line)


class Main(Generator):
    name = 'Word search Easy'
    years = [5, 6, 7]
    directions = 'Cauta cuvintele in tabel.'
    template = 'generators/wordsearch_easy.html'

    def generate_data(self):
        bag_of_words = []
        bag_of_words.append(['CÂINE', 'PISICĂ', 'CAL', 'RAȚĂ', 'GĂINĂ', 'COCOȘ', 'PUI', 'PUIȘOR', 'MĂGAR', 'IED', 'CAPRĂ', 'ȚAP', 'PORC', 'PURCEL', 'OAIE', 'VACĂ', 'VIȚEL'])
        bag_of_words.append('Mugure,frunză,petală,senin,cer,fluture,albină,polen,zambilă,ghiocel,iarbă,copac,floare,verde,soare'.upper().split(','))
        results = []
        for i in range(self.count):
            selected_words = random.sample(random.choice(bag_of_words), 8)
            grid = WordGrid(selected_words, 7, 8)
            grid.print()
            results.append({'grid': grid.get_grid(), 'words': selected_words})
        self.data = results
        return results

    def get_context_data(self, iteration):
        context = super(Main, self).get_context_data(iteration)
        context['items'] = context['items'][iteration]
        return context

