from screenshot import take_screenshot
from image_manipulation import sudoku_only_numbers

if __name__ == '__main__':
  img = take_screenshot('sudoku.png')
  sudoku_only_numbers(img)
