from image_manipulation import sudoku_to_cells
from sudoku_builder import build_sudoku_matrix
from sudoku_solver import SudokuSolver
from io_controller import IOController


def print_matrix(matrix: list[list[int]]) -> None:
  for row in matrix:
    print(*row)


def main() -> None:
  sudoku_solver = SudokuSolver()
  ioc = IOController()
  
  img = ioc.take_total_screenshot(None)
  (x, y, width, height), cells = sudoku_to_cells(img)
  
  topleft = x, y
  bottomright = x+width, y+height

  sudoku = build_sudoku_matrix(cells)
  
  for row in sudoku:
    print(*row)
  print()
  
  result, time = sudoku_solver.solve(sudoku)
  if result is not None:
    print_matrix(result)
    print(f'Time {time*1000:.2f}ms')
    ioc.complete_sudoku((topleft, bottomright), sudoku, result)
  else:
    print(sudoku_solver.msg_error)


if __name__ == '__main__':
  main()
