import cv2
import pandas as pd
import tkinter as tk
from tkinter import filedialog


root = tk.Tk()
root.withdraw()

file_path = filedialog.askopenfilename(
    title="Select an Image",
    filetypes=[("Image Files", "*.jpg *.png *.jpeg")]
)

img = cv2.imread(file_path)
img = cv2.resize(img, (800, 600))

colors = pd.read_csv("colors.csv")

clicked = False
r = g = b = xpos = ypos = 0


def get_color_name(R, G, B):
    minimum = 10000
    cname = ""

    for i in range(len(colors)):
        d = abs(int(R) - int(colors.loc[i, "Red (8 bit)"])) + \
            abs(int(G) - int(colors.loc[i, "Green (8 bit)"])) + \
            abs(int(B) - int(colors.loc[i, "Blue (8 bit)"]))

        if d <= minimum:
            minimum = d
            cname = colors.loc[i, "Name"]   

    return cname


def draw_function(event, x, y, flags, param):
    global b, g, r, xpos, ypos, clicked

    if event == cv2.EVENT_LBUTTONDOWN:
        clicked = True
        xpos = x
        ypos = y
        b, g, r = img[y, x]   


cv2.namedWindow("image")
cv2.setMouseCallback("image", draw_function)

img_copy = img.copy()

while True:
    cv2.imshow("image", img_copy)

    key = cv2.waitKey(1) & 0xFF
    if key == 27:  # ESC
        break

    if clicked:
        img_copy = img.copy()

        color_name = get_color_name(r, g, b)
        text = f"{color_name}  R={r} G={g} B={b}"

        cv2.rectangle(img_copy, (20, 20), (650, 70), (int(b), int(g), int(r)), -1)

        cv2.putText(img_copy, text, (30, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8,
                    (255, 255, 255), 2)

cv2.destroyAllWindows()