from time import perf_counter
from copy import deepcopy

Sudoku = list[list[int]]

class SudokuSolver:
  
  
  def __init__(self) -> None:
    self.sudoku: Sudoku
    self.msg_error: str = ''
  
  
  def valid(self, sudoku) -> bool:
    # check rows
    for row in sudoku:
      visited = [False] * 10
      for n in row:
        if n == 0:
          continue
        if visited[n]:
          return False
        visited[n] = True
    
    # check cols
    t_sudoku = list(zip(*sudoku))
    for col in t_sudoku:
      visited = [False] * 10
      for n in col:
        if n == 0:
          continue
        if visited[n]:
          return False
        visited[n] = True
    
    # check boxes
    for I in range(3):
      for J in range(3):
        visited = [False] * 10
        for i in range(3*I, 3*I+3):
          for j in range(3*J, 3*J+3):
            n = sudoku[i][j]
            if n == 0:
              continue
            if visited[n]:
              return False
            visited[n] = True
    
    return True
  
  
  def check_number(self, I, J, opt) -> bool:
    # check rows
    for n in self.sudoku[I]:
      if n == opt: 
        return False
    
    # check cols
    t_sudoku = list(zip(*self.sudoku))
    for n in t_sudoku[J]:
      if n == opt:
        return False
    
    # check box
    bi = I // 3
    bj = J // 3
    
    for i in range(bi*3, bi*3+3):
      for j in range(bj*3, bj*3+3):
        if self.sudoku[i][j] == opt:
          return False
    
    return True
      
  
  def backtracking(self, e=0) -> bool:
    if e == 81:
      return True
    
    i, j = e // 9, e % 9
    if self.sudoku[i][j] != 0:
      if self.backtracking(e+1):
        return True
    
    else:
      for opt in range(1, 10):
        if self.check_number(i, j, opt):
          self.sudoku[i][j] = opt
          if self.backtracking(e+1):
            return True
      self.sudoku[i][j] = 0
        
    return False
    
  
  def solve(self, sudoku: Sudoku) -> tuple[Sudoku | None, int]:
    if not self.valid(sudoku):
      self.msg_error = 'Sudoku Invalid'
      return None, -1

    self.sudoku = deepcopy(sudoku)
    self.msg_error = ''

    start = perf_counter()
    has_solution = self.backtracking()
    end = perf_counter()
    
    if not has_solution:
      self.msg_error = 'No Solution'
      return None, -1
    
    return self.sudoku, end - start
  

if __name__ == '__main__':
  sudoku_solver = SudokuSolver()
  
  test1_str = '''
  0 0 4 0 0 9 0 5 0
  7 0 0 0 0 0 0 1 0
  0 0 8 2 0 0 7 0 9
  6 0 0 0 0 4 9 0 8
  0 4 0 1 0 0 0 0 0
  0 0 0 0 0 0 0 0 5
  0 0 2 0 3 0 0 0 0
  8 0 0 0 0 1 6 0 4
  0 0 0 0 0 0 0 7 0'''
  
  test1 = [[int(n) for n in row.split()] for row in test1_str.split('\n') if row]
  # print(test1)
  
  res, time = sudoku_solver.solve(test1)
  if res is not None:
    for row in res:
      print(*row)
    print(f'Time {time}s')
  else:
    print(sudoku_solver.msg_error)
  
  