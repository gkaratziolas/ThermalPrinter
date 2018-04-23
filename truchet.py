import ThermalPrinter
import Bitmap
import random

kTileSize = 24
kWidth    = 384
kHeight   = 384


def blank_canvas():
    canvas = []
    for i in range(0, kHeight):
        canvas.append([1]*kWidth)
    return canvas


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

    print_work(canvas, "Truchet - 2018")


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
    full_truchet()
    worm(100000)