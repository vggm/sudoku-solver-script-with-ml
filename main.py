
from pynput.mouse import Listener, Button
import pyautogui as pg

Coord = tuple[int, int]


def get_coords() -> list[int]:
  coords = []
  
  def on_click(x, y, button, pressed) -> Coord:  
    if not pressed and button == Button.left:
      print("TopLeft" if len(coords) == 2 else "BottomRight", 
            f"is ({x}, {y})")
      coords.append(x)
      coords.append(y)
    
    if len(coords) == 4:
      return False

  with Listener(on_click=on_click) as listener:
    listener.join()
  
  return coords


pg.screenshot('sudoku.png', region=get_coords())
