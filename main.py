from image_manipulation import sudoku_to_cells
from sudoku_builder import build_sudoku_matrix
from sudoku_solver import SudokuSolver
from screenshot import take_screenshot

if __name__ == '__main__':
  sudoku_solver = SudokuSolver()
  
  img = take_screenshot('sudoku.png')
  cells = sudoku_to_cells(img)
  
  sudoku = build_sudoku_matrix(cells)
  for row in sudoku:
    print(*row)
  print()
  
  res, time = sudoku_solver.solve(sudoku)
  if res is not None:
    for row in res:
      print(*row)
    print(f'Time {time*1000:.2f}ms')
  else:
    print(sudoku_solver.msg_error)
