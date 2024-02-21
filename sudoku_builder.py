from warnings import filterwarnings
from sudoku_solver import Sudoku
import joblib as jl
import numpy as np

def import_model():
  filterwarnings('ignore', category=UserWarning)
  return jl.load('new_model.joblib')


def image_to_number(img: np.ndarray, model) -> int:  
  return int(model.predict([img])[0])


def build_sudoku_matrix(cells: list[np.ndarray]) -> Sudoku:
  model = import_model()
  sudoku = [[-1 for _ in range(9)] for _ in range(9)]
  for index, cell in enumerate(cells):
    i, j = index // 9, index % 9
    sudoku[i][j] = image_to_number(cell.flatten(), model)
  return sudoku
