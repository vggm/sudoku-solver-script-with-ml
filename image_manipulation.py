from cv2.typing import MatLike
from PIL.Image import Image
from matplotlib import pyplot as plt
import numpy as np
import cv2 as cv

# CELL SIZE
WIDTH = HEIGHT = 50 # pixels
CELL_SIZE = (WIDTH, HEIGHT)


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
  
  max_cont = None
  max_area = 0
  for cont in contours:
    if cv.contourArea(cont) > max_area and filter(cont):
      max_cont = cont
      max_area = cv.contourArea(cont)
  
  
  # img_cont = cv.drawContours(img, [max_cont], -1, (0,255,0), 2, cv.LINE_AA)
  # plt.imshow(cv.cvtColor(img_cont, cv.COLOR_BGR2RGB))
  # plt.show()
  
  topleft = [99999, 99999]
  bottomright = [0, 0]
  for coord in max_cont:
    x, y = coord[0]
    topleft[0] = min(topleft[0], x)
    topleft[1] = min(topleft[1], y)
    bottomright[0] = max(bottomright[0], x)
    bottomright[1] = max(bottomright[1], y)
  
  return topleft[0]+2, topleft[1]+2, bottomright[0] - topleft[0]-2, bottomright[1] - topleft[1]-2


def thresholding(img: MatLike) -> MatLike:
  
  # Make the image with gray scale
  gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
  
  ret1,th1 = cv.threshold(gray,127,255,cv.THRESH_BINARY)
 
  # ret2,th2 = cv.threshold(gray,0,255,cv.THRESH_BINARY+cv.THRESH_OTSU)
 
  # Otsu's thresholding after Gaussian filtering
  # blur = cv.GaussianBlur(gray,(5,5),0)
  # _, th3 = cv.threshold(blur,0,255,cv.THRESH_BINARY+cv.THRESH_OTSU)
  return th1


def resize(img: MatLike) -> MatLike:
  return cv.resize(img,(9*HEIGHT, 9*WIDTH), interpolation = cv.INTER_AREA)
  

def remove_cell_edges(img: MatLike) -> MatLike:
  bgr = cv.cvtColor(img, cv.COLOR_GRAY2BGR)
  # bgr = img
  # gray = cv.cvtColor(img,cv.COLOR_BGR2GRAY)
  edges = cv.Canny(img,50,150,apertureSize = 3)
  lines = cv.HoughLines(edges,1,np.pi/180,100)
  for line in lines:
      rho,theta = line[0]
      a = np.cos(theta)
      b = np.sin(theta)
      x0 = a*rho
      y0 = b*rho
      x1 = int(x0 + 1000*(-b))
      y1 = int(y0 + 1000*(a))
      x2 = int(x0 - 1000*(-b))
      y2 = int(y0 - 1000*(a))
      cv.line(bgr,(x1,y1),(x2,y2),(0,0,255),2)
  # cv.imwrite('test_redline.png', bgr)
  # Convert BGR to HSV
  hsv = cv.cvtColor(bgr, cv.COLOR_BGR2HSV)
  # define range of red color in HSV
  lower_red = np.array([0, 50, 50])
  upper_red = np.array([10, 255, 255])
  # Threshold the HSV image to get only red colors
  mask = cv.inRange(hsv, lower_red, upper_red)
  # Bitwise-AND mask and original image
  bgr[mask != 0] = [255,255,255]
  return cv.cvtColor(bgr, cv.COLOR_BGRA2GRAY)


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


def sudoku_to_cells(pil_img: Image):
  img = convert_PIL_to_Matlike(pil_img)
  thresholded = thresholding(img)
  cv.imwrite('test_threshold.png', thresholded)
  # removed_cell_edges = remove_cell_edges(thresholded)
  # cv.imwrite('test_removed_edges.png', removed_cell_edges)
  cropped = crop_image(*max_contour(img, thresholded), thresholded)
  cv.imwrite('test_cropped.png', cropped)
  resized_img = resize(cropped)
  cv.imwrite('test_resized.png', resized_img)
  return separate_cell_boxes(resized_img)
