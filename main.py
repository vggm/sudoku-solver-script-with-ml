from image_manipulation import sudoku_to_cells
from sudoku_builder import build_sudoku_matrix
from sudoku_solver import SudokuSolver
from io_controller import IOController

if __name__ == '__main__':
  sudoku_solver = SudokuSolver()
  ioc = IOController()
  
  img = ioc.take_screenshot('sudoku.png')
  cells = sudoku_to_cells(img)
  exit(1)
  sudoku = build_sudoku_matrix(cells)
  for row in sudoku:
    print(*row)
  print()
  
  res, time = sudoku_solver.solve(sudoku)
  if res is not None:
    for row in res:
      print(*row)
    print(f'Time {time*1000:.2f}ms')
    
    ioc.complete_sudoku(None, sudoku, res)
  else:
    print(sudoku_solver.msg_error)
