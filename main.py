from pynput.mouse import Listener, Button
import pyautogui as pg


Coord = tuple[int, int]


def get_coords() -> list[int]:
  coords = []
  
  def on_click(x, y, button, pressed) -> Coord:  
    if not pressed and button == Button.left:
      # print("TopLeft" if len(coords) == 0 else "BottomRight", 
      #       f"is ({x}, {y})")
      coords.append(x)
      coords.append(y)
    
    if len(coords) == 4:
      return False

  with Listener(on_click=on_click) as listener:
    listener.join()
  
  return coords


def take_screenshot(region: tuple[int, int, int, int]):
  # print(x1, y1, x2, y2)
  # region: left, top, width, height
  pg.screenshot('sudoku.png', region=region)
  
  
x1, y1, x2, y2 = get_coords()
take_screenshot(x1, y1, x2-x1, y2-y1)
