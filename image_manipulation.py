from cv2.typing import MatLike
from PIL.Image import Image
import numpy as np
import cv2 as cv


def convert_PIL_to_Matlike(pil_img: Image) -> MatLike:
  open_cv_image = np.array(pil_img)
  # Convert RGB to BGR
  open_cv_image = open_cv_image[:, :, ::-1].copy()
  return open_cv_image


def thresholding(img: MatLike) -> MatLike:
  
  # Make the image with gray scale
  gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
 
  ret2,th2 = cv.threshold(gray,0,255,cv.THRESH_BINARY+cv.THRESH_OTSU)
 
  # Otsu's thresholding after Gaussian filtering
  blur = cv.GaussianBlur(gray,(5,5),0)
  _, th3 = cv.threshold(blur,0,255,cv.THRESH_BINARY+cv.THRESH_OTSU)
  return th2


def resize(img: MatLike) -> MatLike:
  return cv.resize(img,(270, 270), interpolation = cv.INTER_CUBIC)
  

def remove_cell_edges(img: MatLike) -> MatLike:
  gray = cv.cvtColor(img,cv.COLOR_BGR2GRAY)
  edges = cv.Canny(gray,50,150,apertureSize = 3)
  lines = cv.HoughLines(edges,1,np.pi/180,200)
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
      cv.line(img,(x1,y1),(x2,y2),(0,0,255),2)
  
  # Convert BGR to HSV
  hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
  # define range of blue color in HSV
  lower_red = np.array([0, 50, 50])
  upper_red = np.array([10, 255, 255])
  # Threshold the HSV image to get only red colors
  mask = cv.inRange(hsv, lower_red, upper_red)
  # Bitwise-AND mask and original image
  img[mask != 0] = [255,255,255]
  return img


def sudoku_only_numbers(pil_img: Image):
  img = convert_PIL_to_Matlike(pil_img)
  resized_img = resize(img)
  removed_cell_edges = remove_cell_edges(resized_img)
  thresholded = thresholding(removed_cell_edges)
  cv.imwrite('sudoku_gen.png', thresholded)
