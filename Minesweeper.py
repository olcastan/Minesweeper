from enum import Enum
import random

class CellStatus(Enum):
  EXPOSED = 1
  UNEXPOSED = 2
  SEALED = 3

class GameStatus(Enum):
  INPROGRESS = 1
  WON = 2
  LOST = 3

MAX_BOUNDS = 10

class Minesweeper:

  def __init__(self):
    self.flag = False

    self.cells = [[CellStatus.UNEXPOSED
      for i in range(MAX_BOUNDS)] for j in range(MAX_BOUNDS)]

    self.CellType = [[False
      for i in range(MAX_BOUNDS)] for j in range(MAX_BOUNDS)]

    self.minedCell = []

  def expose_cell(self, row, col):
    self.check_bounds(row, col)

    if self.cells[row][col] == CellStatus.UNEXPOSED:
      self.cells[row][col] = CellStatus.EXPOSED
      if self.adjacent_mine_count_at(row, col) == 0:
       self.expose_neighbors(row, col)

  def expose_neighbors(self, i, j):
    neighbors = [[i, j+1], [i+1, j], [i+1, j+1], [i, j-1], [i+1, j-1], [i-1, j], [i-1, j+1], [i-1, j-1]]
    for cell in neighbors:
      if 0 <= cell[0] <= MAX_BOUNDS - 1 and 0 <= cell[1] <= MAX_BOUNDS - 1:
        self.expose_cell(cell[0],cell[1])

  def toggle_seal(self, row, col):
    self.check_bounds(row, col)

    if self.cells[row][col] == CellStatus.EXPOSED:
        return

    if self.cells[row][col] == CellStatus.SEALED:
        self.cells[row][col] = CellStatus.UNEXPOSED
    else:
        self.cells[row][col] = CellStatus.SEALED

  def get_cell_state(self, row, col):
      return self.cells[row][col]

  def check_bounds(self, row, column):
    if row not in range(0, MAX_BOUNDS) or column not in range(0, MAX_BOUNDS):
      raise IndexError

  def set_mine(self, row, col):
    self.CellType[row][col] = True
    self.minedCell.append([row,col])

  def is_mine_at(self, row, col):
    if 0 <= row <= 10 - 1 and 0 <= col <= 10 - 1:
      return self.CellType[row][col]
    else:
      return False

  def adjacent_mine_count_at(self, i, j):
    neighbors = [[i, j + 1], [i + 1, j], [i + 1, j + 1], [i, j - 1], [i + 1, j - 1], [i - 1, j], [i - 1, j + 1], [i - 1, j - 1]]
    counter = 0
    for cell in neighbors:
      if self.is_mine_at(cell[0], cell[1]) is True:
        counter += 1
    return counter

  def get_game_status(self):
    for i in range(len(self.minedCell)):
        if self.get_cell_state(self.minedCell[i][0], self.minedCell[i][1]) == CellStatus.EXPOSED:
          return GameStatus.LOST

    for i in range(MAX_BOUNDS):
      for j in range(MAX_BOUNDS):
        if (i, j) not in self.minedCell and self.get_cell_state(i, j) == CellStatus.UNEXPOSED:
          return GameStatus.INPROGRESS

    for i in range(len(self.minedCell)):
      if self.get_cell_state(self.minedCell[i][0], self.minedCell[i][1]) != CellStatus.SEALED:
        return GameStatus.INPROGRESS

    return GameStatus.WON

  def randomize(self,seed):
    random.seed(seed)
    k = list()
    tempList = list()

    while len(tempList) != 10:
      i = random.randint(0, MAX_BOUNDS - 1)
      j = random.randint(0, MAX_BOUNDS - 1)
      k.append([i, j])
      for sublist in k:
        if sublist not in tempList:
          tempList.append(sublist)

    self.minedCell = tempList

    for i in range(len(self.minedCell)):
      self.CellType[self.minedCell[i][0]][self.minedCell[i][1]] = True
