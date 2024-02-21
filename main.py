from image_manipulation import sudoku_to_cells
from sudoku_builder import build_sudoku_matrix
from sudoku_solver import SudokuSolver
from io_controller import IOController


def main() -> None:
  sudoku_solver = SudokuSolver()
  ioc = IOController()
  
  img = ioc.take_total_screenshot('sudoku.png')
  (x, y, width, height), cells = sudoku_to_cells(img)
  
  topleft = x, y
  bottomright = x+width, y+height

  sudoku = build_sudoku_matrix(cells)
  for row in sudoku:
    print(*row)
  print()
  
  res, time = sudoku_solver.solve(sudoku)
  if res is not None:
    for row in res:
      print(*row)
    print(f'Time {time*1000:.2f}ms')
    ioc.complete_sudoku((topleft, bottomright), sudoku, res)
  else:
    print(sudoku_solver.msg_error)


if __name__ == '__main__':
  main()
