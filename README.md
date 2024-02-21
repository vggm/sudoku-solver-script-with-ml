# Sudoku Solver

Sudoku Solver algorithm inspired by [`@santifiorino`](https://github.com/santifiorino/sudoku.com-solver).

This project implement an algorithm that solve a sudoku clicking on the topleft and bottomright corners of the sudoku in [sudoku.com](sudoku.com).

It can be possible thanks to implement a **KNN model** that *'translate'* images of numbers to numbers.

## How to use


> [!WARNING]
To run this projects, **it must be installed** the next libraries from **pip**:

| Packet | Function |
| :----: | :------: |
|scikit-learn|machine learning model|
|joblib|load and save models|
|numpy|math lib|
|pandas|data manipulation|
|matplotlib|data presentation|
|pynput|devices controll|
|pyautogui|devices controll|
|opencv-python|image manipulation|
|ipykernel|jupyter|

It can be installed all in one with the next command:

```
pip install scikit-learn joblib numpy pandas matplotlib pynput pyautogui opencv-python ipykernel
``` 

 > [!TIP]
 > I pretty recommend use a virtual environment, running the next command in the directory of the project:

```powershell
py -m venv "venv" 
```

And activate the venv (for Window):

```
.\venv\Scripts\activate
```

With all done, just run the main file and you will have to click twice (not double-click necessary) when the [sudoku.com](sudoku.com) page is on the screen (recommended on full screen and it's not necessary to do both clicks on the page, just the second one):

```powershell
py main.py
```
