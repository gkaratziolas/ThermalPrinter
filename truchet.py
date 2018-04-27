import ThermalPrinter
import Bitmap
import random
import math

kTileSize = 24
kWidth    = 384
kHeight   = 384

kBlack = 0
kWhite = 1


def blank_canvas():
    canvas = []
    for i in range(0, kHeight):
        canvas.append([1]*kWidth)
    return canvas

def draw_line(canvas, x0, y0, x1, y1, colour=kBlack):
    dx = x1-x0
    dy = y1-y0
    if math.fabs(dx) >= math.fabs(dy): # iterate across x
        for x in range(x0, x1, int(math.fabs(x1-x0)/(x1-x0))):
            y = int(y0 + (x-x0)*dy/dx + 0.5)
            canvas[y][x] = colour
    else: # iterate across y
        for y in range(y0, y1, int(math.fabs(y1-y0)/(y1-y0))):
            x = int(x0 + (y-y0)*dx/dy + 0.5)
            canvas[y][x] = colour

def img_to_bytes(img):
    val = ""
    for row  in img:
        row = [str(r) for r in row]
        row = "".join(row)
        val += row

    bts = int(val, 2).to_bytes(kWidth*kHeight//8, "big")
    return bts

def print_work(canvas, title):
    data = img_to_bytes(canvas)
    P = ThermalPrinter.ThermalPrinter("/dev/ttyUSB0")
    B = Bitmap.Bitmap()
    B.image_data = data
    B.height = kHeight
    B.width_bytes = kWidth//8

    P.print_bitmap(B)
    P.feed(1)
    P.send_bytes(title)
    P.feed(3)

def draw_square_tile(tx, ty, canvas):
    for x in range((tx)*kTileSize, (tx+1)*kTileSize):
        for y in range((ty)*kTileSize, (ty+1)*kTileSize):
            canvas[y][x] = 0

def draw_truchet_tile(tx, ty, tri, canvas):
    if tri == 0 or tri == 1:
        tri_width = kTileSize
        diff      = -1
    else:
        tri_width = 1
        diff      = 1
    for x in range((tx)*kTileSize, (tx+1)*kTileSize):
        for y in range((ty)*kTileSize, (ty+1)*kTileSize):
            if tri == 1 or tri == 3:
                if y - (ty)*kTileSize < tri_width:
                    canvas[y][x] = 0
                else:
                    canvas[y][x] = 1
            else:
                if y - (ty)*kTileSize < tri_width - 1:
                    canvas[y][x] = 1
                else:
                    canvas[y][x] = 0

        tri_width += diff  

def full_truchet():
    canvas = blank_canvas()
    for x in range(0, kWidth//kTileSize):
        for y in range(0, kHeight//kTileSize):
            t = random.randint(0, 3)
            draw_truchet_tile(x,y,t, canvas)

    print_work(canvas, "Truchet ({}) - 2018".format(kTileSize))

def mess_of_lines(n):
    canvas = blank_canvas()
    x0, y0 = 0,0
    for i in range(n):
        x1 = random.randint(0, kWidth-1)
        y1 = random.randint(0, kHeight-1)
        draw_line(canvas, x0, y0, x1, y1)
        x0, y0 = x1, y1
    print_work(canvas, "mess of lines lines ({}) - 2018".format(n))

def star(p, r, cx, cy):
    canvas = blank_canvas()
    for i in range(p):
        theta = 2*math.pi*(i/p)
        x = int(r*math.cos(theta) + cx)
        y = int(r*math.sin(theta) + cy)
        draw_line(canvas, cx, cy, x, y)
    print_work(canvas, "Star ({}) - 2018".format(p))

def star2(p, r, cx, cy):
    canvas = blank_canvas()
    for i in range(p):
        theta = 2*math.pi*(i/p)
        x = int(r*math.cos(theta) + cx)
        y = int(r*math.sin(theta) + cy)
        draw_line(canvas, cx, cy, x, y)

        theta1 = 2*math.pi*((i-1)/p)
        x1 = int(r*math.cos(theta1) + x)
        y1 = int(r*math.sin(theta1) + y)
        draw_line(canvas, x, y, x1, y1)

        theta2 = 2*math.pi*((i+1)/p)
        x2 = int(r*math.cos(theta2) + x)
        y2 = int(r*math.sin(theta2) + y)
        draw_line(canvas, x, y, x2, y2)
    print_work(canvas, "Star2 ({}) - 2018".format(p))

def gradient():
    canvas = blank_canvas()
    for y in range(kHeight):
        for x in range(kHeight):
            a = random.uniform(0,1)
            if x/kWidth < a:
                canvas[y][x] = kBlack
    print_work(canvas, "Random Dither - 2018")

def gradient2(r):
    cx = kWidth//2
    cy = kHeight//2
    canvas = blank_canvas()
    for y in range(kHeight):
        for x in range(kWidth):
            a = random.uniform(0,1)

            if math.sqrt((x-cx)**2 + (y-cy)**2) < r:
                if x/kWidth < a:
                    canvas[y][x] = kBlack
            else:
                if x/kWidth > a:
                    canvas[y][x] = kBlack

    print_work(canvas, "Circular Dither ({}) - 2018".format(r))

def worm(n):
    canvas = blank_canvas()
    x, y = kWidth//2, kHeight//2
    for i in range(0, n):
        x += random.randint(-1,1)
        y += random.randint(-1,1)
        if x < 0:
            x = 0
        if y < 0:
            y = 0
        if x > kWidth-1:
            x = kWidth-1
        if y > kHeight-1:
            y = kHeight-1
        canvas[y][x] = 0

    print_work(canvas, "Worm {} - 2018".format(n))


if __name__ == "__main__":
    gradient2(20)
    #star2(20, 70, kHeight//2, kWidth//2)
    #full_truchet()
    #worm(100000)