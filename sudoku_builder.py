from warnings import filterwarnings

from sklearn.model_selection import train_test_split
from sudoku_solver import Sudoku
from sklearn.ensemble import RandomForestClassifier
import pandas as pd
import joblib as jl
import numpy as np

def import_model():
  filterwarnings('ignore', category=UserWarning)
  return jl.load('new_model.joblib')


def get_model():
  df = pd.read_csv('new_dataset.csv', index_col=None)
  X = df.drop('label', axis=1)
  y = df['label']
  
  model = RandomForestClassifier(n_estimators=100)
  model.fit(X, y)
  return model
  

def image_to_number(img: np.ndarray, model) -> int:  
  return int(model.predict([img])[0])


def build_sudoku_matrix(cells: list[np.ndarray]) -> Sudoku:
  # model = import_model()
  model = get_model()
  sudoku = [[-1 for _ in range(9)] for _ in range(9)]
  for index, cell in enumerate(cells):
    i, j = index // 9, index % 9
    sudoku[i][j] = image_to_number(cell.flatten(), model)
  return sudoku
