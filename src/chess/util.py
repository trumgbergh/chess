import pygame
screen_size = width, height = 730, 730
sq_size = screen_size[0] // 8
rec_size = sq_size * (3.0 / 4.0)
def cord2tlpixel(cord):
    return (cord[0] * sq_size, cord[1] * sq_size)

def cord2blpixel(cord):
    return (cord[0] * sq_size + 75, cord[1] * sq_size + 65)

def cord2centerpixel(cord):
    return (cord[0] * sq_size + sq_size // 2,
            cord[1] * sq_size + sq_size // 2)

def cord2D_to_chesscord(cord):
    col = chr(97 + cord[0])
    row = 8 - cord[1]
    return (col, row)
