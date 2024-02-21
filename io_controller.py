from pynput.mouse import Listener, Button
from sudoku_solver import Sudoku
from PIL.Image import Image
import pyautogui as pg
from time import sleep

Coord = tuple[int, int]


class IOController:
  
  def __init__(self) -> None:
    self.last_coords: list[Coord, Coord]

  def get_coords(self) -> list[Coord, Coord]:
    """ Return a tuple with the coords where the user did click

    Returns:
        tuple[Coord]: topleft and bottomright coords of the clicks
    """
    
    coords = []
    
    def on_click(x, y, button, pressed) -> Coord:  
      if not pressed and button == Button.left:
        coords.append((x, y))
      
      if len(coords) == 2:
        return False

    with Listener(on_click=on_click) as listener:
      listener.join()
    
    self.last_coords = coords
    return coords


  def screenshot(self, filename: str, region: tuple[int, int, int, int]) -> Image:
    """Take a screenshot from a region of the monitor 

    Args:
        filename (str): file name of the screenshot taken
        region (tuple[int, int, int, int]): left, top, width, height of the screenshot

    Returns:
        Image: screenshot
    """
    return pg.screenshot(filename, region=region)
  
  
  def total_screenshot(self, filename: str) -> Image:
    if filename is None:
      return pg.screenshot()
    return pg.screenshot(filename)  


  def take_screenshot(self, filename: str) -> Image:
    (x1, y1), (x2, y2) = self.get_coords()
    return self.screenshot(filename, (x1, y1, x2-x1, y2-y1))
  
  
  def take_total_screenshot(self, filename: str | None) -> Image:
    self.get_coords()
    return self.total_screenshot(filename)


  def complete_sudoku(self, coords: list[Coord, Coord], sudoku_input: Sudoku, sudoku_solved: Sudoku):
    if coords is None:
      coords = self.last_coords
    
    pg.MINIMUM_DURATION = 0
    pause = False
    
    tl, br = coords # topleft, bottomright
    
    (x1, y1), (x2, y2) = tl, br
    height, width = y2-y1, x2-x1
    cell_height, cell_width = height/9, width/9
    
    x, y = tl
    for i in range(9):
      for j in range(9):
        if sudoku_input[i][j] == 0:
          # pg.moveTo(x + j*cell_width + cell_width//2, y + i*cell_height + cell_height//2)
          pg.click(x + j*cell_width + cell_width//2, y + i*cell_height + cell_height//2, _pause=pause)
          pg.press('num%d' % sudoku_solved[i][j], _pause=pause)
          # sleep(1)
