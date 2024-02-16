from pynput.mouse import Listener, Button
from PIL.Image import Image
import pyautogui as pg

Coord = tuple[int, int]


def get_coords() -> list[Coord]:
  """ Return a list with the coords where the user did click

  Returns:
      list[Coord]: topleft and bottomright coords of the clicks
  """
  
  coords = []
  
  def on_click(x, y, button, pressed) -> Coord:  
    if not pressed and button == Button.left:
      coords.append(x)
      coords.append(y)
    
    if len(coords) == 4:
      return False

  with Listener(on_click=on_click) as listener:
    listener.join()
  
  return coords


def screenshot(filename: str, region: tuple[int, int, int, int]) -> Image:
  """Take a screenshot from a region of the monitor 

  Args:
      filename (str): file name of the screenshot taken
      region (tuple[int, int, int, int]): left, top, width, height of the screenshot

  Returns:
      Image: screenshot
  """
  return pg.screenshot(filename, region=region)


def take_screenshot(filename: str) -> Image:
  x1, y1, x2, y2 = get_coords()
  return screenshot(filename, (x1, y1, x2-x1, y2-y1))
