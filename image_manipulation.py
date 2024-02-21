from cv2.typing import MatLike
from PIL.Image import Image
from matplotlib import pyplot as plt
import numpy as np
import cv2 as cv

# CELL SIZE
WIDTH = HEIGHT = 50 # pixels
CELL_SIZE = (WIDTH, HEIGHT)

SudokuDimension = tuple[int, int, int, int]


def convert_PIL_to_Matlike(pil_img: Image) -> MatLike:
  open_cv_image = np.array(pil_img)
  # Convert RGB to BGR
  open_cv_image = open_cv_image[:, :, ::-1].copy()
  return open_cv_image


def filter(contour: MatLike) -> bool:
  topleft = None
  for row in contour:
    for coord in row:
      topleft = coord
      break
  
  (x1, y1) = topleft
  
  return (x1 > 1 and y1 > 300)


def max_contour(img: MatLike, thresh: MatLike) -> tuple[int, int, int, int]:
  contours, _ = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
  
  # img_cont1 = cv.drawContours(img, contours, -1, (0,255,0), 2, cv.LINE_AA)
  # plt.imshow(cv.cvtColor(img_cont1, cv.COLOR_BGR2RGB))
  # plt.show()
  
  squads = []
  for cont in contours:
    if filter(cont):
      squads.append(cont)
  
  max_squad = sorted(squads, key=cv.contourArea, reverse=True)[0]
    
  # img_cont2 = cv.drawContours(img, [max_squad], -1, (0,0,255), 2, cv.LINE_AA)
  # plt.imshow(cv.cvtColor(img_cont2, cv.COLOR_BGR2RGB))
  # plt.show()
  
  topleft = [99999, 99999]
  bottomright = [0, 0]
  for coord in max_squad:
    x, y = coord[0]
    topleft[0] = min(topleft[0], x)
    topleft[1] = min(topleft[1], y)
    bottomright[0] = max(bottomright[0], x)
    bottomright[1] = max(bottomright[1], y)
  
  return topleft[0]+2, topleft[1]+2, bottomright[0] - topleft[0]-2, bottomright[1] - topleft[1]-2


def thresholding(img: MatLike) -> MatLike:
  
  # Make the image with gray scale
  gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
  
  ret1,th1 = cv.threshold(gray,100,255,cv.THRESH_BINARY)
 
  # ret2,th2 = cv.threshold(gray,0,255,cv.THRESH_BINARY+cv.THRESH_OTSU)
 
  # Otsu's thresholding after Gaussian filtering
  # blur = cv.GaussianBlur(gray,(5,5),0)
  # _, th3 = cv.threshold(blur,0,255,cv.THRESH_BINARY+cv.THRESH_OTSU)
  return th1


def resize(img: MatLike) -> MatLike:
  return cv.resize(img,(9*HEIGHT, 9*WIDTH), interpolation = cv.INTER_AREA)


def remove_edges(img: MatLike) -> MatLike:
  sudoku_lateral_length = HEIGHT * 9
  h = sudoku_lateral_length // 3
  
  color = (255, 255, 255)
  thickness = 4
  
  start = [0, 0]
  end = [0, WIDTH*9]
    
  for _ in range(4):
    img = cv.line(img, start, end, color, thickness)
    start[0] += h
    end[0] += h
    
  start = [0, 0]
  end = [WIDTH*9, 0]
    
  for _ in range(4):
    img = cv.line(img, start, end, color, thickness)
    start[1] += h
    end[1] += h
  
  return img


def crop_image(x: int, y: int, width: int, height: int, img: MatLike) -> MatLike:
  """ Crop an image

  Args:
      x (int): left
      y (int): top
      width (int): width of the new img
      height (int): height of the new img
      img (MatLike): image to be cropped

  Returns:
      MatLike: image cropped
  """
  return img[y:y+height, x:x+width]


def separate_cell_boxes(img: MatLike) -> list[np.ndarray]:
  cells = []
  path = 'cells/cell_%s_%s.png'
  for i in range(9):
    for j in range(9):
      cell = crop_image(j*WIDTH, i*HEIGHT, WIDTH, HEIGHT, img)
      cv.imwrite(path % (i, j), cell)
      cells.append(cell)
  
  return cells


def sudoku_to_cells(pil_img: Image) -> tuple[SudokuDimension, list[np.ndarray]]:
  img = convert_PIL_to_Matlike(pil_img)
  thresholded = thresholding(img)
  cv.imwrite('test_threshold.png', thresholded)
  x, y, width, height = max_contour(img, thresholded)
  cropped = crop_image(x, y, width, height, thresholded)
  cv.imwrite('test_cropped.png', cropped)
  resized_img = resize(cropped)
  cv.imwrite('test_resized.png', resized_img)
  final_img = remove_edges(resized_img)
  cv.imwrite('test_final.png', final_img)
  return (x, y, width, height), separate_cell_boxes(resized_img)
