import keyboard
import os
import numpy as np

COLS = 25
ROWS = 15
HIDDEN_CELL = '*'
FLAGGED_CELL = 'F'
MINE = 'X'

currX: int
currY: int
boardView: np.ndarray
boardMines: np.ndarray
hiddenCells: set[tuple[int, int]]
first_touch: bool
alive: bool


def reset_board():
	global currX, currY, boardView, boardMines, hiddenCells, first_touch, alive
	currX = COLS // 2
	currY = ROWS // 2
	boardView = np.full((ROWS, COLS), HIDDEN_CELL, dtype=str)
	boardMines = np.random.rand(ROWS, COLS) > 0.75
	hiddenCells = {(x, y) for y in range(ROWS) for x in range(COLS)}
	first_touch = True
	alive = True
	print_board()


def check_win():
	return not hiddenCells


def print_board():
	toPrint = ""
	if currY:  # print lines above current line, if not on the first line
		toPrint += ' ' + '\n '.join(' '.join(row) for row in boardView[:currY]) + '\n'
	if currX:  # print cells left of current cell, if not on the first cell
		toPrint += ' ' + ' '.join(boardView[currY][:currX])
	toPrint += f"[{boardView[currY][currX]}]{' '.join(boardView[currY][currX + 1:])}\n " + \
		'\n '.join(' '.join(row) for row in boardView[currY + 1:]) + '\n'
	os.system('cls')
	print(toPrint)


def count_mines(x: int, y: int):
	subgrid = boardMines[max(0, y - 1):min(y + 2, ROWS), max(0, x - 1):min(x + 2, COLS)]
	return np.sum(subgrid)


def dead():
	global alive
	alive = False
	boardView[boardMines] = MINE


def recur_cell(x: int, y: int):
	if not (0 <= x < COLS and 0 <= y < ROWS):
		return
	if boardMines[y, x] or boardView[y, x] != HIDDEN_CELL:
		return
	count = count_mines(x, y)
	if count == 0:
		boardView[y, x] = ' '
		recur_cell(x, y - 1)
		recur_cell(x - 1, y)
		recur_cell(x + 1, y)
		recur_cell(x, y + 1)
		recur_cell(x - 1, y - 1)
		recur_cell(x - 1, y + 1)
		recur_cell(x + 1, y - 1)
		recur_cell(x + 1, y + 1)
	else:
		boardView[y, x] = str(count)
	hiddenCells.remove((x, y))


def hit_cell():
	global first_touch, boardView
	if first_touch:
		first_touch = False
		clearMinesFirstTouch()
	if boardMines[currY, currX]:
		dead()
	else:
		recur_cell(currX, currY)
		if check_win():
			dead()


def clearMinesFirstTouch():
	boardMines[max(0, currY - 1):min(currY + 2, ROWS), max(0, currX - 1):min(currX + 2, COLS)] = False


def flag_curr():
	if boardView[currY, currX] == HIDDEN_CELL:
		boardView[currY, currX] = FLAGGED_CELL
	elif boardView[currY, currX] == FLAGGED_CELL:
		boardView[currY, currX] = HIDDEN_CELL


def keypress(event: keyboard.KeyboardEvent):
	global currX, currY
	if not alive:
		if event.name == 'space':
			reset_board()
		return
	match event.name:
		case 'left':
			currX = (COLS + currX - 1) % COLS
		case 'right':
			currX = (COLS + currX + 1) % COLS
		case 'up':
			currY = (ROWS + currY - 1) % ROWS
		case 'down':
			currY = (ROWS + currY + 1) % ROWS
		case 'space':
			if boardView[currY, currX] == HIDDEN_CELL:
				hit_cell()
			else:
				return
		case 'shift':
			flag_curr()
		case _:
			return
	print_board()


def main():
	reset_board()
	keyboard.on_press(keypress)

	while True:
		pass


if __name__ == "__main__":
	main()
