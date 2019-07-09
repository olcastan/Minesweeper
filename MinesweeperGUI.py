import tkinter as tk
from tkinter import *
from tkinter import messagebox
import random
from src.Minesweeper import (Minesweeper,CellStatus,GameStatus,MAX_BOUNDS)

class Window(Frame):
	def __init__(self, master = None):
		self.minesweeper = Minesweeper()
		self.minesweeper.randomize(random.randint(0,10000))

		Frame.__init__(self, master)
		self.master = master

		self.buttons = [[self.create_buttons(j,i) for i in range(MAX_BOUNDS)] for j in range(MAX_BOUNDS)]

	def create_buttons(self,row, col):
		button = tk.Label(master=None, bg = "white",width=4, height = 2,borderwidth = 2, relief='raised')
		button.grid(row = row, column = col)
		button.bind('<Button-1>', lambda e: self.click_cell(row, col))
		button.bind('<Button-3>', lambda e: self.toggle_seals(row, col))

		return button

	def toggle_seals(self,row, col):
		if self.minesweeper.get_cell_state(row, col) is not CellStatus.EXPOSED:
			if self.minesweeper.get_cell_state(row,col) == CellStatus.SEALED:
				self.buttons[row][col].config(text="")
				self.minesweeper.cells[row][col] = CellStatus.UNEXPOSED
			else:
				self.minesweeper.toggle_seal(row,col)
				self.buttons[row][col].config(text=u"\u2691", fg="red")

			self.game_status_update()

	def click_cell(self, row, col):
		if self.minesweeper.get_cell_state(row,col) is not CellStatus.SEALED:
			self.minesweeper.expose_cell(row,col)
			self.buttons[row][col].config(state=DISABLED, bg="#ABABA7")

			if self.minesweeper.adjacent_mine_count_at(row, col):
				self.buttons[row][col].config(text= self.minesweeper.adjacent_mine_count_at(row, col),fg = "red", bg = "#ABABA7", state=DISABLED)
			elif self.minesweeper.get_game_status() != GameStatus.LOST:
				self.disable_neighbors()

			self.game_status_update()

	def disable_neighbors(self):
		for i in range(MAX_BOUNDS):
			for j in range(MAX_BOUNDS):
				if self.minesweeper.get_cell_state(i,j) is CellStatus.EXPOSED:
					if self.minesweeper.adjacent_mine_count_at(i,j):
						self.buttons[i][j].config(text= self.minesweeper.adjacent_mine_count_at(i, j),fg = "red", bg = "#ABABA7", state= DISABLED)
					else:
						self.buttons[i][j].config(state=DISABLED,bg="#ABABA7",fg = "red",)

	def disable_all_buttons(self):
		for i in range(MAX_BOUNDS):
			for j in range(MAX_BOUNDS):
				self.buttons[i][j].config(state = DISABLED)

	def game_status_update(self):
		if self.minesweeper.get_game_status() is GameStatus.LOST:
			self.reveal_mines()
			self.disable_all_buttons()
			messagebox.showinfo("GAME OVER", "YOU LOST")


		if self.minesweeper.get_game_status() is GameStatus.WON:
			messagebox.showinfo("You Won!","CONGRATULATIONS")
			self.disable_all_buttons()

	def reveal_mines(self):
		for i in range(len(self.minesweeper.minedCell)):
			self.buttons[self.minesweeper.minedCell[i][0]][self.minesweeper.minedCell[i][1]].config(text=u"\u2620")


class Main(Window):

	def __init__(self):
		master = Tk()
		master.pack_slaves()

		master.title("Minesweeper")
		app = Window(master)
		app.mainloop()


# Main()  #Feedback: Do not call this from here. The CI build gets stuck launching the GUI
